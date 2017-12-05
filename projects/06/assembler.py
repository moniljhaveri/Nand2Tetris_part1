import glob, os 
import sys
from enum import Enum

class Command(Enum): 
    A_COMMAND = 0 
    C_COMMAND = 1 
    L_COMMAND = 2 


class Assembler: 
    def __init__(self, file_path): 
        self.Dest = { 
         "Null" : "000",
         "M" : "001",
         "D" : "010",
         "MD" : "011",
         "A" : "100",
         "AM" : "101",
         "AD" : "110",
         "AMD" : "111"
        }
        self.Jump = {
         "Null" : "000", 
         "JGT" : "001",
         "JEQ" : "010",
         "JGE" : "011",
         "JLT" : "100",
         "JNE" : "101",
         "JLE" : "110",
         "JMP" : "111"
        }

        self.Comp = {
         "0" : "0101010",
         "1" : "0111111",
         "-1": "0111010",
         "D" : "0001100",
         "A" : "0110000",
         "!D": "0001101",
         "-D": "0001111",
         "-A": "0110011",
         "D+1": "0011111",
         "A+1": "0110111", 
         "A-1": "0110010", 
         "D+A": "0000010",
         "D-A": "0010011", 
         "A-D": "0000111", 
         "D&A": "0000000", 
         "D|A": "0010101", 
         "M" : "1110000",
         "!M": "1110001", 
         "-M": "1110011", 
         "M+1": "1110111",
         "M-1": "1110010",
         "D+M": "1000010",
         "D-M": "1010011",
         "M-D": "1000111",
         "D&M": "1000000",
         "D|M": "1010101"
        }

        self.file_path = file_path
        self.hack_code = []
        self.commands = [] 
        self.commands = self.open_file()
        self.symbol_table = {}
        self.parser()
        self.save_hack_code()

    def open_file(self): 
        # opens the file and reads in the lines 
        with open(self.file_path, "r") as file: 
            for line in file: 
                self.commands = self.clean_file(line, self.commands)
        return self.commands

    def clean_file(self, line, first_pass): 
        # cleans the incoming lines 
        if (line == "\n"): 
            pass
        elif "//" in line: 
            comm_split = line.split("//") 
            if len(comm_split[0]) != 0 : 
                first_pass.append(comm_split[0])
        else: 
            first_pass.append(line.splitlines()[0]) 
        return first_pass

    def command_type(self, line): 
        # returns the command type 
        if(line[0] == '('): 
            return Command.L_COMMAND
        elif(line[0] == '@'): 
            return Command.A_COMMAND
        else:
            return Command.C_COMMAND

    def parser(self): 
        # parses the commands 
        for i in self.commands: 
            command_type = self.command_type(i)
            if command_type == Command.A_COMMAND:
                symbol = self.symbol_parser(i)
                a_binary = self.a_parser(symbol)
                self.add_hack_code(a_binary)
            elif command_type == Command.C_COMMAND: 
                jump = self.jump_parser(i)
                comp = self.comp_parser(i)
                dest = self.dest_parser(i)
                c_binary = "111" + comp + dest + jump
                self.add_hack_code(c_binary)
            else: 
                symbol = self.symbol_parser(i)
    
    def symbol_parser(self, line): 
        # parsers line for the symbol 
        new_line = line.strip("()@")
        return new_line

    def dest_parser(self, line): 
        # parsers line for the dest
        if "=" not in line: 
            return self.Dest["Null"]
        else: 
            split_line = line.split("=")
            return self.Dest[split_line[0]]

    def jump_parser(self, line): 
        # parses line for the jump
        if ";" not in line: 
            return self.Jump["Null"]
        else: 
            split_line = line.split(";")
            return self.Jump[split_line[1]]

    def comp_parser(self, line): 
        # parses line for the comp
        split_line = line.split("=")
        comp=split_line[1]
        return self.Comp[comp]

    def a_parser(self, line): 
        # parses line for the a_instructions 
        return self.decimal_to_binary(line)

    def decimal_to_binary(self, line): 
        # converts decimal to binary 
        num = int(line)
        ind = []
        while(num):  
            remainder = num%2
            ind.append(remainder)
            num = num>>1 
        len_ind = len(ind)
        while(16 - len_ind): 
            ind.append("0")
            len_ind = len(ind)
        ind.reverse()
        con_string = "".join((str(i) for i in ind)) 
        return con_string

    def add_hack_code(self, code): 
        # adds converted code to hack code 
        self.hack_code.append(code)
    
    def save_hack_code(self): 
        # saves the hack code 
        file_name = self.file_path.split(".")[0] + ".hack"
        with open(file_name, "w+") as file:
            for i in self.hack_code: 
                file.write(i + "\n")


def main(): 
    num_args = len(sys.argv)
    if num_args < 2: 
        print("Need to have an input file to run a program")
        return 
    else: 
        file_path = str(sys.argv[1])
        a = Assembler(file_path)
    return 

if __name__ == "__main__": 
    main() 