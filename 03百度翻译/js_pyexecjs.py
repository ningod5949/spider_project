import execjs
import os

# jscript = execjs.get()
# print(jscript)


# 简单
# res = execjs.eval('1+2')
# print(res)


# 复杂
# js_script = """
# function add(x,y){
#     return x + y;
#     }"""
# ctx = execjs.compile(js_script)
# res = ctx.call('add', 1, 3)
# print(res)


# 外部
# js_script = open('2.js').read()
# ctx = execjs.compile(js_script)
# res = ctx.call('e', 'word')
# print(res)