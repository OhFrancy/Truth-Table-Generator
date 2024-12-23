import sys, os, string, time
from pathlib import Path
from os import path

class LogicGates:
    def NOT(truth_rows: list) -> list:
        output_rows = list()
        for row in truth_rows:
            output_rows.append(int(not truth_rows[row]))
        return output_rows

'''
    def AND(truth_rows: list) -> list:

    def NAND(truth_rows: list) -> list:

    def OR(truth_rows: list) -> list:

    def XOR(truth_rows: list) -> list:

    def NOR(truth_rows: list) -> list:

    def XNOR(truth_rows: list) -> list:

'''
LOGIC_GATES  = ['NOT','AND','NAND','OR','XOR','NOR','XNOR']
LOGIC_INPUTS = list(string.ascii_uppercase)

def table_gen(logic_combination: list) -> list:
    found_logic_gates = list()
    found_inputs      = list()

    # Passes all the gates to a new list,
    for gate in logic_combination:
        if gate in LOGIC_GATES:
            found_logic_gates.append(gate)
    if (len(found_logic_gates) == 0):
        print("Error: No logic gates found, cannot continue, exiting...")
        time.sleep(1)
        sys.exit()

    # Copies logic_combination list without logic gates to a new list
    input_combination = [input for input in logic_combination if input not in found_logic_gates]
    char_input_combination = [input for input in input_combination if len(input) == 1]

    # Passes all the inputs to a new list, filtering them if they are of length > 2,
    # To filter out the wrong ones, i.e.: 'ab' declared before a or b were declared
    first_index = 0
    last_saved_index = 0
    for input in input_combination:
        if (len(input) > 1):
            if (len(input) > len(char_input_combination)):
                sys.exit(rf"Error: Length of '{input.lower()}' is greater than amount of inputs.")
            else:
                before_double_input = [input_combination[i] for i in range(first_index, last_saved_index)]
                split_input = list(input)

                match_count = 0
                for i in range(0, len(split_input)):
                    if (split_input[i] == before_double_input[i]):
                        match_count += 1
                if (match_count == 0 or match_count == 1):
                    sys.exit(rf"Error: '{input.lower()}', declared before all inputs in it were declared.")
                else:
                    found_inputs.append(input)
                last_saved_index = 0
        if input in LOGIC_INPUTS:
            found_inputs.append(input)
            if last_saved_index == 0:
                first_index = logic_combination.index(input)
            last_saved_index += 1
    if (len(found_inputs) == 0):
        print("Error: No inputs found, cannot continue, exiting...")
        time.sleep(1)
        sys.exit()
    return table_validation(found_inputs, found_logic_gates, logic_combination)

def table_validation(found_inputs: list, found_logic_gates: list, logic_combination: list) -> list:
    gates_count = 0
    inputs_count = len(found_inputs)

    not_count = 0
    not_indexes = list()
    validated_combination = list()

    # Adds 1 for every input,
    # Adds 1 to not_count for every 'NOT' logic gate, and save the index,
    # adds 2 to gates_count for the first logic operation, else adds 1

    for gate in found_logic_gates:
        if (gate == 'NOT'):
            not_count += 1

            # Saves 'NOT' indexes to a new list, to re-add them after removing them
            not_index = logic_combination.index(gate)
            not_indexes.append(not_index)
            logic_combination[not_index] = None
        elif (gates_count == 0):
            gates_count += 2
        else:
            gates_count += 1

    # To not cause any errors in the next check,  if  the only gates are 'NOT',
    # assigns the inputs_count to the gates_count

    if (gates_count == 0 and (not_count > 1 or inputs_count > 1)):
        sys.exit("Error: Combination mismatching between counts of 'NOT' and logic gates")
    gates_count = inputs_count

    # Remove 'NOT's from found_logic_gates list temporarily with list comprehension,
    # To re-add them after the re-order
    found_logic_gates = [x for x in found_logic_gates if x != 'NOT']

    # Finally if the gates count and input counts correspond,
    # pass the final validated list to the output generator -> table_output,
    # preserving the order using a simple algorithm
    if (gates_count !=inputs_count):
        sys.exit("Error: Combination mismatching between inputs and logic gates")
    elif (gates_count < 2 and not_count == 1):
        validated_combination.append(found_inputs[0])
    else:
        for i in range(0, len(found_logic_gates)):
            if (len(found_logic_gates) == 1):
                validated_combination.extend([found_inputs[i], found_logic_gates[i], found_inputs[i + 1]])
            else:
                validated_combination.extend([found_inputs[i], found_logic_gates[i]])
                if (i == len(found_inputs) - 2):
                    validated_combination.append(found_inputs[i + 1])

    # Re-add the 'NOT's
    for index in not_indexes:
        validated_combination.insert(index, 'NOT')
    print(validated_combination)
    return #table_output(validated_combination, None, None)

#def table_output(logic_combination: list, first_binary_set: list, second_binary_set: list) -> list:


#def table_write(dir_path: str, file_path: str, truth_table_out: list) -> int:
    #with open(rf'{file_handler}','a') as file_handler:

def table_main(dir_path: str, file_path: str, logic_combination: list) -> int:
    truth_table_out = table_gen(logic_combination)
    return #table_write(dir_path, file_path, truth_table_out)

if __name__ == "__main__":
    sys.exit("This file is not runnable as a standalone, try to execute the main file (compare_gen.py)")
