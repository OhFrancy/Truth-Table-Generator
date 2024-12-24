import sys, string, time
from pathlib import Path

class LogicGates:
    def NOT(input_table: list) -> list:
        output_table = [int(not input) for input in input_table]
        return output_table
        
    def AND(first_input_table: list, second_input_table) -> list:
        for i, j in zip(first_input_table, second_input_table):
            output_table.append(int(i == 1 and j == 1))
        return output_table
'''
    def NAND(first_input_table: list, second_input_table) -> list:

        return output_table

    def OR(first_input_table: list, second_input_table) -> list:

        return output_table

    def XOR(first_input_table: list, second_input_table) -> list:

        return output_table

    def NOR(first_input_table: list, second_input_table) -> list:

        return output_table

    def XNOR(first_input_table: list, second_input_table) -> list:

        return output_table
'''
LOGIC_GATES  = ['NOT','AND','NAND','OR','XOR','NOR','XNOR']
LOGIC_INPUTS = list(string.ascii_uppercase)

def table_gen(logic_combination: list) -> dict:
    # Copies all the gates that are in LOGIC_GATES to a new list
    found_logic_gates = [gate for gate in logic_combination if gate in LOGIC_GATES]
    if len(found_logic_gates) == 0:
        print("Error: No logic gates found, cannot continue, exiting...")
        time.sleep(1)
        sys.exit()

    found_inputs = list()
    # Copies logic_combination list without logic gates to a new list
    input_combination = [input for input in logic_combination if input not in found_logic_gates]
    # Copies all the inputs of length 1 to a new list, to use it for the filtering
    char_input_combination = [input for input in input_combination if len(input) == 1]

    # Passes all the inputs to a new list, filtering them if they are of length > 2,
    # To filter out the wrong ones, i.e.: 'ab' declared before a or b were declared
    first_index = 0
    last_saved_index = 0
    for input in input_combination:
        if len(input) > 1:
            if len(input) > len(char_input_combination):
                sys.exit(rf"Error: Length of '{input.lower()}' is greater than amount of inputs.")
            else:
                # Copies all the inputs before the input of length 2, i.e. 'a AND b AND ab' --> ['a','b']
                before_double_input = [input_combination[i] for i in range(first_index, last_saved_index)]

                # Checks if there were 2 inputs with length > 1, if they are not equal, throw an error,
                # As they can't be valid if they are not equal
                if len(before_double_input) == 0:
                    if list(input) != split_input:
                        sys.exit(rf"Error: '{input.lower()}', declared right after '{''.join(split_input).lower()} was declared, without any other inputs to make it valid.")
                        time.sleep(0.7)
                    else:
                        last_saved_index += len(list(input))
                split_input = before_double_input = list(input)

                # Adds 1 to match_count for every match,
                # To check if the len > 1 input is valid, throws an error otherwise
                match_count = sum(i == di for i, di in zip(split_input, before_double_input))
                if match_count < 2:
                    sys.exit(rf"Error: '{input.lower()}', declared before all inputs in it were declared.")
                    time.sleep(0.7)

                found_inputs.append(input)
                last_saved_index = 0
        if input in LOGIC_INPUTS:
            found_inputs.append(input)
            # Saves the index of the first input of length 1 and the last one found,
            # Back to 0 when an input of length 2 is found
            if last_saved_index == 0:
                first_index = input_combination.index(input)
            last_saved_index += 1
    if len(found_inputs) == 0:
        print("Error: No inputs found, cannot continue, exiting...")
        time.sleep(0.6)
        sys.exit()
    return table_validation(found_inputs, found_logic_gates, logic_combination)

def table_validation(found_inputs: list, found_logic_gates: list, logic_combination: list) -> dict:
    gates_count = 0
    inputs_count = len(found_inputs)
    validated_combination = list()

    # Adds 1 for every input,
    # Adds 1 to not_count for every 'NOT' logic gate, and saves the index,
    # adds 2 to gates_count for the first logic operation, else adds 1
    not_count = 0
    not_indexes = list()
    for gate in found_logic_gates:
        if gate == 'NOT':
            not_count += 1

            # Saves 'NOT' indexes to a new list, and swaps the found ones with 'None',
            # to not change the pointer position and save the correct indexes,
            not_index = logic_combination.index(gate)
            not_indexes.append(not_index)
            logic_combination[not_index] = None
        elif (gates_count == 0):
            gates_count += 2
        else:
            gates_count += 1

    # To not cause any errors in the next check, if  the only gates are 'NOT',
    # assigns the inputs_count to the gates_count
    if (gates_count == 0 and (not_count > 1 or inputs_count > 1)):
        sys.exit("Error: Combination mismatching between counts of 'NOT' and logic gates")
    elif (gates_count == 0 and not_count <= inputs_count):
        gates_count = inputs_count

    # Remove 'NOT's by creating a list temporarily with list comprehension,
    # To re-add them after the re-order
    removed_not_logic_gates = [gate for gate in found_logic_gates if gate != 'NOT']

    # Finally if the gates count and input counts correspond,
    # pass the final validated list to the input_dictionary generator -> table_output,
    # preserving the order using a simple algorithm
    if gates_count != inputs_count:
        sys.exit("Error: Combination mismatching between inputs and logic gates")
    elif gates_count < 2 and not_count == 1:
        validated_combination.append(found_inputs[0])
    else:
        for i in range(len(removed_not_logic_gates)):
            if len(removed_not_logic_gates) == 1:
                validated_combination.extend([found_inputs[i], removed_not_logic_gates[i], found_inputs[i + 1]])
            else:
                validated_combination.extend([found_inputs[i], removed_not_logic_gates[i]])
                # Adds remaining input at the end
                if (i == len(found_inputs) - 2):
                    validated_combination.append(found_inputs[i + 1])

    # Re-add the 'NOT's
    for index in not_indexes:
        validated_combination.insert(index, 'NOT')
    return input_dictionary_gen(validated_combination, found_inputs, found_logic_gates)

def input_dictionary_gen(logic_combination: list, found_inputs: list, found_logic_gates: list) -> dict:
    input_dictionary = dict()
    for i in range(len(found_inputs)):
        wrong_tries = 0
        while True:
            tmpList = list(input(f"Enter the binary set for the '{found_inputs[i].lower()}' input:\n"))
            tmpList = [int(x) for x in tmpList if x.isdigit()]
            if len(tmpList) != 4 or any(char != 1 and char != 0 for char in tmpList):
                print("Not valid binary set, retry...")
                wrong_tries += 1
                time.sleep(0.3)
            else:
                input_dictionary[found_inputs[i].lower()] = tmpList
                break
            if wrong_tries > 5:
                print(f"Error: Limit of 5 tries reached, setting set of {found_inputs[i].lower()} as '0101'")
                input_dictionary[found_inputs[i]] = [0,1,0,1]
                time.sleep(0.3)
                break

    return output_dictionary_gen(input_dictionary, logic_combination, found_inputs, found_logic_gates)

def output_dictionary_gen(output_dictionary: dict, logic_combination: list, inputs: list, logic_gates: list) -> dict:
    input_indexes = [logic_combination.index(input) for input in logic_combination if input in inputs]
    is_before = -1
    for i in input_indexes:
        logic_combination.append(None)
        if logic_combination[i - 1] == 'NOT':
            is_before = 2
        elif logic_combination[i + 1] == 'NOT':
            is_before = 0
        if is_before != -1:
            output_dictionary[logic_combination[i].lower()] = getattr(LogicGates, 'NOT')(output_dictionary[logic_combination[i].lower()])
            logic_combination[i + 1 - is_before] = None

    print(output_dictionary)
#def table_write(dir_path: str, file_path: str, input_dictionary: dict):
    #with open(rf'{file_handler}','a') as file_handler:

def table_main(dir_path: str, file_path: list, logic_combination: list) -> int:
    output_dictionary = table_gen(logic_combination)
    return #table_write(dir_path, file_path, output_dictionary)

# TO NOT RUN AS A STANDALONE
if __name__ == "__main__":
    sys.exit("This file is not runnable as a standalone, try to execute the main file (compare_gen.py)")
