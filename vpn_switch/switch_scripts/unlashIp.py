# coding=utf-8
import json
import requests
from tqdm import trange
from base_api.ali_base_api import AliyunMonitor


def unlashIp(vpnID):
    aliyun = AliyunMonitor("http://vpc.aliyuncs.com", vpnID, 1)

    # 查询EIP列表
    payload = {
        'Action': 'DescribeEipAddresses',
        'RegionId': aliyun.region_id,
        'PageSize': 30,
    }
    eipList = []
    url_getEipList = aliyun.make_url(payload)
    request = requests.get(url_getEipList, headers={'Accept-Encoding': 'identity'})
    for eip in json.loads(request.text)['EipAddresses']['EipAddress']:
        eipList.append([eip['AllocationId'], eip['IpAddress']])
        if eip['InstanceId']:
            having_binding_eip = eip['AllocationId']
            having_binding_instanceid = eip['InstanceId']

            # 解绑ip
            payload_unlash = {
                'Action': "UnassociateEipAddress",
                'AllocationId': having_binding_eip,
                'InstanceId': having_binding_instanceid

            }
            url_unlash = aliyun.make_url(payload_unlash)
            request1 = requests.get(url_unlash, headers={'Accept-Encoding': 'identity'})

def releaseIp(vpnID):
    aliyun = AliyunMonitor("http://vpc.aliyuncs.com", vpnID, 1)

    # 查询EIP列表
    payload = {
        'Action': 'DescribeEipAddresses',
        'RegionId': aliyun.region_id,
        'PageSize': 30,
    }
    eipList = []
    url_getEipList = aliyun.make_url(payload)
    request = requests.get(url_getEipList, headers={'Accept-Encoding': 'identity'})
    for eip in json.loads(request.text)['EipAddresses']['EipAddress']:
        eipList.append([eip['AllocationId'], eip['IpAddress']])

        having_binding_eip = eip['AllocationId']
        having_binding_instanceid = eip['InstanceId']

        # 解绑ip
        payload_unlash = {
            'Action': "ReleaseEipAddress",
            'AllocationId': having_binding_eip,
        }

        url_unlash = aliyun.make_url(payload_unlash)
        request1 = requests.get(url_unlash, headers={'Accept-Encoding': 'identity'})

def unlash():
    #解绑ip
    for i in trange(1, 19):
        unlashIp(i)
    print "[*] 解绑ip完成.."

def release():
    # 释放ip
    for i in trange(1, 19):
        releaseIp(i)
    print "[*] 释放ip完成.."

