"""
    ftp 文件服务器
python3.6
socket tcp and process
确保文件完整
"""
"""
技术分析
-并发模型
-tcp
"""
"""
功能分析（封装模型）
【1】 分为服务端和客户端，要求可以有多个客户端同时操作。
-服务端 多进程并发模型
-客户端 tcp接入
【2】 客户端可以查看服务器文件库中有什么文件。
-服务端 
 --接受消息
 --打开目录 
 --遍历目录下文件
 --发送消息
-客户端 
 --发送请求 看文件列表
 --接收消息
【3】 客户端可以从文件库中下载文件到本地。
-客户端
 --发起请求
 --
-服务端

【4】 客户端可以上传一个本地文件到文件库。

【5】 使用print在客户端打印命令输入提示，引导操作
"""
"""
    通信协议设计
-请求类型
 --L -->查看文件列表
 --U -->上传文件
 --D -->下载文件
 --Q -->退出
-请求参量
"""
"""
    细节处理
"""
from socket import *
from threading import Thread
from signal import *
import sys
from os import listdir

HOST = "0.0.0.0"
PORT = 4277
ADDR = (HOST, PORT)


class FTPServer(Thread):
    def __init__(self, connfd):
        super().__init__()
        self.connfd = connfd

    def run(self):
        while True:
            data = self.connfd.recv(1024)
            if not data:
                return
            data = data.decode().split(" ", 1)
            if data[0] == 'L':
                self.list_file(data[1])
            elif data[0] == 'U':
                self.update(data[1])
            elif data[0] == 'D':
                self.download(data[1])
            elif data[0] == 'Q':
                return

    def list_file(self, file_name):
        file = listdir(file_name)  # 列表
        if not file:
            self.connfd.send("文件夹为空".encode())
        mes = "###".join(file)
        self.connfd.send(mes.encode())
        # data = '###'.join(file)  将列表中元素拼接为一个字符串，并添加###分隔

    def update(self, file_target):
        try:
            file = open(file_target, 'rb')
        except:
            self.connfd.send("ok".encode())
        else:
            self.connfd.send('no'.encode())
            return
        with open(file_target, 'wb') as file:
            while True:
                data = self.connfd.recv(1024)
                if data.decode() == "##":
                    break
                file.write(data)
        self.connfd.send("传输完毕".encode())

    def download(self, file_target):
        try:
            file = open(file_target, 'rb')
        except:
            self.connfd.send('no'.encode())
            return
        else:
            self.connfd.send('ok'.encode())
        message = file.read()
        self.connfd.send(message)
        file.close()
        self.connfd.send("##".encode())



def main():
    tcp = socket()
    tcp.bind(ADDR)
    tcp.listen()
    signal(SIGCHLD, SIG_IGN)  # 处理僵尸进程
    while True:
        try:
            connfd, addr = tcp.accept()
        except:
            sys.exit()
            # 创建子进程,处理客户端请求  connected-->具体的处理函数
        p = FTPServer(connfd)
        p.daemon = True  # 父死子死
        p.start()  # 进程启动后 父进程不结束 产生僵尸进程
        p.join()
    tcp.close()


if __name__ == '__main__':
    main()
