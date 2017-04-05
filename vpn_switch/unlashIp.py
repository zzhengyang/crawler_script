# coding=utf-8
import json


import requests
import time
from vpn_switch.ali_base_api import AliyunMonitor

def unlashIp(vpnID):
    aliyun = AliyunMonitor("http://vpc.aliyuncs.com", vpnID,1)

    # 查询EIP列表
    payload = {
        'Action': 'DescribeEipAddresses',
        'RegionId': aliyun.region_id,
        'PageSize': 30,
    }
    eipList = []
    # having_binding_eip = ''
    # having_binding_instanceid=''
    url_getEipList = aliyun.make_url(payload)
    request = requests.get(url_getEipList)
    for eip in json.loads(request.text)['EipAddresses']['EipAddress']:
        eipList.append([eip['AllocationId'], eip['IpAddress']])
        # print eip
        if eip['InstanceId']:
            having_binding_eip = eip['AllocationId']
            having_binding_instanceid = eip['InstanceId']

            #解绑ip
            payload_unlash = {
                'Action': "UnassociateEipAddress",
                'AllocationId': having_binding_eip,
                'InstanceId': having_binding_instanceid

            }

            url_unlash = aliyun.make_url(payload_unlash)
            request1 = requests.get(url_unlash)
            print request1.text
for i in range(1,6):
    unlashIp(i)