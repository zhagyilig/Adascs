# coding=utf-8
# auth: zhangyiling
# time: 2019-04-06 18:58
# description:

"""
资料:
https://github.com/taizilongxu/interview_python

https://juejin.im/post/5b6bc1d16fb9a04f9c43edc3

"""

# http://developer.51cto.com/art/201802/565802.htm
class A(object):
    def show(self):
        print('base show')


class B(object):
    def show(self):
        print('derived show')


obj = B()
obj.show()


obj.__class__ = A
obj.show()

################################################


num = 8

class C(object):
    num = 2
    print(
        '-------'
    )
    print(num)

class D(object):
    print('+++++')
    print(num)

D()
C()
D()