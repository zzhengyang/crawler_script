# coding=utf-8

import base64
import hmac
from hashlib import sha1
import urllib
import time
import uuid
ALIYUN_ACCESS_KEY={1:{"ALIYUN_ACCESS_KEY_ID":"LTAIzVwnVCDXWtYs",
                      "ALIYUN_ACCESS_KEY_SECRET":"aJ1Dia3QtVHd9EbVj5MrYh3yTmr1kc",
                      "ALIYUN_REGION_ID":"cn-beijing",
                      "ALIYUN_INSTANCE_ID":{1:"i-2ze4lf791ggtd7rbombp",2:"i-2zedpuz8j5uwpg6brs6p"}},
                   2:{"ALIYUN_ACCESS_KEY_ID":"LTAIzVwnVCDXWtYs",
                      "ALIYUN_ACCESS_KEY_SECRET":"aJ1Dia3QtVHd9EbVj5MrYh3yTmr1kc",
                      "ALIYUN_REGION_ID":"cn-zhangjiakou",
                      "ALIYUN_INSTANCE_ID":{1:"i-8vb5awc622gw1qs2rc3k",2:"i-8vb5awc622gw1qs2rc3j"}},
                   3:{"ALIYUN_ACCESS_KEY_ID":"LTAIzVwnVCDXWtYs",
                      "ALIYUN_ACCESS_KEY_SECRET":"aJ1Dia3QtVHd9EbVj5MrYh3yTmr1kc",
                      "ALIYUN_REGION_ID":"cn-hangzhou",
                      "ALIYUN_INSTANCE_ID":{1:"i-bp11wvn1qznwqbuwmfgr",2:"i-bp10lz2c208ax7x0urne"}},
                   4:{"ALIYUN_ACCESS_KEY_ID":"LTAIzVwnVCDXWtYs",
                      "ALIYUN_ACCESS_KEY_SECRET":"aJ1Dia3QtVHd9EbVj5MrYh3yTmr1kc",
                      "ALIYUN_REGION_ID":"cn-shanghai",
                      "ALIYUN_INSTANCE_ID":{1:"i-uf6bcmo5psxy5gbucdph",2:"i-uf62c2jlj63xeyfm88hj"}},
                   5:{"ALIYUN_ACCESS_KEY_ID":"LTAIzVwnVCDXWtYs",
                      "ALIYUN_ACCESS_KEY_SECRET":"aJ1Dia3QtVHd9EbVj5MrYh3yTmr1kc",
                      "ALIYUN_REGION_ID":"cn-shenzhen",
                      "ALIYUN_INSTANCE_ID":{1:"i-wz9bdxlee9u01bbhrv27",2:"i-wz9hinmw0qe086ioa5t4"}}
                   }
                   # 2: {"ALIYUN_ACCESS_KEY_ID": "LTAIPQEnUD9Qtahh",
                   #     "ALIYUN_ACCESS_KEY_SECRET": "Ud7kcXiIaQFLLM2UwXkIz4jt6L188M",
                   #    "ALIYUN_REGION_ID":"cn-beijing",
                   #    "ALIYUN_INSTANCE_ID":{1:"i-2ze8edot52via8h044gr",2:"i-2ze8edot52via8h044gs"}},
                   # 3: {"ALIYUN_ACCESS_KEY_ID": "LTAI71kj9JYZMsPV",
                   #     "ALIYUN_ACCESS_KEY_SECRET": "hxIgK7WK1570Jtrph5nVZHFsrmovL6",
                   #    "ALIYUN_REGION_ID":"cn-shanghai",
                   #    "ALIYUN_INSTANCE_ID":{1:"i-uf623s62asvtcd8s3m04",2:"i-uf623s62asvtcd8s3m05"}},
                   # 4: {"ALIYUN_ACCESS_KEY_ID": "LTAImh0hjJOl7ojl",
                   #     "ALIYUN_ACCESS_KEY_SECRET": "rCS1WBzhDN6Lk64JbaL4hrG6wVGm8f",
                   #    "ALIYUN_REGION_ID":"cn-shenzhen",
                   #    "ALIYUN_INSTANCE_ID":{1:"i-wz9casapedy91198jdkp",2:"i-wz9casapedy91198jdkr"}},
                   # 5: {"ALIYUN_ACCESS_KEY_ID": "LTAI71kj9JYZMsPV",
                   #     "ALIYUN_ACCESS_KEY_SECRET": "hxIgK7WK1570Jtrph5nVZHFsrmovL6",
                   #    "ALIYUN_REGION_ID":"cn-shanghai",
                   #    "ALIYUN_INSTANCE_ID":{1:"i-uf623s62asvtcd8s3m04",2:"i-uf623s62asvtcd8s3m05"}},
                   # }


class AliyunMonitor:
    def __init__(self, url, vpnID,ecsID):
        self.access_id = ALIYUN_ACCESS_KEY[vpnID]['ALIYUN_ACCESS_KEY_ID']
        self.access_secret = ALIYUN_ACCESS_KEY[vpnID]['ALIYUN_ACCESS_KEY_SECRET']
        self.url = url
        self.region_id = ALIYUN_ACCESS_KEY[vpnID]['ALIYUN_REGION_ID']
        self.instance_id = ALIYUN_ACCESS_KEY[vpnID]['ALIYUN_INSTANCE_ID'][ecsID]


    # 签名
    def sign(self, accessKeySecret, parameters):
        sortedParameters = sorted(parameters.items(), key=lambda parameters: parameters[0])
        canonicalizedQueryString = ''

        for (k, v) in sortedParameters:
            canonicalizedQueryString += '&' + self.percent_encode(k) + '=' + self.percent_encode(v)

        stringToSign = 'GET&%2F&' + self.percent_encode(canonicalizedQueryString[1:])    # 使用get请求方法

        h = hmac.new(accessKeySecret + "&", stringToSign, sha1)
        signature = base64.encodestring(h.digest()).strip()
        return signature

    def percent_encode(self, encodeStr):
        encodeStr = str(encodeStr)

        res = urllib.quote(encodeStr.decode('utf-8').encode('utf-8'), '')
        res = res.replace('+', '%20')
        res = res.replace('*', '%2A')
        res = res.replace('%7E', '~')
        return res

    def make_url(self, params):
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        parameters = {
            'Format': 'JSON',
            'Version': '2016-04-28',
            'AccessKeyId': self.access_id,
            'SignatureVersion': '1.0',
            'SignatureMethod': 'HMAC-SHA1',
            'SignatureNonce': str(uuid.uuid1()),
            'Timestamp': timestamp,
        }
        for key in params.keys():
            parameters[key] = params[key]

        signature = self.sign(self.access_secret, parameters)
        parameters['Signature'] = signature

        # return parameters
        url = self.url + "/?" + urllib.urlencode(parameters)
        return url

