#!/bin/bash


# Source progress bar
source ./progress_bar.sh

main () {

  db_user=$1
  database=$2
  dir=$3

  if [ -z "${dir}" ]; then
    dir="./"
  fi

  if [ -z "${db_user}" -o -z "${database}" ]; then
    echo "Usage: $0 user database directory"
    exit 1
  fi

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

  files=("setup_db.sql" "setup_countries.sql" "setup_denominations.sql" "setup_values.sql" "setup_coins.sql" "purchases.sql")

  
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
    echo ${dir}/${files[$i]}
    mariadb --user=$db_user --password=$PASSWORD $database < ${dir}/${files[$i]}
    if [ $? -ne 0 ]; then
      break
    fi
    draw_progress_bar $(( ($i+1)*100/$array_length ))
  done
  destroy_scroll_area

}

main $1 $2 $3
