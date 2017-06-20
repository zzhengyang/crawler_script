# coding=utf-8
import json
import requests
from base_api.ali_base_api import AliyunMonitor


def listIp(vpnID, file):
    aliyun = AliyunMonitor("http://vpc.aliyuncs.com", vpnID, 1)

    # 查询EIP列表
    payload = {
        'Action': 'DescribeEipAddresses',
        'RegionId': aliyun.region_id,
        'PageSize': 30,
    }
    url_getEipList = aliyun.make_url(payload)
    request = requests.get(url_getEipList, headers={'Accept-Encoding': 'identity'})
    for eip in json.loads(request.text)['EipAddresses']['EipAddress']:
        print eip['IpAddress']
        file.write(str(eip['IpAddress']) + '\n')

def list():
    #输出ip列表，写入proxy_ip.txt
    file = open('proxy_ip.txt', 'w')
    for proxyId in range(1, 19):
        listIp(proxyId, file)
    file.close()