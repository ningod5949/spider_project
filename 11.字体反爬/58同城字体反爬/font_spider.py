import re
import base64
import json
import requests
from fontTools.ttLib import TTFont
from base_map import base_map


def make_font_file(base64_string):
    '''创建字体文件'''
    bin_data = base64.decodebytes(base64_string.encode())
    with open('new.ttf', 'wb') as f:
        f.write(bin_data)
    return bin_data

# old_font = TTFont('old.ttf')
# old_font.saveXML('old.xml')

# new_font = TTFont('new.tff')
# new_font.saveXML('new.xml')
# print(old_font['glyf']['uniE013'] == new_font['glyf']['uniE325'])
# print(new_font['glyf']['uniE325'])

# 1.首先下载一个字体文件作为基准，根据这个文件生成一个基准的编码和文字的映射
def get_base_map():
    '''手动生成映射关系'''
    data = {}
    font = TTFont('old.ttf')
    names = font.getGlyphOrder()

    for name in names[2:]:
        data[name] = ''

    with open('base_map.py', 'w', encoding='utf-8') as f:
        dict_str = json.dumps(data, indent=4)
        f.write('base_map = ')
        f.write(dict_str)

if __name__ == '__main__':
    # get_base_map()
    # 2.访问页面，拿到字体数据
    session = requests.Session()
    session.headers.update(
        {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'}
    )
    # response = session.get('https://tl.58.com/qzjishuzongjian/?PGTID=0d202409-01a4-9491-9724-0cbade5da0bc&ClickID=4')
    response = session.get('https://tl.58.com/qzjishuzhichi/?PGTID=0d3033a6-01a4-9cd9-5a1b-68a8937c05cc&ClickID=5')
    html = response.text
    font_str = re.findall(r'base64,(.*?)\)  format\("woff"\)', html, re.S)[0]
    # print(font_str)
    # 3.解码字体数据 ，生成字体文件
    make_font_file(font_str)
    # 4.根据已有的基准字体文件和映射生成新的编码文字映射
    new_map = {}
    new_font = TTFont('new.ttf')
    # new_font.saveXML('new.xml')
    keys = new_font.getGlyphOrder()
    base_font = TTFont('old.ttf')
    for key in keys[2:]:
        for name in base_map:
            # print(name)
            if new_font['glyf'][key] == base_font['glyf'][name]:
                new_map[key] = base_map[name]
    # 5.替换数据中的编码
    for item in new_map:
        old_str = '&#x%s;' % item[-4:].lower()
        print(old_str)
        html = html.replace(old_str, new_map[item])
    print(html)
