#!/usr/bin/env python
# _*_ coding:utf-8 _*_

class Input_Base():
    def __init__(self, input_name):
        self.precondition = ''
        self.platform_name = ''
        self.project_name = ''
        self.model_name = ''
        self.sub_model_name = ''
        self.function_name = input_name
        self.version = ''
        self.case = dict()
        self.case[input_name + "默认值"] = ["输入框有默认值显示默认值，输入框无默认值显示预期值。",'按前置条件']

    def __eq__(self, other):
        if  isinstance(other, Input_Base):
            return (self.function_name == other.function_name)
        else:
            return False
    def __ne__(self, other):
        return (not self.__eq__(other))
    def __hash__(self):
        return  hash(self.function_name)
    def add_case(self,case_name,case_pre='',case_step=''):
        self.case[case_name] = [case_pre,case_step]
    def set_precondition(self,precondition):
        self.precondition = precondition
    def set_platform_name(self,plName):
        self.platform_name = plName
    def set_project_name(self,pjName):
        self.project_name = pjName
    def set_model_name(self,mdName):
        self.model_name = mdName
    def set_sub_model_name(self,smdName):
        self.sub_model_name = smdName
    def set_function_name(self,ftName):
        self.function_name = ftName
    def set_function_name(self,version):
        self.version = version
    def all_cases(self):
        return self.case
class Input_Text(Input_Base):
    def __init__(self,input_name):
        super(Input_Text,self).__init__(input_name)
        self.add_case(input_name + "中文字符","文本框中可以输入中文字符。", "输入中文字符。（如：测试文本框）")
        self.add_case(input_name + "英文字符", "文本框中可以输入英文字符。", "输入英文字符。（如：TestText）")
        self.add_case(input_name + "数字字符", "文本框中可以输入数字字符。", "输入数字字符。（如：-0123.4560）")
        self.add_case(input_name + "特殊字符", "文本框中可以输入特殊字符。", "输入特殊字符。（如：αβγさしすⅠⅡⅢ＋－×÷）")
        self.add_case(input_name + "混合字符", "文本框中可以输入所有字符混合。", "输入混合字符。（如：测试文本框TestText-0123.4560αβγさしすⅠⅡⅢ＋－×÷）")
        self.add_case(input_name + "字符长度限制", "文本框中输入超过字符长度的信息，消息提醒且无法提交当前页面；或文本框中无法输入超过字符长度的信息。如无限制多少都可以提交。", "输入字符长度超出限制长度，如无限制文本框中输入足够长的信息（如100个字符）")

class Input_Number(Input_Base):
    def __init__(self,input_name):
        super(Input_Number,self).__init__(input_name)
        self.add_case(input_name + "数值正负", "如果只限制正数，则负数提交报错，否则可以提交当前页面。", "输入正负数。（如：123，-123）")
        self.add_case(input_name + "数值有效位", "允许小数（保留位数），超出四舍五入。", "按照其规则，依次在数字框中输入小数（如：规定保留3位小数，依次在数字框中输入1.23456，1.2）")
        self.add_case(input_name + "数值限值", "如果限制了大小输入超出限制值会报错，否则都可以正常提交。", "有限制大小的话数字框中输入超过数值大小范围的数字，否则输入999999999")
        self.add_case(input_name + "非数值", "消息提醒且无法提交当前页面。", "文本框中输入非数值字符")

class Input_Textarea(Input_Text):
    def __init__(self,input_name):
        super(Input_Textarea,self).__init__(input_name)
        self.add_case(input_name + "缩小", "页面显示正确。", "拖动多行文本框右下方缩放按钮，使多行文本框缩小")
        self.add_case(input_name + "放大", "页面显示正确。", "拖动多行文本框右下方缩放按钮，使多行文本框放大")

class Input_Radio(Input_Base):
    def __init__(self,input_name):
        super(Input_Radio,self).__init__(input_name)
        self.add_case(input_name + "勾选", "点击第1个选项时第1个选项被勾选；点击第2个选项时第2个选项被勾选，第1个选项取消勾选。", "点击勾选框")
        self.add_case(input_name + "取消勾选", "可以取消勾选：点击某选项第1次时勾选该选项，第2次时取消勾选。不可以取消勾选：点击某选项第1次时勾选该选项，第2次时无反应。", "双击勾选框")


class Input_Checkbox(Input_Base):
    def __init__(self,input_name):
        super(Input_Checkbox,self).__init__(input_name)
        self.add_case(input_name + "勾选", "点击第1个选项时第1个选项被勾选；点击第2个选项时第2个选项被勾选，第1个选项不变。", "点击勾选框")
        self.add_case(input_name + "取消勾选", "可以取消勾选：点击某选项第1次时勾选该选项，第2次时取消勾选。不可以取消勾选：点击某选项第1次时勾选该选项，第2次时无反应。", "双击勾选框")

class Input_Select(Input_Base):
    def __init__(self,input_name):
        super(Input_Select,self).__init__(input_name)
        self.add_case(input_name + "下拉值内容", "下拉值数量正确。", "点击展开下拉框")
        self.add_case(input_name + "随机选取下拉值", "选择下拉框的某选项后，下拉框的值变为选中选项的值。", "随机选择下拉框值")
        self.add_case(input_name + "关联项", "如果有关联项的话，关联项展示正确。", "随机选择下拉框值")


class Input_Date(Input_Base):
    def __init__(self,input_name):
        super(Input_Date,self).__init__(input_name)
        self.add_case(input_name + "日期选择", "点击选择日期按钮，弹出日期选择框。日期选择框中选择一个日期，日期选择框自动关闭，日期框中自动填入选择的日期。", "点击选择日期")
        self.add_case(input_name + "日期自动选择", "根据实际规则，进行会让日期自动选择的操作，日期框自动填入日期。（如【申请日期】选择一个日期，【提交日期】也自动选择相同的日期）。", "点击选择近一周/一个月等")
        self.add_case(input_name + "日期输入", "如果支持手动输入则日期框中输入正确格式的信息，日期框变为输入的日期，可以提交当前页面。日期框中输入错误格式的信息（如：测试日期框），消息提醒且无法提交当前页面，否则输入无效。", "手动输入日期")
        self.add_case(input_name + "日期范围", "日期框中输入日期范围内的日期，日期框变为输入的日期，可以提交当前页面。日期框中输入日期范围外的日期，消息提醒且无法提交当前页面。", "点击选择一段日期")
        # self.add_case(input_name + "日期判断", "根据实际规则，输入符合日期判断规则的日期，日期框变为输入的日期，可以提交当前页面。（如【开始日期】小于等于【结束日期】）。根据实际规则，输入不符合日期判断规则的日期，消息提醒且无法提交当前页面。（如【开始日期】大于【结束日期】）。", "")
