import sys
import pyperclip
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox
from dichback import AlgorithmSet
import keyboard
import dichback
import FuckMain
import FuckDialog
import create_cpp
import os

SET_SUP_MAX = 1000

# 测试环境
# from test import Texttest
# test = Texttest()
# test.inp()

# 资源文件目录访问
def source_path(relative_path):
    # 是否Bundle Resource
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

if not os.path.exists("res"):
    # 修改当前工作目录，使得资源文件可以被正确访问
    cd = source_path('')
    os.chdir(cd)

# str类型
COND = ''
# int
INPUT_INDEX = 1


def input_index_change(value):
    global INPUT_INDEX
    print("Changed input index.")
    INPUT_INDEX = value


class GetLen(AlgorithmSet):

    def __init__(self, get_len_func):
        super().__init__()
        self.text = ''
        self.get_len_func = get_len_func

    def logic_unit(self, effective_list: list):
        ret = self.get_len_func(effective_list)
        # 非零返回
        if ret == 1:
            return True
        else:
            return False


class GetRangeLE(AlgorithmSet):

    def __init__(self, le_unit):
        super().__init__()
        self.cond = 'Z'
        self.text = ''
        self.le_unit = le_unit

    def logic_unit(self, effective_list: list) -> bool:
        ret = self.le_unit(effective_list)
        # 非零返回
        if ret == 1:
            return True
        else:
            return False

def return_back(input_len: int, host_list: list, child_list: list) -> str:
    str_list = []
    # 占位
    for _ in range(0, input_len):
        str_list.append(0)

    for index in range(0, len(host_list)):
        for i in child_list[index]:
            str_list[i] = host_list[index][0]

    return ''.join(str_list)

# noinspection PyUnresolvedReferences
class MainHandleThreadGetLen(QThread):
    created_cpp_text = pyqtSignal(str)
    error_num = pyqtSignal()
    finish_attack = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        # 要改
        self.INF = 0
        self.SUP = 1000
        self.need_running = True
        self.choice = None

    def get_len_func(self, effective_list):
        # 显示字符串 TextBrowser
        sc = create_cpp.get_man()
        create_text = create_cpp.construct_file(sc, effective_list, INPUT_INDEX)
        self.created_cpp_text.emit(create_text)

        # 进入running循环
        print("running")
        while True:

            if not self.need_running:
                # 需要那个dialog拯救你 让你跳出循环
                break
            self.msleep(3)
        # 重新初始化
        self.need_running = True
        print(self.choice)
        # dialog告诉你了 choice
        return self.choice

    def run(self):
        # 初始化AlgorithmSet对象：GetLen()函数单元为：get_len()方法
        get_len = GetLen(self.get_len_func)
        # 传入有效数组 这里就是二分法的总区间
        try:
            inp_len = get_len.dichotomy_algorithm([i for i in range(self.INF, self.SUP)])
        except dichback.Dichback.AlgorithmListIneffectiveError:
            print("error")
            self.error_num.emit()
        else:
            print(inp_len)
            self.finish_attack.emit(int(inp_len))


# noinspection PyUnresolvedReferences
class MainHandleThreadGetRange(QThread):
    created_cpp_text = pyqtSignal(str)
    finish_attack = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.choice = None
        # 记得修改-默认值 启动的时候修改参数
        self.origin_possible_chars = []
        # 记得定义
        self.input_len = 0
        # 全是默认值
        self.least_split_degree = 1
        # 正在跑啊
        self.need_running = True

    def le_unit(self, effective_list):
        sc = create_cpp.get_man()
        create_text = create_cpp.construct_file_2(sc, COND, effective_list, INPUT_INDEX)

        self.created_cpp_text.emit(create_text)

        # 进入running循环
        print("running")
        while True:
            if not self.need_running:
                # 需要那个dialog拯救你 让你跳出循环
                break
            self.msleep(3)
        # 重新初始化
        self.need_running = True
        print(self.choice)
        # dialog告诉你了 choice
        return self.choice

    def run(self):
        # 初始化AlgorithmSet对象 内定义了小于和大于等于逻辑函数元
        # 使用小于等于准则
        # 这个地方设计很巧妙
        get_range_le = GetRangeLE(self.le_unit)
        # 声明全局变量 这里也就说明了，本程序很难通过外部调用，global确实不好维护
        global COND

        big_list = [[i for i in range(0, self.input_len)]]
        temp_big_list = []
        # 必须排序
        possible_chars = [sorted(self.origin_possible_chars)]
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
                # 二分回溯法调用逻辑元
                try:
                    left_list = get_range_le.dichotomy_backtracking_algorithm(sublist)
                except dichback.Dichback.AlgorithmChoiceError:
                    left_list = get_range_le.simple_exhaustion_algorithm(sublist)

                print("main handle")

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
                if len(possible_chars[index]) <= self.least_split_degree:
                    result_possible_chars.append(possible_chars[index])
                    result_list.append(big_list[index])
                    # 引出
                    del possible_chars[index]
                    del big_list[index]
        # print(result_possible_chars)
        # print(result_list)
        result = return_back(self.input_len, result_possible_chars, result_list)
        print(result)
        # finish
        # noinspection PyUnresolvedReferences
        self.finish_attack.emit(result)


class Dialog(QDialog):
    def __init__(self):
        super().__init__()
        self.dialog_ui = FuckDialog.Ui_Dialog()
        self.dialog_ui.setupUi(self)
        self.choice = None
        self.create_connection()
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def create_connection(self):
        self.dialog_ui.Not0RetButton.clicked.connect(self.not_zero)
        self.dialog_ui.AnswerErrButton.clicked.connect(self.answer_err)

    def not_zero(self):
        self.choice = 1
        self.close()

    def answer_err(self):
        self.choice = 0
        self.close()

# noinspection PyUnresolvedReferences
class Main(QMainWindow):

    def __init__(self):
        super().__init__()

        self.main_handle_thread_get_len = MainHandleThreadGetLen()
        self.main_handle_thread_get_range = MainHandleThreadGetRange()

        self.counts_1 = 0
        self.counts_2 = 0

        self.ui = FuckMain.Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.InputIndexSpinBox.setMinimum(1)
        self.ui.maxSpinBox.setMinimum(1)
        self.ui.minSpinBox.setMaximum(SET_SUP_MAX - 1)
        self.ui.maxSpinBox.setMaximum(SET_SUP_MAX)
        self.ui.maxSpinBox.setValue(SET_SUP_MAX)

        self.ui.check_AZ.setChecked(True)
        self.ui.check_az.setChecked(True)
        self.ui.check_09.setChecked(True)
        # 等待更新
        self.ui.check_customer.setEnabled(False)
        self.ui.SubmitButton_1.setEnabled(False)
        self.ui.SubmitButton_2.setEnabled(False)
        self.ui.CopyButton_1.setEnabled(False)
        self.ui.CopyButton_2.setEnabled(False)

        self.setFixedSize(self.width(), self.height())
        self.input_len = 0
        self.create_connection()

        self.can_shortcut = False
        self.set_enable_shortcut = True
        keyboard.add_hotkey("ctrl+.", callback=self.keyboard_shortcut)

    def keyboard_shortcut(self):
        if not self.set_enable_shortcut:
            return False
        if not self.can_shortcut:
            return False
        if self.ui.tabWidget.currentIndex() == 0:
            # 不知道为什么没有办法调用copy1
            pyperclip.copy(self.ui.textBrowser.toPlainText())
            self.ui.SubmitButton_1.click()
        if self.ui.tabWidget.currentIndex() == 1:
            # 不知道为什么没有办法调用copy2
            pyperclip.copy(self.ui.textBrowser_2.toPlainText())
            self.ui.SubmitButton_2.click()

    def create_connection(self):
        # Input Index
        self.ui.InputIndexSpinBox.valueChanged.connect(input_index_change)

        # check_box
        self.ui.check_AZ.stateChanged.connect(self.at_least_test)
        self.ui.check_az.stateChanged.connect(self.at_least_test)
        self.ui.check_09.stateChanged.connect(self.at_least_test)

        # self.ui.check_customer.stateChanged.connect(self.at_least_test)

        # Copy
        self.ui.CopyButton_1.clicked.connect(self.copy_1)
        self.ui.CopyButton_2.clicked.connect(self.copy_2)

        # getLen
        self.ui.StartButton_1.clicked.connect(self.init_get_len)
        self.ui.SubmitButton_1.clicked.connect(self.open_dialog)
        self.ui.minSpinBox.valueChanged.connect(self.min_value_change)

        self.main_handle_thread_get_len.created_cpp_text.connect(self.show_cpp)
        self.main_handle_thread_get_len.error_num.connect(self.error_num)
        self.main_handle_thread_get_len.finish_attack.connect(self.finish_attack)

        # getRangeLE
        self.ui.StartButton_2.clicked.connect(self.init_le_get_range)
        self.ui.SubmitButton_2.clicked.connect(self.open_dialog_2)
        self.ui.spinBox.valueChanged.connect(self.get_spin_box_len)
        self.main_handle_thread_get_range.created_cpp_text.connect(self.show_cpp_2)
        self.main_handle_thread_get_range.finish_attack.connect(self.finish_attack_2)

    def show_about(self):
        self.about.show()

    def at_least_test(self):
        a = self.ui.check_AZ.isChecked()
        b = self.ui.check_az.isChecked()
        c = self.ui.check_09.isChecked()
        d = self.ui.check_customer.isChecked()
        if not (a or b or c or d):
            self.ui.check_az.setChecked(True)
            QMessageBox.warning(self, "错误！", "至少选择一个备选库")

    def min_value_change(self, value: int):
        self.ui.maxSpinBox.setMinimum(value + 1)

    def copy_1(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.ui.textBrowser.toPlainText())

    def copy_2(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.ui.textBrowser_2.toPlainText())

    def flush_counts_1(self):
        self.ui.counts_1.setText(str(self.counts_1))

    def flush_counts_2(self):
        self.ui.counts_2.setText(str(self.counts_2))

    def show_cpp(self, cpp_text):
        # 展示cpp 设置发送为enabled:page1
        self.ui.textBrowser.setText(cpp_text)
        QApplication.processEvents()
        self.ui.SubmitButton_1.setEnabled(True)
        self.ui.CopyButton_1.setEnabled(True)
        self.can_shortcut = True

    def show_cpp_2(self, cpp_text):
        # 展示cpp 设置发送为enabled:page2
        self.ui.textBrowser_2.setText(cpp_text)
        QApplication.processEvents()
        self.ui.SubmitButton_2.setEnabled(True)
        self.ui.CopyButton_2.setEnabled(True)
        self.can_shortcut = True

    def get_spin_box_len(self, length):
        self.input_len = length

    def init_get_len(self):
        self.ui.StartButton_1.setEnabled(False)
        self.ui.maxSpinBox.setEnabled(False)
        self.ui.minSpinBox.setEnabled(False)
        self.ui.InputIndexSpinBox.setEnabled(False)
        self.can_shortcut = False
        # flush counts
        self.counts_1 = 0
        self.flush_counts_1()
        # 预留
        self.main_handle_thread_get_len.INF = self.ui.minSpinBox.value()
        self.main_handle_thread_get_len.SUP = self.ui.maxSpinBox.value()
        self.main_handle_thread_get_len.start()

    def error_num(self):
        QMessageBox.warning(self, "错误！", "没有匹配的长度，请重新设置数字范围")
        self.ui.StartButton_1.setEnabled(True)
        self.ui.SubmitButton_1.setEnabled(False)
        self.ui.CopyButton_1.setEnabled(False)
        self.ui.maxSpinBox.setEnabled(True)
        self.ui.minSpinBox.setEnabled(True)
        self.ui.InputIndexSpinBox.setEnabled(True)
        self.can_shortcut = True

    def init_le_get_range(self):
        if self.input_len == 0:
            QMessageBox.warning(self, "错误！", "list_len不应该为0")
            return 0
        self.can_shortcut = False
        # flush counts
        self.counts_2 = 0
        self.flush_counts_2()

        self.ui.StartButton_2.setEnabled(False)
        self.ui.spinBox.setEnabled(False)
        self.ui.InputIndexSpinBox.setEnabled(False)
        self.ui.counts_2.setText("0")

        temp = []
        # 获取备选库
        if self.ui.check_az.isChecked():
            for i in range(97, 123):
                temp.append(chr(i))
        if self.ui.check_AZ.isChecked():
            for i in range(65, 91):
                temp.append(chr(i))
        if self.ui.check_09.isChecked():
            temp = temp + ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        self.ui.check_09.setEnabled(False)
        self.ui.check_az.setEnabled(False)
        self.ui.check_AZ.setEnabled(False)

        # 预留 : *自定义
        self.main_handle_thread_get_range.origin_possible_chars = temp
        del temp

        self.main_handle_thread_get_range.input_len = self.input_len
        self.main_handle_thread_get_range.least_split_degree = 1
        self.main_handle_thread_get_range.start()

    def finish_attack(self, result: int):
        QMessageBox.information(self, "Success!", f"字符串长度是: {result}")
        self.ui.StartButton_1.setEnabled(True)
        # 为page2 提供数字 这就是优雅和全面
        # 为page2 提供数字 这就是优雅和全面
        self.ui.spinBox.setValue(result)
        self.ui.SubmitButton_1.setEnabled(False)
        self.ui.CopyButton_1.setEnabled(False)

        self.ui.maxSpinBox.setEnabled(True)
        self.ui.minSpinBox.setEnabled(True)
        self.ui.InputIndexSpinBox.setEnabled(True)

        self.can_shortcut = True

    def finish_attack_2(self, result: str):
        QMessageBox.information(self, "Success!", result)
        self.ui.StartButton_2.setEnabled(True)
        self.ui.spinBox.setEnabled(True)
        self.ui.SubmitButton_2.setEnabled(False)
        self.ui.CopyButton_2.setEnabled(False)

        self.ui.check_09.setEnabled(True)
        self.ui.check_az.setEnabled(True)
        self.ui.check_AZ.setEnabled(True)
        self.ui.InputIndexSpinBox.setEnabled(True)

        self.can_shortcut = True

    def open_dialog(self):
        # 初始化对象
        self.can_shortcut = False
        dialog = Dialog()
        dialog.move(self.pos())
        dialog.exec()
        choice = dialog.choice
        # 防止关闭
        if choice is None:
            self.can_shortcut = True
            return 0
        if choice == 1:
            # 非零返回
            self.main_handle_thread_get_len.choice = 1
            self.main_handle_thread_get_len.need_running = False
            self.counts_1 += 1
            self.flush_counts_1()

        if choice == 0:
            # 答案错误
            self.main_handle_thread_get_len.choice = 0
            self.main_handle_thread_get_len.need_running = False
            self.counts_1 += 1
            self.flush_counts_1()

    def open_dialog_2(self):
        # 初始化对象
        self.can_shortcut = False
        dialog = Dialog()
        dialog.move(self.pos())
        dialog.exec()
        choice = dialog.choice
        # 防止关闭
        if choice is None:
            self.can_shortcut = True
            return 0
        if choice == 1:
            # 非零返回
            self.main_handle_thread_get_range.choice = 1
            self.main_handle_thread_get_range.need_running = False
            self.counts_2 += 1
            self.flush_counts_2()
        if choice == 0:
            # 答案错误
            self.main_handle_thread_get_range.choice = 0
            self.main_handle_thread_get_range.need_running = False
            self.counts_2 += 1
            self.flush_counts_2()

    def closeEvent(self, event):
        # 释放资源
        self.main_handle_thread_get_range.exit()
        self.main_handle_thread_get_len.exit()
        event.accept()


if __name__ == '__main__':
    # 实例化，传参
    app = QApplication(sys.argv)
    main_window = Main()
    main_window.show()
    # 进入程序的主循环，并通过exit函数确保主循环安全结束(该释放资源的一定要释放)
    sys.exit(app.exec())
