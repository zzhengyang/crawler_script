# coding=utf-8

import base64
import hmac
from hashlib import sha1
import urllib
import time
import uuid
ALIYUN_ACCESS_KEY={1:{"ALIYUN_ACCESS_KEY_ID":"LTAIzVwnVCDXWtYs",    #ranupay
                      "ALIYUN_ACCESS_KEY_SECRET":"aJ1Dia3QtVHd9EbVj5MrYh3yTmr1kc",
                      "ALIYUN_REGION_ID":"cn-qingdao",
                      "ALIYUN_INSTANCE_ID":{1:"i-m5e8854sx0c71sagmups",2:"i-m5e20gz8zjy88jwb6q6z",3:"i-m5ejevtfmojhmptr4k0n"}},
                   2:{"ALIYUN_ACCESS_KEY_ID":"LTAIzVwnVCDXWtYs",
                      "ALIYUN_ACCESS_KEY_SECRET":"aJ1Dia3QtVHd9EbVj5MrYh3yTmr1kc",
                      "ALIYUN_REGION_ID":"cn-beijing",
                      "ALIYUN_INSTANCE_ID":{1:"i-2zeetdy0c3fjxosk84lr",2:"i-2zecvee05xzn649uebc8",3:"i-2zeal4j7nw1qlg63gd84"}},
                   3:{"ALIYUN_ACCESS_KEY_ID":"LTAIzVwnVCDXWtYs",
                      "ALIYUN_ACCESS_KEY_SECRET":"aJ1Dia3QtVHd9EbVj5MrYh3yTmr1kc",
                      "ALIYUN_REGION_ID":"cn-hangzhou",
                      "ALIYUN_INSTANCE_ID":{1:"i-bp1h8nr0sr6x7hpq9aeg",2:"i-bp17avth9xef92p3llxc",3:"i-bp1hij0ha9ma5zlolwni"}},
                   4:{"ALIYUN_ACCESS_KEY_ID":"LTAIzVwnVCDXWtYs",
                      "ALIYUN_ACCESS_KEY_SECRET":"aJ1Dia3QtVHd9EbVj5MrYh3yTmr1kc",
                      "ALIYUN_REGION_ID":"cn-shanghai",
                      "ALIYUN_INSTANCE_ID":{1:"i-uf6i9dn3ri2v4oa9ef9e",2:"i-uf67yj3jp885mwmfgcyo",3:"i-uf626lnzvkib3yshr2ru"}},
                   5:{"ALIYUN_ACCESS_KEY_ID":"LTAIzVwnVCDXWtYs",
                      "ALIYUN_ACCESS_KEY_SECRET":"aJ1Dia3QtVHd9EbVj5MrYh3yTmr1kc",
                      "ALIYUN_REGION_ID":"cn-shenzhen",
                      "ALIYUN_INSTANCE_ID":{1:"i-wz908a551s29u21orshl",2:"i-wz9f7qdocvjpfn0mbsfy",3:"i-wz9ddnvx1jmh9o5pde2s"}},
                   6:{"ALIYUN_ACCESS_KEY_ID":"LTAIzVwnVCDXWtYs",
                      "ALIYUN_ACCESS_KEY_SECRET":"aJ1Dia3QtVHd9EbVj5MrYh3yTmr1kc",
                      "ALIYUN_REGION_ID":"cn-zhangjiakou",
                      "ALIYUN_INSTANCE_ID":{1:"i-8vbe7yd3ei8td6283244",2:"i-8vbe7yd3ei8td6283245"}},
                   7: {"ALIYUN_ACCESS_KEY_ID": "LTAIPQEnUD9Qtahh",  #ran2upay
                      "ALIYUN_ACCESS_KEY_SECRET": "Ud7kcXiIaQFLLM2UwXkIz4jt6L188M",
                      "ALIYUN_REGION_ID":"cn-qingdao",
                      "ALIYUN_INSTANCE_ID":{1:"i-m5eb8w3taij9lcsd4zil",2:"i-m5eboly1pds99h4ifaor",3:"i-m5e1jg36nyosmsl0991p"}},
                   8: {"ALIYUN_ACCESS_KEY_ID": "LTAIPQEnUD9Qtahh",
                      "ALIYUN_ACCESS_KEY_SECRET": "Ud7kcXiIaQFLLM2UwXkIz4jt6L188M",
                      "ALIYUN_REGION_ID":"cn-beijing",
                      "ALIYUN_INSTANCE_ID":{1:"i-2ze5ywngc71w32u8n3zg",2:"i-2ze0hmidzgm33lb1cu4n",3:"i-2zeal4j7nw1qlk45oh6k"}},
                   9: {"ALIYUN_ACCESS_KEY_ID": "LTAIPQEnUD9Qtahh",
                      "ALIYUN_ACCESS_KEY_SECRET": "Ud7kcXiIaQFLLM2UwXkIz4jt6L188M",
                      "ALIYUN_REGION_ID":"cn-hangzhou",
                      "ALIYUN_INSTANCE_ID":{1:"i-bp176helaylvn1l47k4s",2:"i-bp1eveoleb7xjxfnxrcs",3:"i-bp1eqcfinqjvg7klbte9"}},
                   10: {"ALIYUN_ACCESS_KEY_ID": "LTAIPQEnUD9Qtahh",
                      "ALIYUN_ACCESS_KEY_SECRET": "Ud7kcXiIaQFLLM2UwXkIz4jt6L188M",
                      "ALIYUN_REGION_ID":"cn-shanghai",
                      "ALIYUN_INSTANCE_ID":{1:"i-uf6cvee05xzn6g412n7f",2:"i-uf60hmidzgm33lb1cu4q",3:"i-uf653nglzx9je328zk3t"}},
                   11: {"ALIYUN_ACCESS_KEY_ID": "LTAIPQEnUD9Qtahh",
                      "ALIYUN_ACCESS_KEY_SECRET": "Ud7kcXiIaQFLLM2UwXkIz4jt6L188M",
                      "ALIYUN_REGION_ID":"cn-shenzhen",
                      "ALIYUN_INSTANCE_ID":{1:"i-wz910ewtx50ojtcd6yrt",2:"i-wz96lk3rekg2tnj4zpxz",3:"i-wz91rzo7o5ca3jmpdoj7"}},
                   12: {"ALIYUN_ACCESS_KEY_ID": "LTAIPQEnUD9Qtahh",
                      "ALIYUN_ACCESS_KEY_SECRET": "Ud7kcXiIaQFLLM2UwXkIz4jt6L188M",
                      "ALIYUN_REGION_ID":"cn-zhangjiakou",
                      "ALIYUN_INSTANCE_ID":{1:"i-8vbe7yd3ei8tda0ab62i",2:"i-8vbd2mcrddbwfye90chm"}},
                   13: {"ALIYUN_ACCESS_KEY_ID": "LTAIwzSbNn2egrY6",  #ran3upay
                      "ALIYUN_ACCESS_KEY_SECRET": "rQfL3k7Jw8aEUWFglGsNCykmBPInKj",
                      "ALIYUN_REGION_ID":"cn-qingdao",
                      "ALIYUN_INSTANCE_ID":{1:"i-m5e0hmidzgm33r84p02e",2:"i-m5eg60mbrgzekgj2rf1l",3:"i-m5e13qvinee6nbfbalbp"}},
                   14: {"ALIYUN_ACCESS_KEY_ID": "LTAIwzSbNn2egrY6",
                      "ALIYUN_ACCESS_KEY_SECRET": "rQfL3k7Jw8aEUWFglGsNCykmBPInKj",
                      "ALIYUN_REGION_ID":"cn-beijing",
                      "ALIYUN_INSTANCE_ID":{1:"i-2ze20gz8zjy891nl77zw",2:"i-2ze1jtxhlmhe50otoruv",3:"i-2ze1jg36nyosmuk1db10"}},
                   15: {"ALIYUN_ACCESS_KEY_ID": "LTAIwzSbNn2egrY6",
                      "ALIYUN_ACCESS_KEY_SECRET": "rQfL3k7Jw8aEUWFglGsNCykmBPInKj",
                      "ALIYUN_REGION_ID":"cn-hangzhou",
                      "ALIYUN_INSTANCE_ID":{1:"i-bp143t8c42mpl26feoes",2:"i-bp110ewtx50ojz9gj4ph",3:"i-bp18ifnmtig5iheymaz7"}},
                   16: {"ALIYUN_ACCESS_KEY_ID": "LTAIwzSbNn2egrY6",
                      "ALIYUN_ACCESS_KEY_SECRET": "rQfL3k7Jw8aEUWFglGsNCykmBPInKj",
                      "ALIYUN_REGION_ID":"cn-shanghai",
                      "ALIYUN_INSTANCE_ID":{1:"i-uf6adnu5foycf4066aq8",2:"i-uf643t8c42mpl26feoev",3:"i-uf69v5411zjnh8xfwwqj"}},
                   17: {"ALIYUN_ACCESS_KEY_ID": "LTAIwzSbNn2egrY6",
                      "ALIYUN_ACCESS_KEY_SECRET": "rQfL3k7Jw8aEUWFglGsNCykmBPInKj",
                      "ALIYUN_REGION_ID":"cn-shenzhen",
                      "ALIYUN_INSTANCE_ID":{1:"i-wz908a551s29uhtxo8b9",2:"i-wz90hmidzgm33r84p02g",3:"i-wz9ao1kipmybijm2t347"}},
                   18: {"ALIYUN_ACCESS_KEY_ID": "LTAIwzSbNn2egrY6",
                      "ALIYUN_ACCESS_KEY_SECRET": "rQfL3k7Jw8aEUWFglGsNCykmBPInKj",
                      "ALIYUN_REGION_ID":"cn-zhangjiakou",
                      "ALIYUN_INSTANCE_ID":{1:"i-8vbe7yd3ei8tddycja0w",2:"i-8vbe7yd3ei8tddycja0x"}},
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
        self.eipNum = len(ALIYUN_ACCESS_KEY[vpnID]['ALIYUN_INSTANCE_ID'])

    # 签名
    def sign(self, accessKeySecret, parameters):
        sortedParameters = sorted(parameters.items(), key=lambda parameters: parameters[0])
        canonicalizedQueryString = ''

        for (k, v) in sortedParameters:
            canonicalizedQueryString += '&' + self.percent_encode(k) + '=' + self.percent_encode(v)

        stringToSign = 'GET&%2F&' + self.percent_encode(canonicalizedQueryString[1:])

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

        url = self.url + "/?" + urllib.urlencode(parameters)
        return url