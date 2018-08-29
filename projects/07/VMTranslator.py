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
        if command_t in ['C_PUSH', 'C_POP', 'C_FUNCTION', 'C_CALL']:
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
        self.setStack()

    def setFileName(self, file_name):
        self.file_name = file_name
        self.file_object.close()
        self.file_object = open(file_name, "w")

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
            self.WritePushPop('C_PUSH', 0)
            emit_list = ["@" + label1, "0, JMP", "(" + label + ")", ]
            self.file_object.writelines("%s\n" % l for l in emit_list)
            self.WritePushPop('C_PUSH', -1)
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
            self.WritePushPop('C_PUSH', -1)
            emit_list = ["@" + label1, "0, JMP", "(" + label + ")", ]
            self.file_object.writelines("%s\n" % l for l in emit_list)
            self.WritePushPop('C_PUSH', 0)
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
            self.WritePushPop('C_PUSH', -1)
            emit_list = ["@" + label1, "0, JMP", "(" + label + ")", ]
            self.file_object.writelines("%s\n" % l for l in emit_list)
            self.WritePushPop('C_PUSH', 0)
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

    def WritePushPop(self, command, area, data):
        self.emit_comment(command, data)
        if command == 'C_PUSH':
            push_list = []
            if data > 1 or data < -1:
                push_list = ["@" + str(data), "D=A", "@SP", "A=M", "M=D"]
            else:
                push_list = ["@SP", "A=M", "M=" + str(data)]

            self.file_object.writelines("%s\n" % l for l in push_list)
            self.st_ptr += 1
            self.incStack()
            return 1
        elif command == 'C_POP':
            self.popStack()

    def setStack(self):
        init_list = ["@256", "D=A", "@0", "M=D"]
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

    def emit_comment(self, command, data):
        emit_str = "//" + command + " " + str(data) + "\n"
        self.file_object.writelines(emit_str)

    def close(self):
        self.file_object.close()


def test_answer():
    vm_obj = VMParse("./MemoryAccess/BasicTest/BasicTest.vm")
    code_writer = CodeWriter('MemoryAccess/BasicTest/BasicTest.asm')
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
    assert code_writer.WritePushPop('C_PUSH', 7) == 1
    code_writer.setFileName('testASM.asm')
    assert code_writer.file_object.name == 'testASM.asm'


def run():
    vm_obj = VMParse("./StackArithmetic/StackTest/StackTest.vm")
    code_writer = CodeWriter('./StackArithmetic/StackTest/StackTest.asm')
    #vm_obj = VMParse("./MemoryAccess/BasicTest/BasicTest.vm")
    #code_writer = CodeWriter('MemoryAccess/BasicTest/BasicTest.asm')
    while(vm_obj.hasMoreCommands()):
        vm_obj.advance()
        command_type = vm_obj.commandType()
        if command_type == 'C_ARTHIMETIC':
            arg1 = vm_obj.arg1()
            code_writer.emit_comment(arg1, -1)
            code_writer.writeArithmetic(arg1)
        else:
            arg3 = vm_obj.arg3()
            arg2 = vm_obj.arg2()
            arg1 = vm_obj.arg1()
            print(command_type, arg1, arg2, arg3)
            code_writer.WritePushPop(command_type, arg2, arg3)
    code_writer.close()


print("hello world")
run()
print("Run complete")
