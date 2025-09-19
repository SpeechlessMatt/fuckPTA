import re


class SplitCpp:
    def __init__(self):
        self.dic = {}

    def add_struct(self, sign_, struct: str):
        if sign_ in self.dic.keys():
            self.dic[sign_] = self.dic[sign_] + struct
        else:
            print("no this sign")

    def add_sign(self, sign_):
        if not sign_ in self.dic.keys():
            self.dic[sign_] = ''


defines = ["s0", "s1", "f0", "f1", "m", "m0f"]


def get_man():
    sc = SplitCpp()
    with open("res/logic_unit.cpp", "r") as file:
        cox = file.readlines()
    sign = ''
    se_num = 0
    for line in cox:
        if line.strip().startswith("// :"):
            if se_num == 0:
                sign = line.strip().rstrip().replace('// :', '')
                sc.add_sign(sign)
                se_num += 1
                continue
            if se_num == 1:
                se_num = 0
        if se_num == 1:
            sc.add_struct(sign, line)
    return sc

def construct_file(sc_: SplitCpp, effective_list, input_index):
    # 预先指定封装
    effective_len_max = len(effective_list) + 10
    effective_list_str = []
    for i in effective_list:
        effective_list_str.append(str(i))
        effective_list_str.append(",")
    effective_list_str.pop()
    effective_list_str = ''.join(effective_list_str)
    # s0
    result_list = [sc_.dic['s0']]
    # s1
    s1 = sc_.dic["s1"]
    s1 = re.sub(r"#define COND 'a'", "\n", s1, re.S)
    s1 = re.sub(r"#define EFFECTIVE_LEN_MAX 10", rf"#define EFFECTIVE_LEN_MAX {effective_len_max}", s1, re.S)
    s1 = re.sub(r"#define INPUT_INDEX 10", rf"#define INPUT_INDEX {input_index}", s1, re.S)
    s1 = re.sub(r"#define EFFECTIVE_LEN 10", rf"#define EFFECTIVE_LEN {len(effective_list)}", s1, re.S)
    result_list.append(s1)
    # f2
    result_list.append(sc_.dic['f2'])
    # m2
    m2 = sc_.dic['m2']
    m2 = re.sub(r"effective_list\[EFFECTIVE_LEN_MAX] = \{(.*?)};",
               r"effective_list[EFFECTIVE_LEN_MAX] = {" + effective_list_str + r"};", m2, re.S)
    result_list.append(m2)
    result = ''.join(result_list)
    return result


def construct_file_2(sc_: SplitCpp, cond, effective_list, input_index):
    # 预先指定封装
    effective_len_max = len(effective_list) + 10
    effective_list_str = []
    for i in effective_list:
        effective_list_str.append(str(i))
        effective_list_str.append(",")
    effective_list_str.pop()
    effective_list_str = ''.join(effective_list_str)
    # s0
    result_list = [sc_.dic['s0']]
    # s1
    s1 = sc_.dic["s1"]
    s1 = re.sub(r"#define COND 'a'", rf"#define COND '{cond}'", s1, re.S)
    s1 = re.sub(r"#define EFFECTIVE_LEN_MAX 10", rf"#define EFFECTIVE_LEN_MAX {effective_len_max}", s1, re.S)
    s1 = re.sub(r"#define INPUT_INDEX 10", rf"#define INPUT_INDEX {input_index}", s1, re.S)
    s1 = re.sub(r"#define EFFECTIVE_LEN 10", rf"#define EFFECTIVE_LEN {len(effective_list)}", s1, re.S)
    result_list.append(s1)
    # f1
    result_list.append(sc_.dic['f1'])
    # m
    m = sc_.dic['m']
    m = re.sub(r"effective_list\[EFFECTIVE_LEN_MAX] = \{(.*?)};",
               r"effective_list[EFFECTIVE_LEN_MAX] = {" + effective_list_str + r"};", m, re.S)
    result_list.append(m)
    result = ''.join(result_list)
    return result

# if __name__ == '__main__':
#     sc = get_man()
#     s = construct_file_2(sc, "Z", [0, 1, 2])
#     print(s)