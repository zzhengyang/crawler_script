# coding=utf-8
import json


import requests
import time
from vpn_switch.ali_base_api import AliyunMonitor



def swichIp(vpnID,eipIndex,ecsIndex):


    aliyun = AliyunMonitor("http://vpc.aliyuncs.com", vpnID, ecsIndex)


    #查询可用地区列表
    # payload = {
    #     'Action': 'DescribeRegions'
    # }

    # 查询EIP列表
    payload = {
        'Action': 'DescribeEipAddresses',
        'RegionId': aliyun.region_id,
        'PageSize': 30,
    }
    eipList = []
    having_binding_eip = ''
    url_getEipList = aliyun.make_url(payload)
    request = requests.get(url_getEipList)
    for eip in  json.loads(request.text)['EipAddresses']['EipAddress']:
        eipList.append([eip['AllocationId'],eip['IpAddress']])
        # print eip
        if eip['InstanceId'] == aliyun.instance_id:
            having_binding_eip =  eip['AllocationId']


    # print having_binding_eip


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


    request1 = requests.get(url_unlash)
    time.sleep(2)
    request2 = requests.get(url_bind)


    print request1.text
    print request2.text
    print "vpn_index:   " + str(vpnID)
    print "ecs_index:   " + str(ecsIndex)
    print "ecs_id:      " + aliyun.instance_id
    print "ip_index:    " + str(eipIndex)
    print "ip_address:  " + eipList[eipIndex-1][1]


for i in range(1,3):
    swichIp(5,i,i)      #swichIp(第几个ali账号，第几个ip，第几个服务器)