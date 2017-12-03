import glob, os 
import sys

class Assembler: 
    def __init__(self, file_path): 
        self.file_path = file_path
        self.commands = [] 
        self.command = self.open_file()
        self.symbol_table = {}
    
    def open_file(self): 
        with open(self.file_path, "r") as file: 
            for line in file: 
                self.commands = self.parse_file(line, self.commands)
        print(self.commands)

    def parse_file(self, line, first_pass): 
        if (line == "\n"): 
            pass
        elif "//" in line: 
            comm_split = line.split("//") 
            if len(comm_split[0]) != 0 : 
                first_pass.append(comm_split[0])
        else: 
            first_pass.append(line.splitlines()[0]) 
        return first_pass


def main(): 
    num_args = len(sys.argv)
    if num_args < 2: 
        print("Need to have an input file to run a program")
        return 
    else: 
        file_path = str(sys.argv[1])
        a = Assembler(file_path)
    #with open(file_path, "r") as file:
    #    for line in file: 
        #clean_input = parse_file(line, clean_input)
    return 

if __name__ == "__main__": 
    main() 