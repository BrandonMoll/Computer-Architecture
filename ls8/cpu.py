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


        # for i in range(len(program)):
        #     self.ram[i] = program[i]

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        prg_length = len(program)
        self.ram = [0] * prg_length

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")
    
    def ram_read(self, index):
        return print(self.reg[index])

    def ram_write(self, index, value):
        self.reg[index] = value
        return print(f'R{index} is now {self.reg[index]}')

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
        while running:
            command = self.ram[self.pc]

            if command == 0b10000010:
                self.ram_write(self.ram[self.pc+1], self.ram[self.pc+2])
                self.pc += 3
            if command == 0b01000111:
                self.ram_read(self.ram[self.pc+1])
                self.pc += 2
            if command == 0b00000001:
                print('Exiting Program')
                running = False
            
            




