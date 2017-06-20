# coding=utf-8
import json
import time
import requests
from tqdm import trange
from base_api.ali_base_api import AliyunMonitor


def swichIp(vpnID,eipIndex,ecsIndex):
    aliyun = AliyunMonitor("http://vpc.aliyuncs.com", vpnID, ecsIndex)

    # 查询EIP列表
    payload = {
        'Action': 'DescribeEipAddresses',
        'RegionId': aliyun.region_id,
        'PageSize': 30,
    }
    eipList = []
    having_binding_eip = ''
    url_getEipList = aliyun.make_url(payload)
    request = requests.get(url_getEipList, headers={'Accept-Encoding': 'identity'})
    for eip in  json.loads(request.text)['EipAddresses']['EipAddress']:
        eipList.append([eip['AllocationId'],eip['IpAddress']])
        if eip['InstanceId'] == aliyun.instance_id:
            having_binding_eip =  eip['AllocationId']

    #解绑EIP
    payload_unlash = {
        'Action': "UnassociateEipAddress",
        'AllocationId': having_binding_eip,
        'InstanceId': aliyun.instance_id
    }

    #绑定EIP
    payload_bind = {
        'Action': 'AssociateEipAddress',
        'AllocationId': eipList[eipIndex-1][0],
        'InstanceId': aliyun.instance_id
    }
    url_bind = aliyun.make_url(payload_bind)
    url_unlash = aliyun.make_url(payload_unlash)
    request1 = requests.get(url_unlash, headers={'Accept-Encoding': 'identity'})
    time.sleep(2)
    request2 = requests.get(url_bind, headers={'Accept-Encoding': 'identity'})

    # print request1.text
    # print request2.text
    # print "vpn_index:   " + str(vpnID)
    # print "ecs_index:   " + str(ecsIndex)
    # print "ecs_id:      " + aliyun.instance_id
    # print "ip_index:    " + str(eipIndex)
    # print "ip_address:  " + eipList[eipIndex-1][1]

def switch():
    for i in trange(1,19):
        for j in range(1,4):
            try:
                swichIp(i,j,j)      #swichIp(第几个ali账号，第几个ip，第几个服务器)
            except:
                continue