#   Author: Josh Gillum              .
#   Date: 7 August 2025             ":"         __ __
#                                  __|___       \ V /
#                                .'      '.      | |
#                                |  O       \____/  |
#^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^
#
#   MUST BE RUN FROM ROOT PROJECT DIRECTORY!!!
#
#   This script makes it easier to add new coins to the database. It does not
#   actually add the coins to the database, it simply prints out the sql
#   queries that would do so. It will prompt for the needed country, 
#   denomination, and value if necessary.
#   
#^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^
import mariadb
import sys
import pathlib
from datetime import datetime
import math
import copy

# Various files for output
environment_prefix = "test_"
log_file = pathlib.PurePath('addCoins.log')
countries_file = pathlib.PurePath(f'{environment_prefix}setup_countries.sql')
denominations_file = pathlib.PurePath(f'{environment_prefix}setup_denominations.sql')
values_file = pathlib.PurePath(f'{environment_prefix}setup_values.sql')
coins_file = pathlib.PurePath(f'{environment_prefix}setup_coins.sql')

# Ensures that files are in project_root/db directory
cwd = pathlib.Path.cwd()
if not cwd.name == 'db':
    cwd = cwd / 'db'
log_file = cwd / log_file
countries_file = cwd / countries_file
denominations_file = cwd / denominations_file
values_file = cwd / values_file
coins_file = cwd / coins_file

db_config = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "test",
    "database": "coin_data",
}
# Lists of query strings
queries_countries = []
queries_denominations = []
queries_values = []
queries_coins = []

# List of ids for items added during this session
added_countries = []
added_denominations = []
added_values = []
added_coins = []

# String appended to the prefix as the value of this level
country_code = ""
denomination_code = ""
value_code = ""

# prefix for id of level. Ex: coin_prefix is the denomination_id for the coin and prefix of the coin_id
denomination_prefix = ""
value_prefix = ""
coin_prefix = ""

def log(text,file=None):
    if file is None:
        file = log_file
    with open(file,"a") as f:
        f.write(f"{text}\n")



def addCountry(information):
    country_id = information["country_code"].lower()
    name = input(f"Country name for ({country_id}): ").lower()
    while True:
        alternative_names = []
        if not name:
            name = input("A name is required. Enter it here:")
            continue
        for i in range(5):
            response = input("Alternative name? (enter empty string to skip): ")
            if response:
                alternative_names.append(response.lower())
            else:
                break
        print(f"\n---Country Name: {name}---")
        for alternative_name in alternative_names:
            print(f"  {alternative_name}")
        
        response = input("Press enter to continue. Enter new name to re-enter names: ")
        if response:
            name = response
        else:
            break
    query_string = "INSERT INTO countries(country_id,name" 
    for i in range(len(alternative_names)):
        query_string += f",alternative_name_{i+1}"
    query_string += f') VALUES("{country_id}","{name}"'
    for i in range(len(alternative_names)):
        query_string += f',"{alternative_names[i]}"'
    query_string += ");"
    log(query_string)
    added_countries.append(country_id)
    queries_countries.append(query_string)


def addDenomination(information):
    prefix = information["denomination_prefix"].lower()
    code = information["denomination_code"].lower()
    name = code
    response = input(f"Default name for ({prefix}_{code}) is {name}. Press enter to continue or enter new name here: ").lower()
    if response:
        name = response
    while True:
        alternative_names = []
        if not name:
            name = input("A name is required. Enter it here:")
            continue
        for i in range(5):
            response = input("Alternative name? (enter empty string to skip): ")
            if response:
                alternative_names.append(response.lower())
            else:
                break
        print(f"\n---Denomination name: {name}---")
        for alternative_name in alternative_names:
            print(f"  {alternative_name}")
        
        response = input("Press enter to continue. Enter new name to re-enter names: ")
        if response:
            name = response
        else:
            break
    query_string = "INSERT INTO denominations(denomination_id,country_id,name" 
    for i in range(len(alternative_names)):
        query_string += f",alternative_name_{i+1}"
    query_string += f') VALUES("{prefix}_{code}","{prefix}","{name}"'
    for i in range(len(alternative_names)):
        query_string += f',"{alternative_names[i]}"'
    query_string += ");"
    log(query_string)
    added_denominations.append(f"{prefix}_{code}")
    queries_denominations.append(query_string)

def addValue(information):
    prefix = information["value_prefix"].lower()
    code = information["value_code"]
    value = code
    while True:
        name = ""
        alternative_names = []
        if "fractional" in code:
            response = input("Use standard fractional names? (y/n): ").lower()
            if response == 'y' or response =='yes':
                nums = code.split("_")[1:]
                whole_num = 0
                numerator = 0
                denominator = 0
                try:
                    if len(nums) >= 3:
                        whole_num = int(nums[-3])
                    if len(nums) >= 2:
                        numerator = int(nums[-2])
                        denominator = int(nums[-1])
                except ValueError:
                    print("Error parsing fractional name. Select 'no' for using fractional names to enter your own.")
                    continue

                whole_num_str = str(whole_num)+"-" if whole_num else ""
                name = f"{whole_num_str}{numerator}/{denominator}"
                if whole_num:
                    alternative_names = [f"{whole_num_str}{numerator}/{denominator}".replace("-"," "),f"{numerator + whole_num*denominator}/{denominator}"]
                value = whole_num + numerator/denominator

        else:
            name = input(f"Value name for ({prefix}_{code}) (enter empty string to skip): ").lower()
            if not name:
                break
            for i in range(5):
                response = input("Alternative name? (enter empty string to skip): ")
                if response:
                    alternative_names.append(response.lower())
                else:
                    break
        print(f"\n---Value name: {name}---")
        for alternative_name in alternative_names:
            print(f"  {alternative_name}")
        
        response = input("Press enter to continue. Enter any character to re-enter names: ")
        if not response:
            break
    query_string = "INSERT INTO face_values(value_id,denomination_id" 
    if name:
        query_string += ",name"
        for i in range(len(alternative_names)):
            query_string += f",alternative_name_{i+1}"
    query_string += f',value) VALUES("{prefix}_{code}","{prefix}"'
    if name:
        query_string += f',"{name}"'
        for i in range(len(alternative_names)):
            query_string += f',"{alternative_names[i]}"'
    query_string += f",{value}"
    query_string += ");"
    log(query_string)
    added_values.append(f"{prefix}_{code}")
    queries_values.append(query_string)

def addCoin(information):
    prefix = information['coin_prefix'].lower()
    code = information["coin_number"]
    if information["nickname"] is None:
        name = input(f"Coin name for ({prefix}_{code}) (enter empty string to skip): ").lower()
        while True:
            if name:
                print(f"\n---Coin name: {name}---")
                response = input("Press enter to continue. Enter name here to re-enter name: ")
            else:
                name = ""
                response = False
            if response:
                name = response
                continue
            else:
                information["nickname"] = name
                break
    gross_weight = information["gross_weight"]
    if gross_weight is not None:
        try:
            gross_weight_usable = float(gross_weight)
        except ValueError:
            information["gross_weight"] = None
    fineness = information["fineness"]
    precious_metal_weight = information["precious_metal_weight"]
    gross_weight_usable = 0.0
    # Updates gross weight if requested
    if not information["gross_weight"]:
        while True:
            gross_weight = input("Enter gross weight (in grams):")
            try:
                gross_weight_usable = float(gross_weight)
                information["gross_weight"] = gross_weight
                information["precious_metal_weight"] = None
                break
            except ValueError:
                print("Gross weight must be numeric.")
                continue
    # Updates fineness if requested
    if not information["fineness"]:
        while True:
            try:
                fineness = input("Enter fineness (90% = 0.9):")
                fineness = float(fineness) # Ensures that user enters numeric value
                if fineness > 100:
                    fineness = str(fineness).split(".")
                    fineness = "".join(fineness)
                    fineness = float(f"{fineness[:2]}.{fineness[2:]}")
                if fineness > 1:
                    while fineness >= 10:
                        fineness = fineness / 10
                    fineness = float(fineness/10)
                fineness = round(fineness,4)
                information["fineness"] = fineness
                information["precious_metal_weight"] = None
                break
            except ValueError:
                print("Fineness must be numeric.")
                continue
    # Updates precious metal weight if requested (updating gross weight or fineness will request it)
    if not information["precious_metal_weight"]:
        precious_metal_weight = gross_weight_usable * fineness * 0.03215075
        precious_metal_weight = round(precious_metal_weight,4)
        response = input(f"Is the calculated precious metal weight ({precious_metal_weight}) correct? (Press enter to continue. Enter it here (in troy ounces) to manually enter it.)")
        if response: # User wanted to change. Continually loop until they are satisfied
            precious_metal_weight = response
            while True:
                response = input(f"Is {precious_metal_weight} correct? (Press enter to continue. Enter it here (in troy ounces) to modify): ")
                if response:
                    precious_metal_weight = response
                    precious_metal_weight = float(precious_metal_weight)
                    continue
                break
        information["precious_metal_weight"] =  precious_metal_weight
    if not information["metal"]:
        valid_metal = False
        while not valid_metal:
            metal = input("Enter periodic symbol for metal (sil=ag,gol=au,plat=pt,pala=pd,rho=rh):").lower()
            valid_metal = [x for x in ["ag","au","pt","pd","rh"] if metal == x]
        information["metal"] = metal
    if not information["years"]:
        years = ""
        while True:
            years = input("Enter years (comma separated)(shorthand x-y is acceptable):")
            if years:
                years_list = years.split(",")
                years = ""
                fail = False
                for item in years_list:
                    if fail:
                        break
                    try:
                        int(item)
                        years += f"{item}, "
                    except ValueError:
                        if "-" in item:
                            temp = item.find("-")
                            beginning = item[:temp]
                            end = item[temp+1:]
                            try:
                                beginning = int(beginning)
                                end = int(end)
                                if end < 100:
                                    century = math.floor(beginning / 100) * 100
                                    start_year = beginning % 100
                                    if end < start_year:
                                        century += 100
                                    end += century
                                for i in range(beginning,end+1):
                                    years += f"{i}, "
                            except ValueError: # Two numbers were not actually numbers
                                print("All values must be numbers")
                                fail = True
                                continue
                        else:
                            print("Values must be individual years or of the form x-y (ex: 1898-1900)")
                            fail = True
                            continue
                if not fail:
                    years = years[:-2] # Chops off trailing comma and space
                    information["years"] = years
                    break

    query_string = "INSERT INTO coins(coin_id,face_value_id" 
    if information["nickname"]:
        query_string += ",name"
    query_string += ",gross_weight,fineness,precious_metal_weight,years,metal"
    query_string += f') VALUES("{prefix}_{code}","{prefix}"'
    if information["nickname"]:
        query_string += f',"{information["nickname"]}"'
    query_string += f',{information["gross_weight"]},{information["fineness"]},{information["precious_metal_weight"]},"{information["years"]}","{information["metal"]}"'
    query_string += ");"
    log(query_string)
    added_coins.append(f"{prefix}_{code}")
    queries_coins.append(query_string)

if __name__ == "__main__":
    log(str(datetime.now()))
    conn = None
    cursor = None
    try:
        # 2. Establish a Connection
        print("Connecting to MariaDB...")
        conn = mariadb.connect(**db_config)
        print("Connection successful!")

        # 3. Create a Cursor Object
        cursor = conn.cursor()
        skip = 0
        information = {
                "country_code":None,
                "denomination_code":None,
                "value_code":None,
                "coin_number":1,
                "denomination_prefix":None,
                "value_prefix":None,
                "coin_prefix":None,
                "nickname":None,
                "gross_weight":None,
                "fineness":None,
                "precious_metal_weight":None,
                "metal":None,
                "years":None,
                }
        while True:
            # Lists of query strings
            copy_queries_countries = copy.copy(queries_countries)
            copy_queries_denominations = copy.copy(queries_denominations)
            copy_queries_values = copy.copy(queries_values)
            copy_queries_coins = copy.copy(queries_coins)

            # List of ids for items added during this session
            copy_added_countries = copy.copy(added_countries)
            copy_added_denominations = copy.copy(added_denominations)
            copy_added_values = copy.copy(added_values)
            copy_added_coins = copy.copy(added_coins)
            if not information["country_code"]:
                information.update(country_code=input("ISO 3 Alpha country code=").lower())
            if not information["denomination_code"]:
                information.update(denomination_code=input("Denomination code=").lower())
            if not information["value_code"]:
                information.update(value_code=input("Value code=").lower())
            information["denomination_prefix"] = f"{information['country_code']}"
            information["value_prefix"] = f"{information['denomination_prefix']}_{information['denomination_code']}"
            information["coin_prefix"] = f"{information['value_prefix']}_{information['value_code']}"
            information["coin_number"] = 1


            # --- Example: Select Data ---
            print("\nSelecting data...")
            select_query = "SELECT value_id FROM face_values WHERE value_id = ?"
            cursor.execute(
                select_query, (f"{information['coin_prefix']}",)
            )  # Note the comma for single parameter tuple

            print("Fetched data:")
            temp = list(cursor)
            if temp or [x for x in added_values if information["coin_prefix"] == x]: # The value was found in the database or has been added
                matches = [int(x.split("_")[-1]) for x in added_coins if information["coin_prefix"] in x]
                if matches: # See if any added coins match
                    information['coin_number'] = max(matches) + 1
                else:
                    select_query = "SELECT coin_id FROM coins WHERE coin_id LIKE ?"
                    cursor.execute(
                        select_query, (f"{information['coin_prefix']}%",)
                    )  # Note the comma for single parameter tuple
                    temp = list(cursor)
                    if temp:
                        information['coin_number'] = int(temp[-1][0].split("_")[-1]) + 1# Gets count value at end of coin_id
            else: # No value found
                print("No data found")
                print("\nSelecting data...")
                select_query = "SELECT denomination_id FROM denominations WHERE denomination_id = ?"
                cursor.execute(
                    select_query, (f"{information['value_prefix']}",)
                )  # Note the comma for single parameter tuple

                print("Fetched data:")
                temp = list(cursor)
                if not temp and not [x for x in added_denominations if information["value_prefix"] == x]: # No denomination in database or added
                    print("No data found")
                    print("\nSelecting data...")
                    select_query = "SELECT country_id FROM countries WHERE country_id = ?"
                    cursor.execute(
                        select_query, (f"{information['denomination_prefix']}",)
                    )  # Note the comma for single parameter tuple

                    print("Fetched data:")
                    temp = list(cursor)
                    if not temp and not [x for x in added_countries if information["country_code"] == x]: # no country in database or added
                        addCountry(information)
                    addDenomination(information)
                addValue(information)
            addCoin(information)
            print("Enter a string of characters for what to edit: 'c'-country 'd'-denomination 'v'-value (empty string to continue).")
            print("'n'-coin name 'g'-gross weight 'f'-fineness 'p'-precious metal weight 'm'-metal type 'y'-years")
            response = input("'D' to discard last: ")
            if not response:
                break
            else:
                if 'c' in response:
                    information["country_code"] = None   
                    response += "dvngfpmy"
                if 'd' in response:
                    information["denomination_code"] = None
                    response += "vngfpmy"
                if 'v' in response:
                    information["value_code"] = None
                if 'n' in response:
                    information["nickname"] = None
                if 'g' in response:
                    information["gross_weight"] = None
                if 'f' in response:
                    information["fineness"] = None
                if 'p' in response:
                    information["precious_metal_weight"] = None
                if 'm' in response:
                    information["metal"] = None
                if 'y' in response:
                    information["years"] = None
                if 'D' in response: # Rollback latest updates
                    response += 'a'
                    queries_countries = copy_queries_countries
                    queries_denominations = copy_queries_denominations
                    queries_values = copy_queries_values
                    queries_coins = copy_queries_coins
                    added_countries = copy_added_countries
                    added_denominations = copy_added_denominations
                    added_values = copy_added_values
                    added_coins = copy_added_coins
                if 'a' in response:
                    for key in information:
                        information[key] = None


    except mariadb.Error as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    finally:
        # 4. Close Cursor and Connection
        if cursor:
            cursor.close()
            print("Cursor closed.")
        if conn:
            conn.close()
            print("Connection closed.")

    for item in [(queries_countries,"Countries"),(queries_denominations,"Denominations"),(queries_values,"Values"),(queries_coins,"Coins")]:
        if item[0]:
            print(f"-----{item[1]}-----")
            for query in item[0]:
                print(query)

    response = input("Append SQL to file? (y/n): ").lower()
    if response == 'y' or response == "yes":
        for item in [(queries_countries,countries_file),(queries_denominations,denominations_file),(queries_values,values_file),(queries_coins,coins_file)]:
            if item[0]:
                for entry in item[0]:
                    log(entry,item[1])
                    log(f"Writing '{entry}'\n  to file ({item[1]})")

