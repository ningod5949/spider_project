import time
import re
import json
import binascii
import base64
from urllib import parse
import urllib3
from urllib3.exceptions import InsecureRequestWarning

import requests
from Cryptodome.Cipher import PKCS1_v1_5
from Cryptodome.PublicKey import RSA


def crypt_username(username):
    temp = parse.quote(username)        # 将字符进行url编码
    res = base64.b64encode(temp.encode())
    return res.decode('utf-8')

def crypt_password(password, pubkey):
    public_key = RSA.RsaKey(n=int(pubkey, 16), e=65537)
    cipher = PKCS1_v1_5.new(public_key)
    res =cipher.encrypt(password.encode())
    return binascii.b2a_hex(res).decode()


# 创建一个浏览器对象
session = requests.Session()
# 伪装
session.headers.update({ 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'})
session.verify = False
urllib3.disable_warnings(InsecureRequestWarning)
# 请求首页面, 为了获取cookie
session.get('https://weibo.com')
# print(session.cookies)
# 请求prelogin 获取响应内容
params = {
    'entry': 'weibo',
    'callback': 'sinaSSOController.preloginCallBack',
    'su': '',
    'rsakt': 'mod',
    'client': 'ssologin.js(v1.4.19)',
    '_': int(time.time() * 1000)
}
res = session.get('https://login.sina.com.cn/sso/prelogin.php', params=params)
# print(res.text)
# data = re.findall(r'\((.*?)\)', res.text)[0]
data = json.loads(re.findall(r'\((.*?)\)', res.text)[0])
# print(data)
# 获取验证码
url = 'https://login.sina.com.cn/cgi/pin.php?r=97751468&s=0&p=yf-3b6c72d288bcaa01c634390723492bd174f8'
res = session.get(url).content
with open('test.jpg', 'wb') as f:
    f.write(res)
door = input('请输入验证码')
login_data = {
    'entry': 'weibo',
    'gateway': '1',
    'from': '',
    'savestate': '7',
    'qrcode_flag': 'false',
    'useticket': '1',
    'pagerefer': '',
    'vsnf': 1,
    'door': door,
    'su': crypt_username('18341346135'),
    'service': 'miniblog',
    'servertime': data['servertime'],
    'nonce': data['nonce'],
    'pwencode': 'rsa2',
    'rsakv': data['rsakv'],
    'sp': crypt_password(str(data['servertime']) + '\t' + data['nonce'] + '\n' + '050616xnx',data['pubkey']),
    'sr': '1920*1080',
    'encoding': 'UTF-8',
    'prelt': '49',
    'url': 'https://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
    'returntype': 'META'
}
# 校验用户名和密码
response = session.post('https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)', data=login_data)
response.encoding = 'gbk'
# print(response.text)

# 获取重定向的URL
redirect_url = re.findall(r'replace\("(.*?)"\)',response.text)[0]
# print(redirect_url)
# print(parse.unquote(redirect_url, encoding='gbk'))

# 再次重定向
response = session.get(redirect_url)
response.encoding = 'gbk'
print(response.text)

# 获取URL列表
urls = re.findall(r'"arrURL":(\[.*?\])',response.text)[0]
urls = json.loads(urls)
# print(urls)
# print(urls)
res1 = session.get(urls[0])
# print(res1.text)
# print('-'*100)
res2 = session.get(urls[1])
# print(res2.text)
# print('-'*100)
res3 = session.get(urls[2])
# print(res3.text)
# print('-'*100)
res4 = session.get(urls[3])
# print(res4.text)

# 跳转到微博登录的首页
home_response = session.get('https://weibo.com/?wvr=5&lf=reg',verify=False)
# home_response = session.get('https://weibo.com/',verify = False)
home_response.encoding= 'utf-8'
print(home_response.url)