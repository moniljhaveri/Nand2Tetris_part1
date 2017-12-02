import glob, os 
import sys

def parse_file(line, first_pass): 

    if (line == "\n"): 
        pass
    elif "//" in line: 
       comm_split = line.split("//") 
       if len(comm_split[0]) != 0 : 
           first_pass.append(comm_split[0])
    else: 
        first_pass.append(line) 
    return first_pass

file_path = "/home/mjhaveri/develop/Nand2Tetris_part1/projects/06/add/Add.asm"
clean_input = []
with open(file_path, "r") as file:
    for line in file: 
        first_pass = parse_file(line, clean_input)