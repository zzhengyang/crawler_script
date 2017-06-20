# coding=utf-8
import requests
from tqdm import trange

from vpn_switch.base_api.ali_base_api import AliyunMonitor


def allocateIp(vpnID):
    aliyun = AliyunMonitor("http://vpc.aliyuncs.com", vpnID, 1)

    # 查询EIP列表
    payload = {
        'Action': 'AllocateEipAddress',
        'RegionId': aliyun.region_id,
        'Bandwidth': 20,
        'InternetChargeType': 'PayByTraffic'
    }
    url_allocate = aliyun.make_url(payload)
    request = requests.get(url_allocate, headers={'Accept-Encoding': 'identity'})

def allocate():
    for proxyId in trange(1,19):
        aliyun = AliyunMonitor("http://vpc.aliyuncs.com", proxyId, 1)
        for j in range(aliyun.eipNum):
            allocateIp(proxyId)

