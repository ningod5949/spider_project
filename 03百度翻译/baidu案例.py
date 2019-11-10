import execjs
import re
import requests


def get_sign(word):
    ctx = execjs.compile(open('2.js').read())
    res = ctx.call('e', word)
    return res
session = requests.Session()
session.verify = False
session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'})
index_response = session.get('https://fanyi.baidu.com/')
index_response = session.get('https://fanyi.baidu.com/')
index_response.encoding = 'utf-8'
# print(index_response.text)
token = re.findall(r"token: '(.*?)'", index_response.text)[0]
gtk = re.findall((r"window.gtk = '(.*?)'"), index_response.text)[0]
word = input('请输入你要查询的单词：')
form_data = {
    'from': 'en',
    'to': 'zh',
    'query': word,
    'transtype': 'translang',
    'simple_means_flag': '3',
    'sign': get_sign(word),
    'token': token,
}
res = session.post('https://fanyi.baidu.com/v2transapi', data=form_data)

res = res.content.decode('unicode-escape')
# print(res)
content = re.findall(r'"data":\[{"dst":"(.*?)","prefixWrap":.*?"src":".*?"",', res)[0]
print(content)