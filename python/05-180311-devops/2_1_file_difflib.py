#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# 文件内容比较


import difflib
import sys


try:
    textfile1 = sys.argv[1]  # 第一个配置文件
    textfile2 = sys.argv[2]  # 第二个配置文件
except Exception as e:
    print("Error: " + str(e))
    print("Usage: %s filename1 filename2" % sys.argv[0])
    sys.exit()

def readfile(filename):
    '''文件读取分隔函数'''
    try:
        with open(filename, 'r', encoding='utf-8') as fileHandle:
            text = fileHandle.read().splitlines()   # 读取以行分隔
            return text
    except IOError as e:
        print("Read file Error: " + str(e))
        sys.exit()

if textfile1 == "" and textfile2 == "":
    print("Usage: %s filename1 filename2" % sys.argv[0])
    sys.exit()

text1_lines = readfile(textfile1)
text2_lines = readfile(textfile2)

d = difflib.HtmlDiff()
print(d.make_file(text1_lines, text2_lines))

