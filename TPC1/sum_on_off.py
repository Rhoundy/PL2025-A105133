import sys
import itertools

on_off_combs = []
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def gen_combs(word):
    # Create a list of tuples, where each tuple contains the lowercase and uppercase of the character
    choices = [(char.lower(), char.upper()) for char in word]

    # Generate all possible combinations using itertools.product
    combinations = {''.join(combo) for combo in itertools.product(*choices)}

    return combinations

def sum_on_off(file):
    isOn = True
    on = 0
    with open(file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            i = 0
            while i < len(line):
                value = 0
                if line[i] == 'o' or line[i] == 'O':
                    cmdOn = line[i:i+2]
                    cmdOff = line[i:i+3]
                    if cmdOn in on_off_combs:
                            isOn = True
                            i += 2
                    elif cmdOff in on_off_combs:
                            isOn = False
                            i += 3
                    else:
                        i += 1
                elif line[i] in numbers and isOn:
                    while i < len(line) and line[i] in numbers:
                        value = value * 10 + int(line[i])
                        i += 1
                    on = on + value
                elif line[i] == '=':
                    print(f'Sum: {on}')
                    i += 1
                else:
                    i += 1


if __name__ == '__main__':
    file = sys.argv[1]
    on_off_combs = gen_combs('on')
    on_off_combs.update(gen_combs('off'))
    sum_on_off(file)