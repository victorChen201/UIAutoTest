#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import requests
import os
import time
import re
from selenium import webdriver
import Input_Case,Button_Case
from SaveCaseToExcel import SaveCaseToExcel
class Operation_Platform():
    def __init__(self,url='http://duop.imgo.tv/#/login'):
        self.driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        self.driver.implicitly_wait(2)
        self.driver.maximize_window()
        self.driver.get(url)
        self.controls = set()

    def set_up(self):
        pass

    def tear_down(self):
        self.driver.close()

    def login(self,patform_name='AMP'):
        self.patform_name = patform_name
        need_login = self.driver.find_elements_by_xpath('//span[text()="登 录"]')
        if need_login.__len__()==0:
            print ("不需要登陆")
            return
        self.driver.find_element_by_xpath('//input[@placeholder="请输入OA邮箱"]').send_keys('shuangsheng')
        self.driver.find_element_by_xpath('//input[@placeholder="请输入密码"]').send_keys('Css861007/')
        self.driver.find_element_by_xpath('//span[text()="登 录"]').click()
        self.driver.set_page_load_timeout(3)
        self.driver.find_element_by_xpath('//div[text()="%s"]/preceding-sibling::div[2]' % patform_name).click()

    def switch_page(self,page_list=[]):
        self.page_name = page_list
        for p in page_list:
            #判断是否可以展开
            wb = self.driver.find_element_by_xpath('//span[text()="%s"]'%p)
            i_numbers = wb.find_elements_by_xpath('following-sibling::i')
            if i_numbers.__len__()!=0:#能展开
                cs = wb.find_element_by_xpath('../..').get_attribute('class')
                if "is-opened" in cs:
                    pass
                else:
                    wb.click()
                # print (cs)
            else:
                wb.click()

    def find_all_selects(self):
        name_list = []
        divs = self.driver.find_elements_by_xpath('//div[@x-placement="bottom-start" or @x-placement="up-start"]')
        if divs.__len__()>0:
            lis = divs[0].find_elements_by_tag_name("li")
            for li in lis:
                name_list.append(li.text)
        return name_list

    def find_all_inputs(self,element='',precondition=''):
        inputs = element.find_elements_by_tag_name("input") if element != '' else self.driver.find_elements_by_tag_name("input")
        case = ''
        for i in inputs:
            type=''
            placeholder=''
            disabled = ''
            try:
                type = i.get_attribute("type")
            except Exception as e:
                type=''
            try:
                disabled = i.get_attribute("disabled")
            except Exception:
                disabled = ''
            try:
                placeholder = i.get_attribute("placeholder")
            except Exception as e:
                #没有placeholder属性
                placeholder="请选择"
            if (type=="checkbox" or type=="radio") and disabled != "true":
                label = i.find_elements_by_xpath('../../preceding-sibling::label')
                if label.__len__() == 1:
                    case = Input_Case.Input_Checkbox(label[0].text+"复选框") if type == "checkbox" else Input_Case.Input_Radio(label[0].text+"单选框")
                    case.set_precondition(precondition if precondition != '' else "登陆%s,进入%s" % (
                    self.patform_name, '->'.join(self.page_name)))
                    case.set_platform_name("统一运营平台")
                    case.set_project_name(self.patform_name)
                    case.set_model_name(self.page_name[0])
                    case.set_sub_model_name(self.page_name[-1])
                    case.set_function_name(label[0].text)
                    self.controls.add(case)
                # continue
            elif (type == "text" or type == "number" or type == "textarea") and disabled != "true":
                if placeholder == "开始日期" or placeholder == "结束日期":
                    case = case or Input_Case.Input_Date('')
                    case.set_precondition(precondition if precondition != '' else "登陆%s,进入%s"%(self.patform_name, '->'.join(self.page_name)))
                    case.set_platform_name("统一运营平台")
                    case.set_project_name(self.patform_name)
                    case.set_model_name(self.page_name[0])
                    case.set_sub_model_name(self.page_name[-1])
                    case.set_function_name("日期")
                    self.controls.add(case)
                else:
                    span_number = i.find_elements_by_xpath('./../span') #+ i.find_elements_by_xpath('preceding-sibling::span')
                    label = []
                    end_name = ''
                    if span_number:#下拉框
                        label = i.find_elements_by_xpath('../../../preceding-sibling::label')
                        end_name = "下拉框"
                        # 是否展开下拉框，没有展开要先点击下
                        i_s = span_number[0].find_elements_by_tag_name('i')
                        if i_s:
                            if "is-reverse" not in i_s[0].get_attribute("class"):
                                try:
                                    i.click()
                                except Exception:
                                    self.driver.execute_script("arguments[0].click();",i)
                                time.sleep(1)
                            try:
                                i.click()
                            except Exception:
                                self.driver.execute_script("arguments[0].click();", i)
                        else:
                            print ("没找到下拉框：",label[0].text)
                        # selected_elements = self.find_all_selects()
                        # self.driver.execute_script("arguments[0].click();",i)
                        # print (selected_elements)
                    else:#文本框
                        label = i.find_elements_by_xpath('../../preceding-sibling::label')
                        end_name = "文本框"
                    if label:
                        if type == "text":
                            case = ((end_name == "下拉框") and Input_Case.Input_Select(label[0].text+end_name)) or Input_Case.Input_Text(label[0].text+end_name)
                        elif type == "number":
                            case = Input_Case.Input_Number(label[0].text+end_name)
                        case.set_precondition(precondition if precondition != '' else "登陆%s,进入%s" % (self.patform_name, '->'.join(self.page_name)))
                        case.set_platform_name("统一运营平台")
                        case.set_project_name(self.patform_name)
                        case.set_model_name(self.page_name[0])
                        case.set_sub_model_name(self.page_name[-1])
                        case.set_function_name(label[0].text)
                        self.controls.add(case)
            else:
                print (type,"没有处理")

    def find_all_buttons(self,element='',precondition=''):
        #过滤表格中的button
        bts = element.find_elements_by_xpath('div[not(contains(@class, "cell"))]/button') if element != '' else self.driver.find_elements_by_xpath('//div[not(contains(@class, "cell"))]/button')
        for bt in bts:
            spans = bt.find_elements_by_tag_name('span')
            if spans.__len__() != 0 and spans[0].text != '':
                if re.search("新(建|增).*",spans[0].text):
                    # bt.click()
                    self.driver.execute_script("arguments[0].click();", bt)
                    time.sleep(1)
                    dialogs = self.driver.find_elements_by_xpath('//div[@role="dialog"]')
                    # for dialog in dialogs:

                    self.find_all_inputs(dialogs[-1],precondition="登陆%s,进入%s,点击%s"% (self.patform_name, '->'.join(self.page_name), spans[0].text))
                    try:
                        bt = dialogs[-1].find_element_by_xpath('.//button[@aria-label="Close"]')
                        self.driver.execute_script("arguments[0].click();", bt)
                        # dialogs[-1].find_element_by_xpath('//button[@aria-label="Close"]').click()
                    except Exception:
                        dialogs[-1].find_element_by_xpath('//button/span[text()="取 消"]').click()
                    time.sleep(1)
                case = Button_Case.Button(spans[0].text+"按钮")
                case.set_platform_name("统一运营平台")
                case.set_project_name(self.patform_name)
                case.set_model_name(self.page_name[0])
                case.set_sub_model_name(self.page_name[-1])
                case.set_function_name(spans[0].text)
                case.set_precondition(precondition if precondition != '' else "登陆%s,进入%s" % (self.patform_name, '->'.join(self.page_name)))
                self.controls.add(case)

    def all_controls(self):
        return self.controls

if __name__=="__main__":
    target = "http://test-admin.da.imgo.tv/adx/creative/pre"
    op = Operation_Platform()
    op.login('AMP')
    op.switch_page(["素材管理", "广告素材"])
    time.sleep(1)
    # op.find_all_inputs()
    op.find_all_buttons()
    s = SaveCaseToExcel()
    s.writeCases(op.all_controls())
    s.saveCaseToExcel("Testcase.xlsx")