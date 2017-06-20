# coding=utf-8
import requests
from sshConnector import botnetCommand

def proxyTest():
    f = open('proxy_ip.txt', 'r')
    for i in f.readlines():
        try:
            r=requests.get("http://ifconfig.io/ip", proxies={'http': i.replace("\n","")+":8888"}, timeout=20)
            proxyIp = r.text
            print "[ok] ====> " + i.replace("\n","")
        except:
            # 代理测试失败则连接ssh重启代理服务
            botnetCommand(i.replace("\n",""), 'sudo service tinyproxy restart')

            print i.replace("\n","")