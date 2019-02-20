#coding=utf-8
from selenium import webdriver
import os
import sys
import time

reload(sys)
sys.setdefaultencoding('utf8')

#设置浏览器驱
driver = webdriver.Chrome('/Users/mac/Downloads/chromedriver')

#最大化窗口
driver.maximize_window()

jenkinsPage = 'http://192.168.199.120:8080/job/uat5/'

defaultProject = []
defaultValue = []

projectFileName = 'jenkinsProject_uat5.csv'

def getDataFromFile(projectFileName):
    file = open(projectFileName,'r')
    while 1:
        line = file.readline()
        if not line:
            break
        print(line) 
        data = [str(n) for n in line.split(',')]
        print(data)
        defaultProject.append(data[0])
        defaultValue.append(data[1])
        #print (data[0] + '  ' + data[1] + '\n')
    file.close()

def setProjectBranch(driver,strBranch):
    time.sleep(10)
    branch_key = driver.find_element_by_xpath('//*[@id="main-panel"]/div/div/div/form/table/tbody/tr[79]/td[3]/div/div[1]/table/tbody/tr[1]/td[3]/input')
    branch_key.clear()
    branch_key.send_keys(strBranch)

def setProjects(driver):
    for i in range(len(defaultProject)):
        url = jenkinsPage + 'job/' +defaultProject[i]+ '/configure'
        driver.get(url)
        print ('项目'+defaultProject[i]+'的分支为： '+defaultValue[i])
        setProjectBranch(driver, defaultValue[i])
        time.sleep(2)

getDataFromFile(projectFileName)
setProjects(driver)
