"""
    多线程并发模型
- 创建网络套接字用于接收客户端请求
- 等待客户端连接
- 客户端连接，则创建新的线程具体处理客户端请求
- 主线程继续等待其他客户端连接
- 如果客户端退出，则销毁对应的线程
"""
from socket import *
from threading import Thread

#设置全局变量
HOST = "0.0.0.0"
PORT = 4278
ADDR = (HOST,PORT)
#应对函数
def do(conned):
    pass

def main():
    tcp = socket()
    tcp.bind(ADDR)
    tcp.listen()
    while True:
        try:
            connfd, addr = tcp.accept()
            print("客户端地址：", addr)
        except Exception:
            sys.exit("服务退出")
        #创建新线程
        t = Thread(target=do,args=(connfd,))
        t.daemon = True
        t.start()
    tcp.close()


if __name__ == '__main__':
    main()