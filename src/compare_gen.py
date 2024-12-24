import sys, os, time
from pathlib import Path
from os import path
# Change only if you plan to move the Dependencies folder, default sys.path: ../Dependencies/table_gen.py
sys.path.extend(['.', path.dirname(path.abspath(__file__))])
from Dependencies.table_gen import table_main

# Change based on chip, default file extension '.cmp'
FILE_NAME = 'Xor' + '.cmp'
# Change the name of the directory where you want to save the file
DIR_NAME = 'bin'

# Passes the paths to the table generator function, after adding potential additional paths
def write_file(logic_combination: list) -> int:
    dir_path = Path().absolute()

    # If directory was successfully created, adds new dir to the path
    if Path(DIR_NAME).exists():
        dir_path /= DIR_NAME

    file_path = dir_path / FILE_NAME
    # Calls external function to create/write the file
    return table_main(dir_path, file_path, logic_combination)

# Prompting for the creation of the folder where the file will be stored
def create_directory() -> int:
    prompt = input(r"Do you want to create a dir to store files? [y\n]: ").lower()

    match (prompt):
        case 'y' | '1':
            return directory_creation_handling(DIR_NAME)
        case 'n' | '0':
            print("Did not create a directory, proceeding...")
            time.sleep(0.2)
            return 1
        case _:
            print("Default input, directory created...")
            time.sleep(0.2)
            return directory_creation_handling(DIR_NAME)

# Error handling for the folder creation,
# To return, if successful, the name of the dir that will be created.
def directory_creation_handling(DIR_NAME: str) -> int:
    try:
        os.mkdir(DIR_NAME)
        print("Created a directory, proceeding...")
        return 0
    except FileExistsError:
        print(f"Directory already exists, proceeding...")
        return 0
    except PermissionError:
        print(f"Not enough permissions to create directory, proceeding...")
        return 1
    except Exception as error:
        print(f"An error occured when creating the directory: {error} ,proceeding...")
        return 1

# Takes the user input and converts it into an array,
# To make the work easier on the dependant file 'table_gen.py'
def combination_handling() -> list:
    logic_combination = input("Enter the combination, i.e. (ignore <>) <a NOT AND b NOT AND c>:\n")
    if len(logic_combination) == 0:
        sys.exit("Combination not valid, not enough arguments, exiting...")
    if any(char.isdigit() for char in logic_combination):
        time.sleep(0.1)
        sys.exit("Combination not valid, digit detected, exiting...")
        time.sleep(0.2)

    # Converting string to array, to return the array to an external function
    # Removing spaces, converting commas to spaces to remove them with list comprehension
    logic_combination = logic_combination.replace(',', '').upper().split(' ')
    logic_combination = [element for element in logic_combination if element != ' ' and element != '']
    return logic_combination

def main() -> None:
    create_directory()
    logic_combination = combination_handling()
    write_file(logic_combination)

# RUN THROUGH main()
if __name__ ==   "__main__":
	main()
