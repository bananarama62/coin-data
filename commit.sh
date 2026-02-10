#!/bin/bash

cat ./test_setup_countries.sql >> ./setup_countries.sql
cat ./test_setup_denominations.sql >> ./setup_denominations.sql
cat ./test_setup_values.sql >> ./setup_values.sql
cat ./test_setup_coins.sql >> ./setup_coins.sql
cat ./test_setup_countries.sql >> ./setup_coins_years.sql

rm ./test_setup_*.sql
