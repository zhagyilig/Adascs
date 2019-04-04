# -*- coding: utf-8 -*-


def bulk(self):
    print('%s is yelling ...' %self.name)

class Dog(object):
    def __init__(self, name):
        self.name = name

    def eat(self, food):
        print('%s is eating %s' % self.name,food)

d = Dog('kk')

choice = input('>> ').strip()

if hasattr(d, choice):
    func = getattr(d, choice)
    func('baozi')
else:
    setattr(d, choice, bulk)  # d.choice = bule
    func = getattr(d, choice)
    func(d)
