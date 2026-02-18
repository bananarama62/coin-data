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

``` text
+----------------+-----------------------+--------------+-------+---------------+------+
| coin_id        | precious_metal_weight | fineness     | metal | value         | year |
+----------------+-----------------------+--------------+-------+---------------+------+
| pol_zloty_10_1 |          0.5305000000 | 0.7500000000 | ag    | 10.0000000000 | 1933 |
+----------------+-----------------------+--------------+-------+---------------+------+
```

This selected all coins from the database with "zloty" in the coin id, with face value of 10, and were minted in 1933. Assuming this worked, the database should be correctly set up. See the docs folder in the precious metals calculator repository for more in depth information about the schema and how to add new coins (or other objects made of precious metals) to the database.

## Country statuses

A country (or entity) can be in one of the following states:

0. none: The country is acknowleged, but no plan exists for it to be implemented.
1. absent: The country is planned but does not have enough coin data complete to qualify for the base state.
2. base: All precious metal coins for the country minted from 1850-1964 are present. Years for individual coins can be overly broad, to fill in gaps. All years that the coin was made in must be present though.
3. refined: The mintage years for all coins must be accurate. No more filling in of gaps.
4. expanded: All precious metal coins minted by the country in all years are present. Similarly to base state, gaps may be filled.
5. complete: All gaps are unfilled and mintage years must be accurate.
6. complete+: Introduces all non-precious metal coins of all years. Gaps may be filled.
7. complete++: All gaps must be unfilled. All coins minted for general circulation that the country has ever minted are present.

The four official series for entries will be:
* **base** for entries for the base and refined states
* **expanded** for entries for the expanded and complete states
* **non-precious** for entries for the complete+ and complete++ states

| name                     | id         | state                 |
|:------------------------:|:----------:|:---------------------:|
| afghanistan              | afg        | base                  |
| albania                  | alb        | base                  |
| argentina                | arg        | base                  |
| australia                | aus        | base                  |
| austria                  | aut        | base                  |
| belgium                  | bel        | base                  |
| bulgaria                 | bgr        | base                  |
| bermuda                  | bmu        | base                  |
| bolivia                  | bol        | base                  |
| brazil                   | bra        | base                  |
| canada                   | can        | base                  |
| switzerland              | che        | base                  |
| chile                    | chl        | base                  |
| china                    | chn        | base                  |
| colombia                 | col        | base                  |
| comoros                  | com        | base                  |
| costa rica               | cri        | base                  |
| czechoslovakia           | csk        | base                  |
| cuba                     | cub        | base                  |
| curacao                  | cuw        | base                  |
| Cyprus                   | cyp        | base                  |
| germany                  | deu        | base                  |
| denmark                  | dnk        | base                  |
| ecuador                  | ecu        | base                  |
| egypt                    | egy        | base                  |
| eritrea                  | eri        | base                  |
| spain                    | esp        | base                  |
| estonia                  | est        | base                  |
| ethiopia                 | eth        | base                  |
| finland                  | fin        | base                  |
| fiji                     | fji        | base                  |
| france                   | fra        | base                  |
| great britain            | gbr        | base                  |
| greece                   | grc        | base                  |
| guatemala                | gtm        | base                  |
| hawaii                   | haw        | base                  |
| hong kong                | hkg        | base                  |
| honduras                 | hnd        | base                  |
| haiti                    | hti        | base                  |
| hungary                  | hun        | base                  |
| india                    | ind        | base                  |
| ireland                  | irl        | base                  |
| iran                     | irn        | base                  |
| iraq                     | irq        | base                  |
| iceland                  | isl        | base                  |
| israel                   | isr        | base                  |
| italy                    | ita        | base                  |
| jamaica                  | jam        | base                  |
| japan                    | jpn        | base                  |
| cambodia                 | khm        | base                  |
| korea                    | kor        | base                  |
| kuwait                   | kwt        | base                  |
| lebanon                  | lbn        | base                  |
| liberia                  | lbr        | base                  |
| liechtenstein            | lie        | base                  |
| lithuania                | ltu        | base                  |
| luxembourg               | lux        | base                  |
| latvia                   | lva        | base                  |
| macau                    | mac        | base                  |
| morocco                  | mar        | base                  |
| mexico                   | mex        | base                  |
| myanmar                  | mmr        | base                  |
| mongolia                 | mng        | base                  |
| newfoundland             | nfl        | base                  |
| netherlands, the         | nld        | base                  |
| norway                   | nor        | base                  |
| nepal                    | npl        | base                  |
| new zealand              | nzl        | base                  |
| panama                   | pan        | base                  |
| peru                     | per        | base                  |
| philippines              | phl        | base                  |
| poland                   | pol        | base                  |
| portugal                 | prt        | base                  |
| paraguay                 | pry        | base                  |
| romania                  | rou        | base                  |
| russia                   | rus        | base                  |
| saudi arabia             | sau        | base                  |
| el salvador              | slv        | base                  |
| serbia                   | srb        | base                  |
| suriname                 | sur        | base                  |
| sweden                   | swe        | base                  |
| syria                    | syr        | base                  |
| thailand                 | tha        | base                  |
| turkey                   | tur        | base                  |
| united arab republic     | uar        | base                  |
| uruguay                  | ury        | base                  |
| united states of america | usa        | base                  |
| venezuela                | ven        | base                  |
| south africa             | zaf        | base                  |
| arabian sultanate (yemen)| N/A        | absent                |
| belgian congo            | N/A        | absent                |
| british guiana           | N/A        | absent                |
| british honduras         | N/A        | absent                |
| british north borneo     | N/A        | absent                |
| british west africa      | N/A        | absent                |
| ceylon                   | N/A        | absent                |
| crete                    | N/A        | absent                |
| danish west indies       | N/A        | absent                |
| danzig                   | N/A        | absent                |
| dominican republic       | N/A        | absent                |
| east africa              | N/A        | absent                |
| french cochin china      | N/A        | absent                |
| french indo-china        | N/A        | absent                |
| german east africa       | N/A        | absent                |
| german new guinea        | N/A        | absent                |
| hejaz                    | N/A        | absent                |
| italian somaliland       | N/A        | absent                |
| katanga                  | N/A        | absent                |
| malaya and british borneo| N/A        | absent                |
| mauritius                | N/A        | absent                |
| mobasa                   | N/A        | absent                |
| monaco                   | N/A        | absent                |
| montenegro               | N/A        | absent                |
| mozambique               | N/A        | absent                |
| muscat and oman          | N/A        | absent                |
| netherland antilles, the | N/A        | absent                |
| new brunswick            | N/A        | absent                |
| new caledonia            | N/A        | absent                |
| new guinea               | N/A        | absent                |
| nicaragua                | N/A        | absent                |
| nigeria- bri. west africa| N/A        | absent                |
| palestine                | N/A        | absent                |
| portuguese india         | N/A        | absent                |
| puerto rico              | N/A        | absent                |
| rhodesia, southern       | N/A        | absent                |
| st. thomas and prince    | N/A        | absent                |
| san marino               | N/A        | absent                |
| sarawak                  | N/A        | absent                |
| seychelles               | N/A        | absent                |
| south african republic   | N/A        | absent                |
| straits settlements      | N/A        | absent                |
| timor                    | N/A        | absent                |
| vatican city             | N/A        | absent                |
| yugoslavia               | N/A        | absent                |
| zanzibar                 | N/A        | absent                |
