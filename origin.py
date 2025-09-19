import algorithm_set
from algorithm_set import AlgorithmSet
# from dichback import AlgorithmSet
from test import Texttest

# str类型
COND = ''


# 测试环境
test = Texttest()
test.inp()

# 待添加
# int类型
INF = 0
SUP = 10000


@test.functest
def get_len_func(effective_list):
    if effective_list[0] <= len(test.inp_) < effective_list[0] + len(effective_list):
        return 0
    return 1

@test.functest
def le_unit(effective_list):
    for i in effective_list:
        if test.inp_[i] > COND:
            return 0
    return 1

class GetLen(AlgorithmSet):

    def __init__(self):
        super().__init__()
        self.text = ''

    def logic_unit(self, effective_list: list):
        if get_len_func(effective_list) == "答案错误":
            return True
        return False


class GetRangeLE(AlgorithmSet):

    def __init__(self):
        super().__init__()
        self.cond = 'Z'
        self.text = ''

    def logic_unit(self, effective_list: list) -> bool:
        if le_unit(effective_list) == "答案错误":
            return False
        return True

def main_function_le(origin_possible_chars: list, input_len: int, least_split_degree: int = 1):
    """

    :param origin_possible_chars: 候选字段
    :param input_len: 确定总体数量
    :param least_split_degree: 最小区间长度
    :return:
    """
    # 初始化AlgorithmSet对象 内定义了小于和大于等于逻辑函数元
    # 使用小于等于准则
    get_range_le = GetRangeLE()
    # 声明全局变量 这里也就说明了，本程序很难通过外部调用，global确实不好维护
    global COND

    big_list = [[i for i in range(0, input_len)]]
    temp_big_list = []

    possible_chars = [sorted(origin_possible_chars)]
    temp_possible_chars = []
    # 结果输出区间
    result_possible_chars = []
    result_list = []

    while len(possible_chars) != 0:

        # 候选列表对应分割 形成对应关系
        for sublist in possible_chars:
            temp_possible_chars.append(sublist[0:len(sublist) // 2])
            temp_possible_chars.append(sublist[len(sublist) // 2:])

        possible_chars = temp_possible_chars
        temp_possible_chars = []

        for index, sublist in enumerate(big_list):
            # 小于等于策略
            # 这里的意思是：候选库的2n次分割后的最小字
            COND = possible_chars[index * 2][-1]
            # 调用二分回溯法:小于逻辑元
            try:
                left_list = get_range_le.dichotomy_backtracking_algorithm(sublist)
            except algorithm_set.AlgorithmChoiceError:
                left_list = get_range_le.simple_exhaustion_algorithm(sublist)

            right_list = [i for i in sublist if i not in left_list]
            # 先小后大
            temp_big_list.append(left_list)
            temp_big_list.append(right_list)

        big_list = temp_big_list
        temp_big_list = []

        # 空列表清除 逆序 避免索引问题
        for index in range(len(big_list) - 1, -1, -1):
            if len(big_list[index]) == 0 or len(possible_chars[index]) == 0:
                del possible_chars[index]
                del big_list[index]

        # 最小列表引出 逆序 防止索引问题
        for index in range(len(possible_chars) - 1, -1, -1):
            if len(possible_chars[index]) <= least_split_degree:
                result_possible_chars.append(possible_chars[index])
                result_list.append(big_list[index])
                # 引出
                del possible_chars[index]
                del big_list[index]
    # print(result_possible_chars)
    # print(result_list)
    return result_possible_chars, result_list

def return_back(input_len: int, host_list: list, child_list: list) -> str:
    str_list = []
    # 占位
    for _ in range(0, input_len):
        str_list.append(0)

    for index in range(0, len(host_list)):
        for i in child_list[index]:
            str_list[i] = host_list[index][0]

    return ''.join(str_list)

if __name__ == '__main__':
    # 初始化AlgorithmSet对象：GetLen()函数单元为：get_len()方法
    get_len = GetLen()
    # 传入有效数组 这里就是二分法的总区间
    inp_len = get_len.dichotomy_algorithm([i for i in range(INF, SUP)])

    print(f"输入的字符串长度：{inp_len}")
    # [chr(i) for i in range(65, 91)] +
    possible = [chr(i) for i in range(97, 123)] + [chr(i) for i in range(65, 91)] + ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] + ['+', '/']
    # possible = ['0', '1']
    # 使用二分回溯法 数据量大一点会好一点
    result_1, result_2 = main_function_le(possible, inp_len)
    result = return_back(inp_len, result_1, result_2)
    print(result)