class VMParse:
    def __init__(self, file_path):
        self.file_path = file_path
        self.inst_st = []
        self.n = 0
        self.parse()
        self.ind = -1
        self.current_command = ""
        self.commandDict = {}
        # have to figure out logical commands but havent don it yet
        self.keyWordDict = {'push': 'C_PUSH', 'pop': 'C_POP', 'label': 'C_LABEL', 'goto': 'C_GOTO', 'if-goto': 'C_IF',
                            'function': 'C_FUNCTION', 'call': 'C_CALL', 'return': 'C_RETURN', 'add': 'C_ARTHIMETIC', 'sub': 'C_ARTHIMETIC', 'eq': 'C_ARTHIMETIC'}

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
        if self.ind < self.n:
            return True
        return False

    def advance(self):
        if self.hasMoreCommands():
            self.ind += 1
            self.current_command = self.inst_st[self.ind]

    def num_instr(self):
        return self.n

    def commandType(self):
        pass


print("hello world")
vm_obj = VMParse("./StackArithmetic/SimpleAdd/SimpleAdd.vm")


def test_answer():
    assert vm_obj.num_instr() == 3
    vm_obj.ind += 5
    assert vm_obj.hasMoreCommands() == False
    vm_obj.ind = 0
    assert vm_obj.hasMoreCommands() == True
    vm_obj.ind = -1
    assert vm_obj.ind == -1
    vm_obj.advance()
    assert vm_obj.ind == 0


test_answer()
