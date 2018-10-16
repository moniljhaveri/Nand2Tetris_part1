import os
import sys


class VMParse:
    def __init__(self, file_path):
        self.file_path = file_path
        self.inst_st = []
        self.n = 0
        self.parse()
        self.ind = -1
        self.current_command = ""
        self.command_ind = []
        # have to figure out logical commands but havent don it yet
        self.keyWordDict = {'push': 'C_PUSH', 'pop': 'C_POP', 'label': 'C_LABEL', 'goto': 'C_GOTO', 'if-goto': 'C_IF',
                            'function': 'C_FUNCTION', 'call': 'C_CALL', 'return': 'C_RETURN', 'add': 'C_ARTHIMETIC', 'sub': 'C_ARTHIMETIC', 'eq': 'C_ARTHIMETIC', 'lt': 'C_ARTHIMETIC', 'gt': 'C_ARTHIMETIC', 'neg': 'C_ARTHIMETIC', 'and': 'C_ARTHIMETIC', 'or': 'C_ARTHIMETIC', 'not': 'C_ARTHIMETIC'}
        self.command_type()
        self.st_ptr = 256

    def parse(self):
        with open(self.file_path) as file:
            #            read_data = file.read()
            self.inst_st = []
            for line in file:
                line_split = line.split("//")
                line_seg = line_split[0].replace("\n", "")
                if 0 < len(line_seg):
                    self.inst_st.append(line_seg)
        self.n = len(self.inst_st)

    def hasMoreCommands(self):
        if self.ind < self.n - 1:
            return True
        return False

    def advance(self):
        if self.hasMoreCommands():
            self.ind += 1
            self.current_command = self.inst_st[self.ind]

    def num_instr(self):
        return self.n

    def parse_instr(self, command):
        split_str = command.split()
        return self.keyWordDict[split_str[0]]

    def command_type(self):
        for i in self.inst_st:
            key_val_pair = {self.parse_instr(i): list(i.split())}
            self.command_ind.append(key_val_pair)

    def commandType(self):
        obj = list(self.command_ind[self.ind].keys())[0]
        return obj

    def arg1(self):
        obj = list(self.command_ind[self.ind].values())[0][0]
        return obj

    def arg2(self):
        command_t = self.commandType()
        if command_t in ['C_PUSH', 'C_POP', 'C_FUNCTION', 'C_CALL', 'C_LABEL', 'C_IF', 'C_GOTO']:
            return list(self.command_ind[self.ind].values())[0][1]
        return

    def arg3(self):
        command_t = self.commandType()
        if command_t in ['C_PUSH', 'C_POP', 'C_FUNCTION', 'C_CALL']:
            return int(list(self.command_ind[self.ind].values())[0][2])
        return


class CodeWriter:
    def __init__(self, file_name):
        self.file_name = file_name
        self.file_object = open(file_name, "w")
        self.st_ptr = 256
        self.label_num = 0
        # self.setStack()
        self.return_add = 0
        self.location = {'local': 'LCL', 'argument': 'ARG',
                         'this': 'THIS', 'that': 'THAT', 'temp': 'TEMP'}

    def writeInit(self):
        emit_list = ["@256", "D=A", "@SP", "M=D", "@0", "D=A", "@LCL", "M=-D"]
        #self.file_object.writelines("%s\n" % l for l in emit_list)
        emit_list = ["@0", "D=A", "@ARG", "M=-D", "@0", "D=A", "@THIS", "M=-D"]
        #self.file_object.writelines("%s\n" % l for l in emit_list)
        emit_list = ["@0", "D=A", "@THAT", "M=-D"]
        #self.file_object.writelines("%s\n" % l for l in emit_list)
        emit_list = ["@256", "D=A", "@SP", "M=D"]
        #self.file_object.writelines("%s\n" % l for l in emit_list)

    def writeLabel(self, label):
        emit_list = ['(' + label + ')']
        self.file_object.writelines("%s\n" % l for l in emit_list)

    def writeGoto(self, label):
        emit_list = ['@' + str(label), '0; JMP']
        self.file_object.writelines("%s\n" % l for l in emit_list)

    def writeIf(self, label):
        emit_list = ['@SP', 'M=M-1', 'A=M', 'D=M',
                     '@' + str(label), 'D; JNE']
        self.file_object.writelines("%s\n" % l for l in emit_list)

    def writeCall(self, functionName, numArgs):
        self.emit_comment('C_CALL', functionName, numArgs)
        returnLabel = "ret_lab$" + str(self.label_num)
        emit_list = ["@" + returnLabel, "D=A", "@SP", "A=M", "M=D"]
        self.file_object.writelines("%s\n" % l for l in emit_list)
        self.incStack()
        emit_list = [ "@LCL", "D=A", "@SP", "A=M", "M=D"]
        self.file_object.writelines("%s\n" % l for l in emit_list)
        self.incStack()
        emit_list = ["@ARG", "D=A", "@SP","A=M", "M=D"]
        self.file_object.writelines("%s\n" % l for l in emit_list)
        self.incStack()
        emit_list = ["@THIS", "D=A", "@SP","A=M", "M=D"]
        self.file_object.writelines("%s\n" % l for l in emit_list)
        self.incStack()
        emit_list = ["@THAT", "D=A", "@SP","A=M", "M=D"]
        self.file_object.writelines("%s\n" % l for l in emit_list)
        self.incStack()
        #emit_list = ["@SP", "D=A", "@" + str(numArgs), "D=D-A", "@5", "D=D-A", "@ARG", "M=D",
        #             "@SP", "D=A", "@LCL", "M=D", "@" + functionName, "0;JMP", "(" + returnLabel + ")"]
        emit_list = ["@SP", "D=M", "@5", "D=D-A", "@"+str(numArgs), "D=D-A"]
        self.file_object.writelines("%s\n" % l for l in emit_list)
        emit_list = ["@SP", "D=M", "@LCL", "M=D"]
        self.file_object.writelines("%s\n" % l for l in emit_list)
        emit_list = ["@"+functionName, "0;JMP", "(" + returnLabel + ")" ]
        self.file_object.writelines("%s\n" % l for l in emit_list)
        self.label_num += 1

    def writeReturn(self, label):
        self.emit_comment(label, label, -1)
        Frame = ["@LCL", "D=M", "@R13", "M=D"]
        self.file_object.writelines("%s\n" % l for l in Frame)
        Ret = ["@5", "D=D-A", "A=D", "D=M", "@R14", "M=D"]
        self.file_object.writelines("%s\n" % l for l in Ret)
        s_Arg = ["@SP", "M=M-1", "A=M", "D=M",
                 "@SP", "M=M-1", "@ARG", "A=M", "M=D"]
        self.file_object.writelines("%s\n" % l for l in s_Arg)
        SP = ["@ARG", "D=M", "D=D+1", "@SP", "M=D"]
        self.file_object.writelines("%s\n" % l for l in SP)
        THAT = ["@R13", "D=M", "@1", "D=D-A", "A=D", "D=M", "@THAT", "M=D"]
        self.file_object.writelines("%s\n" % l for l in THAT)
        THIS = ["@R13", "D=M", "@2", "D=D-A", "A=D", "D=M", "@THIS", "M=D"]
        self.file_object.writelines("%s\n" % l for l in THIS)
        ARG = ["@R13", "D=M", "@3", "D=D-A", "A=D", "D=M", "@ARG", "M=D"]
        self.file_object.writelines("%s\n" % l for l in ARG)
        LCL = ["@R13", "D=M", "@4", "D=D-A", "A=D", "D=M", "@LCL", "M=D"]
        self.file_object.writelines("%s\n" % l for l in LCL)
        GOTO = ["@R14", "A=M", "0; JMP"]
        self.file_object.writelines("%s\n" % l for l in GOTO)

    def writeFunction(self, label, numLocals):
        self.emit_comment(label, label, -1)
        emit_list = ["(" + label + ")"]
        self.file_object.writelines("%s\n" % l for l in emit_list)
        for i in range(numLocals):
            self.WritePushPop('C_PUSH', 'constant', 0)

    def setFileName(self, file_name):
        self.file_name = file_name
        self.file_object.close()
        self.file_object = open(file_name, "w")

    def parseFileName(self):
        tmp = self.file_name.split('.')
        tmp1 = tmp[0].split('/')[-1]
        return tmp1

    def writeArithmetic(self, operator):
        if operator == 'add':
            self.popStack()
            emit_list = ["A=M", "D=M+D", "@0", "A=M", "M=D"]
            self.file_object.writelines("%s\n" % l for l in emit_list)
            self.incStack()
        elif operator == 'sub':
            self.popStack()
            emit_list = ["A=M", "D=M-D", "@0", "A=M", "M=D"]
            self.file_object.writelines("%s\n" % l for l in emit_list)
            self.incStack()
        elif operator == 'eq':
            label = "label" + str(self.label_num)
            self.label_num += 1
            label1 = "label" + str(self.label_num)
            self.popStack()
            emit_list = ["A=M", "D=D-M", "@" + label, "D, JEQ", "@" + label1]
            self.file_object.writelines("%s\n" % l for l in emit_list)
            self.WritePushPop('C_PUSH', 'constant', 0)
            emit_list = ["@" + label1, "0, JMP", "(" + label + ")", ]
            self.file_object.writelines("%s\n" % l for l in emit_list)
            self.WritePushPop('C_PUSH', 'constant', -1)
            emit_list = ["(" + label1 + ")", ]
            self.label_num += 1
            self.file_object.writelines("%s\n" % l for l in emit_list)
        elif operator == 'lt':
            label = "label" + str(self.label_num)
            self.label_num += 1
            label1 = "label" + str(self.label_num)
            self.popStack()
            emit_list = ["A=M", "D=D-M", "@" + label, "D, JLE", "@" + label1]
            self.file_object.writelines("%s\n" % l for l in emit_list)
            self.WritePushPop('C_PUSH', 'constant', -1)
            emit_list = ["@" + label1, "0, JMP", "(" + label + ")", ]
            self.file_object.writelines("%s\n" % l for l in emit_list)
            self.WritePushPop('C_PUSH', 'constant', 0)
            emit_list = ["(" + label1 + ")", ]
            self.file_object.writelines("%s\n" % l for l in emit_list)
            self.label_num += 1
        elif operator == 'gt':
            label = "label" + str(self.label_num)
            self.label_num += 1
            label1 = "label" + str(self.label_num)
            self.popStack()
            emit_list = ["A=M", "D=D-M", "@" + label, "D, JGE", "@" + label1]
            self.file_object.writelines("%s\n" % l for l in emit_list)
            self.WritePushPop('C_PUSH', 'constant', -1)
            emit_list = ["@" + label1, "0, JMP", "(" + label + ")", ]
            self.file_object.writelines("%s\n" % l for l in emit_list)
            self.WritePushPop('C_PUSH', 'constant', 0)
            emit_list = ["(" + label1 + ")", ]
            self.file_object.writelines("%s\n" % l for l in emit_list)
            self.label_num += 1
        elif operator == 'neg':
            emit_list = ["@0", "M=M-1", "A=M",
                         "D=M", "D=-D", "@0", "A=M", "M=D"]
            self.file_object.writelines("%s\n" % l for l in emit_list)
            self.incStack()
        elif operator == 'not':
            emit_list = ["@0", "M=M-1", "A=M",
                         "D=M", "D=!D", "@0", "A=M", "M=D"]
            self.file_object.writelines("%s\n" % l for l in emit_list)
            self.incStack()
        elif operator == 'and':
            self.popStack()
            emit_list = ["A=M", "D=M&D", "@0", "A=M", "M=D"]
            self.file_object.writelines("%s\n" % l for l in emit_list)
            self.incStack()
        elif operator == 'or':
            self.popStack()
            emit_list = ["A=M", "D=M|D", "@0", "A=M", "M=D"]
            self.file_object.writelines("%s\n" % l for l in emit_list)
            self.incStack()
        else:
            print(operator)

    def WritePushPop(self, command, arg, data):
        self.emit_comment(command, arg, data)
        if (command == 'C_PUSH') and (arg == 'constant'):
            push_list = []
            if data > 1 or data < -1:
                push_list = ["@" + str(data), "D=A", "@SP", "A=M", "M=D"]
            else:
                push_list = ["@SP", "A=M", "M=" + str(data)]

            self.file_object.writelines("%s\n" % l for l in push_list)
            self.st_ptr += 1
            self.incStack()
            return 1
        elif (command == 'C_PUSH') and (arg == 'pointer'):
            tmp = ''
            if data:
                tmp = 'THAT'
            else:
                tmp = 'THIS'
            emit_list = ['@' + tmp, 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1']
            self.file_object.writelines("%s\n" % l for l in emit_list)
            return 3
        elif (command == 'C_PUSH') and (arg == 'static'):
            name = '@' + self.parseFileName() + '.' + str(data)
            emit_list = [name, 'D=M', '@SP', 'A=M', 'M=D']
            self.file_object.writelines("%s\n" % l for l in emit_list)
            self.incStack()
            return 4
        elif (command == 'C_POP') and (arg == 'static'):
            name = '@' + self.parseFileName() + '.' + str(data)
            emit_list = ['@SP', 'M=M-1', 'A=M', 'D=M', name, 'M=D']
            self.file_object.writelines("%s\n" % l for l in emit_list)
            return -4
        elif (command == 'C_POP') and (arg == 'pointer'):
            tmp = ''
            if data:
                tmp = 'THAT'
            else:
                tmp = 'THIS'
            emit_list = ['@SP', 'M=M-1', 'A=M', 'D=M', '@' + tmp, 'M=D']
            self.file_object.writelines("%s\n" % l for l in emit_list)
            return -3
        elif(command == 'C_PUSH') and (arg != 'constant'):
            emit_list = ['@' + self.location[arg], 'D=M', '@' +
                         str(data), 'D=A+D', 'A=D', 'D=M', '@SP', 'A=M', 'M=D']
            self.file_object.writelines("%s\n" % l for l in emit_list)
            self.incStack()
            return 2
        elif(command == 'C_POP') and (arg != 'constant'):
            emit_list = ['@' + self.location[arg], 'D=M', '@' + str(
                data), 'D=D+A', '@' + self.location[arg], 'M=D', '@SP', 'M=M-1', 'A=M', 'D=M', '@' + self.location[arg], 'A=M', 'M=D', '@' + self.location[arg], 'D=M', '@' + str(data), 'D=D-A', '@' + self.location[arg], 'M=D']
            self.file_object.writelines("%s\n" % l for l in emit_list)
            return -2
        elif command == 'C_POP':
            self.popStack()
            return -1
        elif command == 'C_LABEL':
            self.writeLabel(arg)
            return 5
        elif command == 'C_IF':
            self.writeIf(arg)
        elif command == 'C_GOTO':
            self.writeGoto(arg)

    def setStack(self):
        init_list = ["@256", "D=A", "@0", "M=D", "@5", 'D=A', '@TEMP', 'M=D']
        self.file_object.writelines("%s\n" % l for l in init_list)

    def incStack(self):
        self.st_ptr += 1
        inc_list = ["@0", "M=M+1"]
        self.file_object.writelines("%s\n" % l for l in inc_list)

    def popStack(self):
        self.st_ptr -= 1
        dec_list = ["@0", "M=M-1", "A=M", "D=M", "@0", "M=M-1"]
        self.file_object.writelines("%s\n" % l for l in dec_list)

    def return_pointer(self):
        return ["@pointer", "A=M", "D=M"]

    def emit_comment(self, command, arg, data):
        if (arg == None):
            arg = ""
        if (data == None):
            data = ""
        emit_str = "//" + command + " " + arg + " " + str(data) + "\n"
        self.file_object.writelines(emit_str)

    def close(self):
        self.file_object.close()


def test_answer():
    vm_obj = VMParse("./MemoryAccess/StaticTest/StaticTest.vm")
    code_writer = CodeWriter('MemoryAccess/StaticTest/StaticTest.asm')
    assert vm_obj.num_instr() == 3
    vm_obj.ind += 5
    assert vm_obj.hasMoreCommands() == False
    vm_obj.ind = 0
    assert vm_obj.hasMoreCommands() == True
    vm_obj.ind = -1
    assert vm_obj.ind == -1
    vm_obj.advance()
    assert vm_obj.ind == 0
    vm_obj.ind = 0
    assert vm_obj.commandType() == 'C_PUSH'
    vm_obj.ind = 1
    assert vm_obj.commandType() == 'C_PUSH'
    vm_obj.ind = 2
    assert vm_obj.commandType() == 'C_ARTHIMETIC'
    assert vm_obj.arg1() == 'add'
    assert vm_obj.arg2() == None
    vm_obj.ind = 1
    assert vm_obj.arg1() == 'push'
    assert vm_obj.arg2() == 8
    vm_obj.ind = 0
    assert vm_obj.arg1() == 'push'
    assert vm_obj.arg2() == 7
    assert code_writer.file_object.name == 'SimpleAdd.asm'
    assert code_writer.WritePushPop('C_PUSH', 'constant', 7) == 1
    code_writer.setFileName('testASM.asm')
    assert code_writer.file_object.name == 'testASM.asm'


def run(fileName, flag=False, newFileName=""):
    # vm_obj = VMParse("./StackArithmetic/StackTest/StackTest.vm")
    # code_writer = CodeWriter('./StackArithmetic/StackTest/StackTest.asm')
    # vm_obj = VMParse("./MemoryAccess/BasicTest/BasicTest.vm")
    # code_writer = CodeWriter('MemoryAccess/BasicTest/BasicTest.asm')
    fileAsm = fileName.split('.')[0] + '.asm'
    newFileASM = newFileName + \
        newFileName.split("/")[len(newFileName.split("/")) - 2] + ".asm"
    vm_obj = VMParse(fileName)
    code_writer = CodeWriter(fileAsm)
    if flag:
        print('monil', newFileASM)
        code_writer.setFileName(newFileASM)
        code_writer.writeInit()
    while(vm_obj.hasMoreCommands()):
        vm_obj.advance()
        command_type = vm_obj.commandType()
        if command_type == 'C_ARTHIMETIC':
            arg1 = vm_obj.arg1()
            print(command_type, arg1)
            code_writer.emit_comment(arg1, str(-1), -1)
            code_writer.writeArithmetic(arg1)
        elif command_type == 'C_FUNCTION':
            arg1 = vm_obj.arg1()
            arg2 = vm_obj.arg2()
            arg3 = vm_obj.arg3()
            print(command_type, arg1, arg2, arg3)
            code_writer.emit_comment(arg1, arg2, arg3)
            code_writer.writeFunction(arg2, arg3)
        elif command_type == 'C_RETURN':
            arg3 = vm_obj.arg3()
            arg2 = vm_obj.arg2()
            arg1 = vm_obj.arg1()
            print(command_type, arg1, arg2, arg3)
            code_writer.writeReturn(arg1)
        elif command_type == 'C_CALL':
            arg3 = vm_obj.arg3()
            arg2 = vm_obj.arg2()
            arg1 = vm_obj.arg1()
            print(command_type, arg1, arg2, arg3)
            code_writer.writeCall(arg2, arg3)
        else:
            arg3 = vm_obj.arg3()
            arg2 = vm_obj.arg2()
            arg1 = vm_obj.arg1()
            print(command_type, arg1, arg2, arg3)
            code_writer.WritePushPop(command_type, arg2, arg3)
    code_writer.close()


file = sys.argv[1]
if os.path.isdir(file):
    vm_files = [file + i for i in os.listdir(file) if '.vm' in i]
    print(vm_files)
    for i in vm_files:
        run(i, True, file)
else:
    run(file)
print("Run complete")
