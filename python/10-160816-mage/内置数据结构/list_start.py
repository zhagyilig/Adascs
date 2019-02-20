# coding=utf-8
# auth: zhangyiling
# time: 2019/1/22 下午11:25
# description:


class User(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return f'{self.name} {self.age}'


users = [User(f'user{i}', i) for i in (1,9,6,5,8)]

print(users)
users.sort(key=lambda u: u.age)
print(users)


"""
output:
(ven363) ➜  mage git:(master) ✗ python 列表排序.py
[user1 1, user9 9, user6 6, user5 5, user8 8]
[user1 1, user5 5, user6 6, user8 8, user9 9]s
"""



