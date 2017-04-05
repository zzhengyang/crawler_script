# coding=utf-8
import json


import requests
import time
from vpn_switch.ali_base_api import AliyunMonitor

def releaseIp(vpnID):
    aliyun = AliyunMonitor("http://vpc.aliyuncs.com", vpnID,1)

    # 查询EIP列表
    payload = {
        'Action': 'DescribeEipAddresses',
        'RegionId': aliyun.region_id,
        'PageSize': 30,
    }
    eipList = []

    url_getEipList = aliyun.make_url(payload)
    request = requests.get(url_getEipList)
    for eip in json.loads(request.text)['EipAddresses']['EipAddress']:
        eipList.append([eip['AllocationId'], eip['IpAddress']])

        having_binding_eip = eip['AllocationId']

        #释放IP
        payload_release = {
            'Action': "ReleaseEipAddress",
            'AllocationId': having_binding_eip,
        }

        url_release = aliyun.make_url(payload_release)
        request1 = requests.get(url_release)
        print request1.text

releaseIp(1)