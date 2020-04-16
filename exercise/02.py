"""
    线程锁示例
    要锁全锁
    一个执行到上锁，所有的停止
    解锁后所有的继续执行
"""
from threading import Thread,Lock

a = b = 0
lock = Lock()
def value():
    while True:
        lock.acquire()  # 上锁
        if a != b:
            print(a,b)#大量打印死循环  原因 a执行，b没有执行
        lock.release()  # 解锁

t =Thread(target=value)
t.start()
while True:
    lock.acquire()#上锁
    a +=1
    b +=1
    lock.release()#解锁

t.join()