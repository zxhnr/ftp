"""
重点代码
    多进程并发模型

* 创建网络套接字用于接收客户端请求
* 循环等待客户端连接
* 客户端连接，则创建新的进程具体处理客户端请求
* 主进程继续等待其他客户端连接
* 如果客户端退出，则销毁对应的进程
"""

from socket import *
from multiprocessing import Process
from signal import *
import sys
# 设置全局变量 地址
HOST = "0.0.0.0"
PORT = 4279
ADDR = (HOST, PORT)


# 应对客户端请求的函数
def connected(connfd):
    while True:
        data = connfd.recv(1024)
        if not data:
            break
        print(data.decode())


def main():
    # 创建套接字
    tcp = socket(AF_INET, SOCK_STREAM)
    tcp.bind(ADDR)
    tcp.listen()  # 监听套接字
    signal(SIGCHLD, SIG_IGN) # 处理僵尸进程
    # 循环链接客户端
    while True:
        try:
            connfd, addr = tcp.accept()
            print("客户端地址：", addr)
        except Exception:
            sys.exit("服务退出")
        # 创建子进程,处理客户端请求  connected-->具体的处理函数
        p = Process(target=connected, args=(connfd,))
        p.daemon = True  # 父死子死
        p.start()  # 进程启动后 父进程不结束 产生僵尸进程

    tcp.close()


if __name__ == '__main__':
    main()
