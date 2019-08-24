"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self, ram = [0] * 256, reg = [0] * 8, pc = 0):
        """Construct a new CPU."""
        self.ram = ram,
        self.reg = reg
        self.pc = pc

    def load(self):
        self.ram = [0] * 256
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
        return print(f'Ram at index {index} is now {self.ram[index]}')

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
        LDI = 0b10
        MULT = 0b10
        PRN = 0b0111
        while running:
            command = self.ram[self.pc]
            args = command >> 6
            alu = (command >> 5) & 0b00000001  
            op = command & 0b00001111

            if alu == 0:
                if op == LDI:
                    self.reg[self.ram[self.pc+1]] = self.ram[self.pc + 2]
                    print(f'R{self.ram[self.pc+1]} is now {self.ram[self.pc + 2]}')
                    self.pc += 1 + args
                elif op == PRN:
                    print(self.reg[self.ram[self.pc + 1]])
                    self.pc += 1 + args
            elif alu == 1:
                if op == MULT:
                    num_1 = self.ram[self.pc + 1]
                    num_2 = self.ram[self.pc + 2]
                    print(num_1 * num_2)
                    self.pc += 1 + args
                

            if command == 0b00000001:
                print('Halting program')
                running = False
            elif self.pc > 14:
                print('Exiting with self pc')
                running = False
            
            




