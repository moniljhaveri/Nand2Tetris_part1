class VMParse:
    def __init__(self, file_path):
        self.file_path = file_path
        self.inst_st = []

    def parse(self):
        with open(self.file_path) as file:
            #            read_data = file.read()
            for line in file:
                line_split = line.split("//")
                line_seg = line_split[0].replace("\n", "")
                if 0 < len(line_seg):
                    self.inst_st.append(line_seg)


print("hello world")
vm_obj = VMParse("./StackArithmetic/SimpleAdd/SimpleAdd.vm")

vm_obj.parse()
print(vm_obj.inst_st)
