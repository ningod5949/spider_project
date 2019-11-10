import base64
import json
import re
from io import BytesIO, StringIO
import requests
from fontTools.ttLib import TTFont
from lxml import etree

def get_base_map():
    """
    生成手动映射关系
    :return:
    """
    data = {}
    font = TTFont('base.ttf')
    res = font.getGlyphNames()
    for item in res:
        if 'uni' in item:
            data[item] = ''
    with open('base.map.json', 'w', encoding='utf-8') as f:

        json.dump(data, f, indent=4)


def make_font_file(base64_string):
    """
    创建字体文件
    :param base64_string: 页码base编码数据
    :return: 二进制数据
    """
    bin_data = base64.decodebytes(base64_string.encode())
    with open('new.ttf', 'wb') as f:
        f.write(bin_data)
    return bin_data


def convert_font_to_xml(font_bin):
    """
    创建字体xml文件
    :param font_bin:
    :return: font obj
    """
    # ByteIO把一个二进制内存块当成文件来操作，
    font = TTFont(BytesIO(font_bin))
    # 将解码字体保存为xml
    font.saveXML("new.xml")
    return font


def get_map(font):
    """
    生成新的映射关系
    :param font:
    :return: map
    """
    with open('base.map.json', 'r', encoding='utf-8') as f:

        base_map = json.load(f)

    map = {}

    base_font = TTFont('base.ttf')

    for name in font.getGlyphNames():
        if 'uni' in name:
            new_obj = font['glyf'][name]
            for base_name in base_font.getGlyphNames():
                if 'uni' in base_name:
                    old_obj = base_font['glyf'][base_name]
                    if new_obj == old_obj:
                        map[name] = base_map[base_name]

    return map


if __name__ == '__main__':
    session = requests.Session()
    session.headers.update({'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'})

    # 1.请求页面
    response = session.get('https://bj.58.com/qzyewu/?PGTID=0d202409-0000-1aa8-92da-777b90a7dc73&ClickID=1')
    html = response.text

    # 2.解析网页中的字体信息，生成字体文件，和xml文件
    base_str = re.findall(r'base64,(.*?)\)  format\("woff"\)', html, re.S)
    if base_str:
        font_bin = make_font_file(base64_string=base_str[0])
        font = convert_font_to_xml(font_bin)
        # 3.根据basemap生成映射关系
        map = get_map(font)
        print(map)

        # 4.替换页面内容
        for item in map:
            old_str = '&#x%s;' % item[-4:].lower()
            print(old_str)
            html = html.replace(old_str, map[item])

        print(html)