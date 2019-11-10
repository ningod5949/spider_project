# coding:utf-8

import re
import requests
from fontTools.ttLib import TTFont
from lxml import etree

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/66.0.3359.139 Safari/537.36 "
}

index_url = 'http://maoyan.com/'
# 获取首页内容
response_index = requests.get(index_url, headers=headers).text
index_xml = etree.HTML(response_index)
info_list = index_xml.xpath('//*[@id="app"]/div/div[1]/div[1]/div/div[2]/ul/li[1]/a/div[2]/div//text()')
a = u'电影名称：%s, 票房总数：%s' % (info_list[1], info_list[4])
print(a)

# 获取字体文件的url
woff_ = re.search(r"url\('(.*\.woff)'\)", response_index).group(1)
woff_url = 'http:' + woff_
response_woff = requests.get(woff_url, headers=headers).content

with open('fonts.woff', 'wb') as f:
    f.write(response_woff)

# base_nums， base_fonts 需要自己手动解析映射关系， 要和basefonts.woff一致
baseFonts = TTFont('basefonts.woff')
base_nums = ['8', '1', '2', '6', '7', '4', '5', '3', '0', '9']
base_fonts = ['uniE2CA', 'uniED0B', 'uniECE8', 'uniF472', 'uniE71C', 'uniED6F', 'uniE63C', 'uniEA6D', 'uniF241',
              'uniEFA4']
onlineFonts = TTFont('fonts.woff')

onlineFonts.saveXML('test.xml')

uni_list = onlineFonts.getGlyphNames()[1:-1]
# uni_list1 = onlineFonts.getGlyphOrder()
# print(uni_list)
# print(uni_list1)
temp = {}
# 解析字体库
for i in range(10):
    onlineGlyph = onlineFonts['glyf'][uni_list[i]]
    for j in range(10):
        baseGlyph = baseFonts['glyf'][base_fonts[j]]
        if onlineGlyph == baseGlyph:
            temp["&#x" + uni_list[i][3:].lower() + ';'] = base_nums[j]

# 字符替换
pat = '(' + '|'.join(temp.keys()) + ')'
print(pat)
print(temp)
response_index = re.sub(pat, lambda x: temp[x.group()] and print(x, x.group(), temp[x.group()]), response_index)
# print(response_index)
# 内容提取
index_xml = etree.HTML(response_index)
info_list = index_xml.xpath('//*[@id="app"]/div/div[1]/div[1]        /div/div[2]/ul/li[1]/a/div[2]/div//text()')
a = u'电影名称：%s, 票房总数：%s' % (info_list[1], info_list[4])
print(a)
