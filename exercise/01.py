"""
    event 线程同步互斥方法
"""

from threading import Thread,Event
s = None
e = Event()
#线程函数
def person():
    print("前来拜山")
    global s
    s = "天王盖地虎"
    e.set()

t = Thread(target=person)
t.start()
e.wait()
if s == "天王盖地虎":
    print("宝塔镇河妖")
    print("通过")
else:
    print("拉出去枪毙十分钟")

t.join()