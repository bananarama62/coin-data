#!/bin/bash


db_user=$1
database=$2
dir=$3

# Defaults to CWD if one is not specified
if [ -z "${dir}" ]; then
  dir="./updates/"
  echo Using directory: "$dir"
fi

# User and database must be specified in command line
if [ -z "${db_user}" -o -z "${database}" ]; then
  echo "Usage: $0 user database directory"
  exit 1
fi

echo "This script will modify the database and may irreparably damage it. Backup the database before continuing."
read -p "Continue? (y)Yes/(n)No:- " choice
case $choice in
  [yY]* ) ;;
  *) exit 0 ;;
esac

# Gets database password from user
printf "Password for $database as $db_user: "
trap 'stty echo' INT EXIT
stty -echo
read password
printf "\n"

# Used to detect infinite loop (if version does not change after script is run)
previous_major=-1
previous_minor=-1

# Updates as many times as needed
while true; 
do
  # Fetches current version number from database
  result="$(mariadb --user=$db_user --password=$password $database -e'select major,minor from version;')"
  if [ $? -ne 0 ]; then
    exit
  fi

  # Extracts major and minor version numbers from outpur
  result=($result)
  major=${result[2]}
  minor=${result[3]}

  # Outputs the version found and what the previous version is.
  echo "Found version number: $major.$minor in database."
  echo Previous version: "$previous_major"."$previous_minor"

  # If previous version is the same as the current version,
  # the last update did not update the version number and an
  # infinite loop will occur, so exit
  if (( $previous_major == $major && $previous_minor == $minor )); then
    echo "Infinite Loop detected. Aborting..."
    exit
  fi
  # Updates previous version number to be this current one.
  previous_major=$major
  previous_minor=$minor

  # Finds all possible updates from the current version.
  # (Any file that starts with major_minor)
  search_string="$major"_"$minor"*
  update_file=$(find $dir -name "$search_string")

  # Split string by spaces (turns str to array of files found)
  update_file=($update_file)

  # Used to determine what version is being updated to
  updating_to_major=$major
  updating_to_minor=$minor
  updating_to_file=""

  # Loops through each file found the updates from this current version.
  # Finds the one that updates to the greatest version, and uses that.
  for f in "${update_file[@]}";
  do
    echo Found update file: $f
    # Searches for the version that the file updates to
    if [[ "$f" =~ .*to_(([0-9]+)_([0-9]+))\..* ]]; then
      echo ${BASH_REMATCH[1]}

      # Extracts the major and minor versions that the file updates to
      new_major=${BASH_REMATCH[2]}
      new_minor=${BASH_REMATCH[3]}

      # Determines if this file's new version is the greatest one found.
      if (( $updating_to_major < 0  || ( $new_major > $updating_to_major ) || ( $new_major == $updating_to_major && $new_minor > $updating_to_minor ) )); then
        updating_to_major=$new_major
        updating_to_minor=$new_minor
        updating_to_file=$f
      fi

      # Prints out the greatest version found so far
      echo Greatest version: "$updating_to_major"_"$updating_to_minor"

    else
      # The file found does not have the correct format '.*_to_major_minor\..*'
      echo "Invalid format"
    fi
  done

  # A file for updating was found.
  if [[ ! -z $updating_to_file ]]; then
    # Prints out that it is possible and which file will be used
    echo "Update possible."
    echo "$updating_to_file"

    # Executes the actual update
    mariadb --user=$db_user --password=$password $database < $updating_to_file

    # Check if an error occured
    if [ $? -ne 0 ]; then
      echo "Error. Aborting..."
      exit
    fi
    echo Update successful

  # No file for updating was found
  else
    echo "Unable to update any further."
    exit 
  fi
done
