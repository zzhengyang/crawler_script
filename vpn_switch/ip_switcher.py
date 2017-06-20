# coding=utf-8
from switch_scripts import unlashIp
from switch_scripts import allocateIp
from switch_scripts import switchIP
from switch_scripts import proxyTest
from switch_scripts import sshConnector
from switch_scripts import listIp

if __name__ == '__main__':
    # unlashIp.unlash()   #解绑ip
    # unlashIp.release()  #释放ip
    # allocateIp.allocate()   #申请ip
    # switchIP.switch()   #绑定ip
    # listIp.list()   #输出绑定ip列表并写入proxy_ip.txt
    sshConnector.sshstarter()  #批量连接ssh，重启代理服务
    # proxyTest.proxyTest()      #测试代理，并重新重启失败代理
