class VMParse:
    def __init__(self, file_path):
        self.file_path = file_path
        self.inst_st = []
        self.n = 0
        self.parse()
        self.ind = 0

    def parse(self):
        with open(self.file_path) as file:
            #            read_data = file.read()
            self.ind = 0
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

    def num_instr(self):
        return self.n


print("hello world")
vm_obj = VMParse("./StackArithmetic/SimpleAdd/SimpleAdd.vm")


def test_answer():
    assert vm_obj.num_instr() == 3
