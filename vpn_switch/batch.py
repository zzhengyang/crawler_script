#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
import paramiko
import threading
import getpass
def main():
    try:
        cmd = sys.argv[1:]
        username = "root"
        passwd = 'Qg2WfV1L%^R!o93'
        threads = [4]
        f = file('proxy_ip.txt')
        while True:
            ip = f.readline()
            if len(ip) == 0:
                break
            a = threading.Thread(target=ssh2,args=(ip,username,passwd,cmd))
            a.start()
        f.close()
    except:
         pass
def ssh2(ip,username,passwd,cmd):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip,22,username,passwd,timeout=5)
        for m in cmd:
            stdin,stdout,stderr = ssh.exec_command(m)
            # stdin.write("Y")
            out = stdout.readlines()
            for o in out:
                print o,
        print '[OK]%s' %(ip),
        print '========================================================================='
        ssh.close()
    except:
        print '[Error]%s' %(ip),
        print '========================================================================='
if __name__ == '__main__':
    main()