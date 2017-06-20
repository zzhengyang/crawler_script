# coding=utf-8
from pexpect import pxssh
from tqdm import tqdm
import os
class Client:

    def __init__(self, host):
        self.host = host
        self.user = 'root'
        self.password = 'Qg2WfV1L%^R!o93'
        self.session = self.connect()

    def connect(self):
        try:
            s = pxssh.pxssh()
            s.login(self.host, self.user, self.password)
            return s
        except Exception as e:
            print(e)
            print('[-] Error Connecting' + '\n')

    def send_command(self, cmd):
        self.session.sendline(cmd)
        self.session.prompt()
        return self.session.before

def botnetCommand(host, command):
    client = Client(host)
    output = client.send_command(command)
    # print('[*] Output from ' + client.host)
    # print('[+] ' + output + '\n')

def sshstarter():
    os.system('> ~/.ssh/known_hosts')
    f = open('proxy_ip.txt', 'r')
    # commond = "wget https://git.io/vpnsetup -O vpnsetup.sh && sudo VPN_IPSEC_PSK='EfD7uv8z7JDN42K8' VPN_USER='heylotus1' VPN_PASSWORD='heylotus1' sh vpnsetup.sh"
    commond = "sudo service ipsec restart"
    for i in tqdm(f.readlines()):

        ipAddress =  i.replace("\n","")

        try:
            botnetCommand(ipAddress, commond)
            print ipAddress
        except AttributeError:
            print "[!] error esc:" + ipAddress
            continue

