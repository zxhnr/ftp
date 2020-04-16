"""
    FTP 客户端
"""
from socket import *
from time import sleep

sever_address = ("127.0.0.1", 4277)


class FTPClient():
    def __init__(self, tcp):
        self.tcp = tcp

    def cmd(self, cmd):
        if cmd == '1':
            self.list_file()
        elif cmd == '2':
            self.update()
        elif cmd == '3':
            self.download()
        elif cmd == '4':
            self.exit()
        else:
            print("无此命令")

    def list_file(self):
        file_name = input("请输入文件路径")
        mes = 'L %s' % file_name
        self.tcp.send(mes.encode())
        data = self.tcp.recv(4096)
        for item in data.decode().split("###"):
            print(item, end='\n')
        print("打印完毕")
        print("========================")

    def update(self):
        while True:
            file_name = input("请输入文件路径")
            mes = 'U %s' % file_name
            self.tcp.send(mes.encode())
            cmd = self.tcp.recv(128)
            if cmd.decode() == 'no':
                print("文件名已存在")
            elif cmd.decode() == "ok":
                break
        file_target = input("请输入要传输的文件路径")
        with open(file_target, 'rb') as file:
            data = file.read()
            self.tcp.send(data)
        self.tcp.send("##".encode())
        print(self.tcp.recv(128).decode())

    def download(self):
        while True:
            file = input("请输入需要下载的文件路径")
            mes = 'D %s' % file
            self.tcp.send(mes.encode())
            cmd = self.tcp.recv(128).decode()
            if cmd == 'no':
                print('文件路径错误')
            elif cmd == 'ok':
                break
        while True:
            path = input("请输入文件保存路径")
            try:
                file = open(path, 'rb')
            except Exception:
                cmd1 = 0
            else:
                cmd1 = 1
            if cmd1 == 0:
                break
        file = open(path, "wb")
        while True:
            data = self.tcp.recv(1024)
            if data.decode() == "##":
                break
            file.write(data)
        file.close()
        print("下载完成")

    def exit(self):
        self.tcp.send('Q '.encode())


def main():
    tcp = socket()
    tcp.connect(sever_address)
    ftp = FTPClient(tcp)
    while True:
        print("已连接")
        print("1，查看文件列表")
        print("2，上传文件")
        print("3，下载文件")
        print("4,退出")
        pcmd = input("输入命令：")
        ftp.cmd(pcmd)
        if pcmd == '4':
            sleep(3)
            break
    tcp.close()

if __name__ == '__main__':
    main()
