import requests
import re
import base64
import json
from fontTools.ttLib import TTFont


def make_font_file(str, name):
    """
    通过获取的字符串转化为字体文件
    :param str: 网页获取的字符串
    :param name: 为字体取的名字
    :return:
    """
    bin_data = base64.decodebytes(str.encode())
    with open(f'{name}.ttf', 'wb') as f:
        f.write(bin_data)
    return bin_data


if __name__ == '__main__':

    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                          'like Gecko) Chrome/74.0.3729.108 Safari/537.36'})
    res = session.get('https://www.shixiseng.com/interns?k=%E6%95%B0%E6%8D%AE%E5%BA%93&p=2')
    html = res.text
    # print(html)
    # font_str = re.findall(r';base64,(.*?)"\)}', html, re.S)[0]
    url = re.findall(r'font-family:myFont;src:url\((.*?)\)', html)
    url = 'https://www.shixiseng.com' + url[0]
    res = session.get(url).content
    with open('base.ttf', 'wb') as f:
        f.write(res)
    # font_str = re.findall(r";base64,(.*?)'\)", res, re.S)[0]
    # base_font = make_font_file(font_str, 'base')
    old = ['一', '师', '会', '四', '计', '财', '场', '聘', '招', '工', '周', '端', '年', '设', '程', '二', '五', '天', '前', '网', '广', '市',
           '月', '个', '告', '作', '三', '互', '生', '人', '政', '件', '行', '软', '银', '联', '0', '1', '2', '3', '4', '5', '6', '7',
           '8',
           '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
           'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
           'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    new_font = TTFont('base.ttf')
    new_font.saveXML('base.xml')

    keys = new_font.getBestCmap()
    new_map = []
    for key in keys:
        key = hex(key)
        new_map.append(key)
    new_map = ['&#x%s' % i[-4:] for i in new_map[1:]]

    items = [(new_map[i], old[i]) for i in range(len(new_map))]

    for i in range(len(items)):
        html = html.replace(items[i][0], items[i][1])

    print(html)