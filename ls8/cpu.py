"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256,
        self.reg = [0] * 8
        self.pc = 0
        self.FL = 0b00000000

    def load(self):
        self.ram = [0] * 256
        self.reg[7] = 0xF3
        address = 0
        if len(sys.argv) != 2:
            print('Add a file name to run')
            print(sys.stderr)
            sys.exit(1)

        try:
            with open(sys.argv[1]) as file:
                for line in file:
                    comment_split = line.split('#')
                    possible_number = comment_split[0]
                    if possible_number == '':
                        continue
                    first_bit = possible_number[0]
                    if first_bit == '1' or first_bit == '0':
                        op = possible_number[0:8]
                        int_op = int(op, 2)
                        self.ram_write(address, int_op)
                        address += 1
                        

        except:
            print('file not found')
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")
    
    def ram_read(self, index):
        return self.ram[index]

    def ram_write(self, index, value):
        self.ram[index] = value
        # return print(f'Ram at index {index} is now {self.ram[index]}')

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        running = True
        LDI = 0b0010
        MULT = 0b0010
        PRN = 0b0111
        PUSH = 0b0101
        POP = 0b0110
        CALL = 0b0000
        RET = 0b0001
        JMP = 0b0100
        CMP = 0b0111
        JEQ = 0b0101
        JNE = 0b0110
        while running:
            command = self.ram[self.pc]
            args = command >> 6
            alu = (command >> 5) & 0b00000001
            setPC = (command >> 4) & 0b00000001  
            op = command & 0b00001111

            if alu == 0:

                if setPC == 1:
                    if op == JMP:
                        register_address = self.ram[self.pc + 1]
                        address_to_jump_to = self.reg[register_address]
                        self.pc = address_to_jump_to

                    elif op == JEQ:
                        equals_flag = self.FL & 0b00000001
                        if equals_flag == 0b00000001:
                            register_address = self.ram[self.pc + 1]
                            address_to_jump_to = self.reg[register_address]
                            self.pc = address_to_jump_to
                        else:
                            self.pc += args + 1

                    elif op == JNE:
                        equals_flag = self.FL & 0b00000001
                        if equals_flag == 0b00000000:
                            register_address = self.ram[self.pc + 1]
                            address_to_jump_to = self.reg[register_address]
                            self.pc = address_to_jump_to
                        else:
                            self.pc += args + 1

                elif setPC == 0:
                    if op == LDI:
                        index = self.ram[self.pc + 1]
                        value = self.ram[self.pc + 2]

                        self.reg[index] = value
                        # print(f'R{index} is now {self.reg[index]}')

                        self.pc += 1 + args

                    elif op == PRN:
                        index = self.ram[self.pc + 1]

                        print(self.reg[index])

                        self.pc += 1 + args
                        
                    elif op == PUSH:
                        self.reg[7] = ( self.reg[7] -1 ) % 255
                        SP = self.reg[7]

                        reg_address = self.ram[self.pc + 1]
                        value = self.reg[reg_address]

                        self.ram[SP] = value
                        self.pc += 1 + args

                    elif op == POP:
                        SP = self.reg[7]

                        value = self.ram[SP]
                        reg_address = self.ram[self.pc + 1]
                        self.reg[reg_address] = value

                        self.reg[7] = ( SP + 1) % 255
                        self.pc += 1 + args

                    elif op == CALL:
                        register_address = self.ram[self.pc + 1]
                        address_to_jump_to = self.reg[register_address]

                        next_instruction = self.pc + 2
                        self.reg[7] = ( self.reg[7] - 1 ) % 255
                        SP = self.reg[7]
                        self.ram[SP] = next_instruction
                        self.pc = address_to_jump_to

                    elif op == RET:
                        SP = self.reg[7]
                        address_to_return_to = self.ram[SP]

                        self.reg[7] = ( SP + 1 ) % 255

                        self.pc = address_to_return_to

            elif alu == 1:
                if op == MULT:
                    index_1 = self.ram[self.pc + 1]
                    index_2 = self.ram[self.pc + 2]

                    num_1 = self.reg[index_1]
                    num_2 = self.reg[index_2]

                    print(num_1 * num_2)
                    
                    self.pc += 1 + args
                elif op == CMP:
                    reg_address_A = self.ram[self.pc + 1]
                    reg_address_B = self.ram[self.pc + 2]
                    regA = self.reg[reg_address_A]
                    regB = self.reg[reg_address_B]

                    if regA == regB:
                        self.FL = 0b00000001
                    elif regA > regB:
                        self.FL = 0b00000010
                    elif regA < regB:
                        self.FL = 0b00000100

                    self.pc += args + 1

            if command == 0b00000001:
                print('Halting program')
                running = False
            
            




