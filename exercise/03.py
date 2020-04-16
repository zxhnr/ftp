"""
    练习： 两个分支线程同时运行
    一个线程打印1-52 这52个数字
    另一个打印a-z 26 个字母
    要求12a34b56c......5152z
    不用sleep
"""

from threading import Thread, Lock

lock = Lock()
lock1 = Lock()

words = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n'
    , 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


def number():
    for i in range(1, 53, 2):
        lock.acquire()
        print(i, end='')
        print(i + 1, end='')
        lock1.release()


def word():
    for i in words:
        lock1.acquire()
        print(i, end="")
        lock.release()


t = Thread(target=number)
t1 = Thread(target=word)
lock1.acquire()
t.start()
t1.start()
t.join()
t1.join()
