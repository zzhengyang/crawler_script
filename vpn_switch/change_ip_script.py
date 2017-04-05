#-*- coding: utf-8 -*-
import paramiko
#paramiko.util.log_to_file('/tmp/sshout')
def ssh2(ip,username,passwd,cmd):
    # try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip,22,username,passwd)#key_filename='/Users/Zyang/.ssh/known_hosts')
        stdin,stdout,stderr = ssh.exec_command(cmd)
#           stdin.write("Y")   #简单交互，输入 ‘Y’
        print stdout.read()
#        for x in  stdout.readlines():
#          print x.strip("n")
        print '%stOKn'%(ip)
        ssh.close()
    # except :
    #     print '%stErrorn'%(ip)
commend = "sed 's/59.110.136.217//g ' ;sed 's/59.110.137.125//g';sed 's/139.224.238.40//g';sed 's/120.77.211.195//g '"
ssh2("139.129.210.170","test","2e6xYnRO1mBE", commend)