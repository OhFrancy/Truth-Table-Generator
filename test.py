import time
def test_dict():
    found_inputs = ['a', 'b', 'c', 'd']

    stronk = dict()
    values_variable = list()
    for i in range(len(found_inputs)):
        wrong_tries = 0
        while True:
            tmpList = list(input(f"Enter the binary set for the '{found_inputs[i]}' input:\n"))
            tmpList = [int(x) for x in tmpList if x.isdigit()]
            if len(tmpList) != 4 or any(char != 1 and char != 0 for char in tmpList):
                print("Not valid binary set, retry...")
                wrong_tries += 1
                time.sleep(0.3)
            else:
                stronk[found_inputs[i]] = tmpList
                break
            if wrong_tries > 5:
                print(f"Error: Limit of 5 tries reached, setting set of {found_inputs[i]} as '0101'")
                stronk[found_inputs[i]] = [0,1,0,1]
                time.sleep(0.3)
    '''
    for i in range(2, found_inputs):
        try:
            stronk[found_inputs[i] =
        except Exception as error:
            print(rf"Error: {error}")

    truth_c = list(input("enter a value:\n"))
    for input in found_inputs:

    stronk = dict()
    write_file(stronk)
    '''
    print(stronk)
def write_file(out: dict) -> int:
    print(out)
    return 0

test_dict()


