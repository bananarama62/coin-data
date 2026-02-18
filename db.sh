#!/bin/bash


# Source progress bar
source ./progress_bar.sh

main () {

  db_user=$1
  database=$2
  dir=$3

  # Defaults to CWD if one is not specified
  if [ -z "${dir}" ]; then
    dir="./"
  fi
  
  # User and database must be specified in command line
  if [ -z "${db_user}" -o -z "${database}" ]; then
    echo "Usage: $0 user database directory"
    exit 1
  fi

  # Gets confirmation for continuing.
  echo "User: $db_user will connect to database: $database and use data from: $dir"
  read -p "Continue? (y)Yes/(n)No:- " choice
  case $choice in
    [yY]* ) ;;
    *) exit 0 ;;
  esac

  printf "Password for $database as $db_user: "
  trap 'stty echo' INT EXIT
  stty -echo
  read PASSWORD
  printf "\n"

  # List of all files that will be fed into database
  files=("base_setup_db.sql" "base_setup_countries.sql" "base_setup_denominations.sql" "base_setup_values.sql" "base_setup_coins.sql" "base_setup_coins_years.sql" "base_purchases.sql")

  # Drops and recreates database
  mariadb --user=$db_user --password=$PASSWORD -e "DROP DATABASE IF EXISTS $database; CREATE DATABASE $database;"
  if [ $? -ne 0 ]; then
    exit 1
  fi
  # Make sure that the progress bar is cleaned up when user presses ctrl+c
  enable_trapping
  # Create progress bar
  setup_scroll_area

  array_length=${#files[@]}
  for (( i=0; i<${array_length}; ++i )); 
  do
    file=${dir}/${files[$i]}
    echo $file
    # Skips files that do not exist and hope they were optional
    if [  -f "$file" ]; then
      mariadb --user=$db_user --password=$PASSWORD $database < $file
      if [ $? -ne 0 ]; then
        break
      fi

    # File did not exist
    else
      echo File does not exist. Skipping...
    fi
    draw_progress_bar $(( ($i+1)*100/$array_length ))
  done
  destroy_scroll_area

}

main $1 $2 $3

