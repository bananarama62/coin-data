# coin-data
This repository will serve as the storage location for files that can be used to build the database needed for the precious metal calculator program found at: https://github.com/JMGillum/melt-calculator. The SQL files are what are needed to build the database. They are written in MySQL, so MySQL or MariaDB will be required (the melt-calculator program uses MariaDB, so this is recommended).   

# Installation
The first step before these files can be loaded into a database system, is to have the database system installed. We will use MariaDB, as that is what the program was written for and tested with. Follow the instructions: https://mariadb.com/docs/server/mariadb-quickstart-guides/installing-mariadb-server-guide to install MariaDB, then return here.

## Automatic
Contained within this repository is the bash script: `db.sh`, which handles loading all of the files into the database system for you. All that you have to do is to invoke the script with at least two arguments: the user to connect to the database with, the name of the database to use, and optionally: the path to the directory storing the SQL files, which is ./ (unless you moved them).  
Ex: `./db.sh root coin_data` or optionally: `./db.sh root coin_data ./`  
The script will prompt you as needed, and will load all of the files into the database system as needed. 

## Manual
The files must be loaded into the database system in the following order:
1. setup_db.sql -> This creates all of the tables for the database.
2. setup_countries.sql -> This stores all of the data for the countries.
3. setup_denominations.sql -> This stores all of the data for the monetary denominations.
4. setup_values.sql -> This stores all of the data for the coin face values.
5. setup_coins.sql -> This stores all of the data for individual coins.
6. setup_coins_years.sql -> This stores all of the years that the coins were available in.
7. purchases.sql -> This file is absent from the repository. It will be created throughout usage of the program. It stores any coin purchases made.

Each file builds upon the last, so they must be ran in this exact order (otherwise your computer will explode).

## Testing
To check that everything worked, you can log into MariaDB with: `mariadb -u <user> -p <database_name>`. Then enter: `show tables`. This will bring up the name of every table in this database. The output should look like:  
```
+---------------------+  
| Tables_in_coin_data |  
+---------------------+  
| coins               |  
| countries           |  
| country_names       |  
| denomination_names  |  
| denominations       |  
| face_values         |  
| face_values_names   |  
| metals              |  
| purchases           |  
| specific_coins      |  
| tags                |  
| version             |  
| years               |  
+---------------------+  
```

If you have less tables than this, one of the SQL files was not loaded properly. Assuming you have all of the correct tables, enter the following SQL query:  
```
select coins.coin_id,precious_metal_weight,fineness,metal,value,year
from coins join years on coins.coin_id=years.coin_id join face_values on coins.face_value_id=face_values.value_id
where coins.coin_id like "%zloty%" and years.year=1933 and face_values.value=10;
```  

The output should look like: 
```
+----------------+-----------------------+--------------+-------+---------------+------+
| coin_id        | precious_metal_weight | fineness     | metal | value         | year |
+----------------+-----------------------+--------------+-------+---------------+------+
| pol_zloty_10_1 |          0.5305000000 | 0.7500000000 | ag    | 10.0000000000 | 1933 |
+----------------+-----------------------+--------------+-------+---------------+------+
```
This selected all coins from the database with "zloty" in the coin id, with face value of 10, and were minted in 1933. Assuming this worked, the database should be correctly set up. See the docs folder in the precious metals calculator repository for more in depth information about the schema and how to add new coins (or other objects made of precious metals) to the database.
