import sys

PRINT_TIM = 1
HALT  = 2
PRINT_NUM = 3
PRINT_SUM = 4
SAVE = 5
ADD = 6
PUSH = 7
POP = 8

ram = [0] * 256
registers = [0] * 8 # [0, 0, 0, 0, 0, 0, 0, 0]

PC = 0
running = True

registers[7] = 255 # SP, in cpu.py F3

def load_memory(filename):
    address = 0
    try:
        with open(filename) as file:
            for line in file:
                comment_split = line.split('#')
                possible_number = comment_split[0]

                if possible_number == '' or possible_number == '\n':
                    continue
                instruction = int( possible_number)
                ram[address] = instruction
                address += 1

    except IOError:  #FileNotFoundError
        print('I cannot find that file, check the name')
        sys.exit(2)

program = [
    PRINT_TIM,
    PRINT_NUM,
    99,
    SAVE,
    2,
    99,
]

load_memory(sys.argv[1])

while running:
    command = ram[PC]

    if command == PRINT_TIM:
        print('Tim!')
        PC += 1

    elif command == PRINT_NUM:
        num = ram[PC + 1]
        print(num)
        PC += 2

    elif command == PRINT_SUM:
        first_number = ram[PC + 1]
        second_number = ram[PC + 2]
        print(first_number + second_number)
        PC += 3

    elif command == SAVE:
        register = ram[PC + 1]
        number_to_save = ram[PC + 2]
        registers[register] = number_to_save
        PC += 3

    elif command == ADD:
        first_register = ram[PC + 1]
        second_register = ram[PC + 2]
        sum = registers[first_register] + registers[second_register]
        registers[first_register] = sum
        PC += 3

    elif command == PUSH:
        # registers[7] = ( registers[7] - 1 ) % 255
        SP = registers[7]
        registers[7] = ( SP - 1 ) % 255

        register_address = ram[PC + 1]
        value = registers[register_address]

        ram[SP] = value
        PC += 2

    elif command == POP:
        SP = registers[7]

        value = ram[SP]
        register_address = ram[PC + 1]
        registers[register_address] = value

        # registers[7] += 1
        registers[7] = ( SP + 1 ) % 255
        
        PC += 24
        
    elif command == HALT:
        running = False

    else:
        print('command not recognized: {}'.format(command))
        running = False