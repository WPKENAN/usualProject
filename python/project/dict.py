# # # import hashlib
# # # import random
# # # import requests
# # # import time
# # #
# # #
# # # s = requests.Session()
# # # m = hashlib.md5()
# # #
# # # class Dict:
# # #     def __init__(self):
# # #         self.headers = {
# # #             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
# # #             'Referer': 'http://fanyi.youdao.com/',
# # #             'contentType': 'application/x-www-form-urlencoded; charset=UTF-8'
# # #         }
# # #         self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule&sessionFrom='
# # #         self.base_config()
# # #
# # #     def base_config(self):
# # #         """
# # #         设置基本的参数，cookie
# # #         """
# # #         s.get('http://fanyi.youdao.com/')
# # #
# # #     def translate(self,i):
# # #         # i = 'apple'
# # #         salf = str(int(time.time() * 1000) + random.randint(0, 9))
# # #         n = 'fanyideskweb' + i + salf + "rY0D^0'nM0}g5Mm1z%1G4"
# # #         m.update(n.encode('utf-8'))
# # #         sign = m.hexdigest()
# # #         data = {
# # #             'i': i,
# # #             'from': 'AUTO',
# # #             'to': 'AUTO',
# # #             'smartresult': 'dict',
# # #             'client': 'fanyideskweb',
# # #             'salt': salf,
# # #             'sign': sign,
# # #             'doctype': 'json',
# # #             'version': "2.1",
# # #             'keyfrom': "fanyi.web",
# # #             'action': "FY_BY_DEFAULT",
# # #             'typoResult': 'false'
# # #         }
# # #         resp = s.post(self.url, headers=self.headers, data=data)
# # #         return resp.json()
# # #
# # #
# # # while(1):
# # #     dic = Dict()
# # #     word=input("please input your word:")
# # #     resp = dic.translate(word)
# # #     print(resp)
# #
# # # 导入需要的库
# # # import urllib.request
# # # import urllib.parse
# # # import json
# # #
# # #
# # # # 等待用户输入需要翻译的单词
# # # content = input('请输入需要翻译的单词：')
# # #
# # # # 有道翻译的url链接
# # # url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule&sessionFrom=null'
# # #
# # # # 发送给有道服务器的数据
# # # data = {}
# # #
# # # # 需要翻译的文字
# # # data['i'] = content
# # # # 下面这些都先按照我们之前抓包获取到的数据
# # # data['from'] = 'AUTO'
# # # data['to'] = 'AUTO'
# # # data['smartresult'] = 'dict'
# # # data['client'] = 'fanyideskweb'
# # # data['salt'] = '1500349255670'
# # # data['sign'] = '997742c66698b25b43a3a5030e1c2ff2'
# # # data['doctype'] = 'json'
# # # data['version'] = '2.1'
# # # data['keyfrom'] = 'fanyi.web'
# # # data['action'] = 'FY_BY_CL1CKBUTTON'
# # # data['typoResult'] = 'true'
# # #
# # # # 对数据进行编码处理
# # # data = urllib.parse.urlencode(data).encode('utf-8')
# # #
# # # # 创建一个Request对象，把url和data传进去，并且需要注意的使用的是POST请求
# # # request = urllib.request.Request(url=url, data=data, method='POST')
# # # # 打开这个请求
# # # response = urllib.request.urlopen(request)
# # # # 读取返回来的数据
# # # result_str = response.read().decode('utf-8')
# # # # 把返回来的json字符串解析成字典
# # # result_dict = json.loads(result_str)
# # #
# # # # 获取翻译结果
# # # print('翻译的结果是：%s' % result_dict)
# #
# # import urllib.request
# # import urllib.parse
# # import json
# # import time
# # import random
# # import hashlib
# #
# # content = input('请输入需要翻译的句子：')
# #
# # url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule&sessionFrom=https://www.google.com/'
# #
# # data = {}
# #
# # u = 'fanyideskweb'
# # d = content
# # f = str(int(time.time() * 1000) + random.randint(1, 10))
# # c = 'rY0D^0\'nM0}g5Mm1z%1G4'
# #
# # sign = hashlib.md5((u + d + f + c).encode('utf-8')).hexdigest()
# #
# # data['i'] = content
# # data['from'] = 'AUTO'
# # data['to'] = 'AUTO'
# # data['smartresult'] = 'dict'
# # data['client'] = 'fanyideskweb'
# # data['salt'] = f
# # data['sign'] = sign
# # data['doctype'] = 'json'
# # data['version'] = '2.1'
# # data['keyfrom'] = 'fanyi.web'
# # data['action'] = 'FY_BY_CL1CKBUTTON'
# # data['typoResult'] = 'true'
# #
# # data = urllib.parse.urlencode(data).encode('utf-8')
# # request = urllib.request.Request(url=url, data=data, method='POST')
# # response = urllib.request.urlopen(request)
# #
# # print(response.read().decode('utf-8'))
#
# from urllib import request
# from urllib import parse
# import json
#
#
# def translate(content):
#     Request_URL = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
#     Form_Data = {}
#     Form_Data['i'] = content
#     Form_Data['from'] = 'AUTO'
#     Form_Data['to'] = 'AUTO'
#     Form_Data['smartresult'] = 'dict'
#     Form_Data['client'] = 'fanyideskweb'
#     Form_Data['doctype'] = 'json'
#     Form_Data['version'] = '2.1'
#     Form_Data['keyfrom'] = 'fanyi.web'
#     Form_Data['action'] = 'FY_BY_REALTIME'
#     Form_Data['typoResult'] = 'false'
#     data = parse.urlencode(Form_Data).encode('utf-8')
#     response = request.urlopen(Request_URL, data)
#     html = response.read().decode('utf-8')
#     translate_results = json.loads(html)
#     return translate_results
#     # translate_results = translate_results['translateResult'][0][0]['tgt']
#     # return translate_results
#
# while(1):
#     result = translate(input("请输入要翻译的英文:"))
#     print("翻译的结果是:%s" % result)
#

# import requests # 导入requests包
# from bs4 import BeautifulSoup
# r = requests.get('http://www.youdao.com/') # 向有道词典请求资源
# html = r.text
# soup = BeautifulSoup(html, 'html.parser') # 结构化文本soup
# div = soup.find(name='div', attrs={'class': 'trans-container'}) # 获取中文释义所在的标签
# print(div.get_text()) # 获取标签内文本

import requests # 导入requests包
import json
while(1):
    word=input("please input you word:")
    url='http://dict.youdao.com/w/%s'%(word)
    r = requests.get(url) # 向有道词典请求资源
    html = r.text
    print(len(html))
    result=json.loads(html)
    print(result)
