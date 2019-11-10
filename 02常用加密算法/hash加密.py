import hashlib


# sha1 sha 256 sha 512 md5 使用方法一样
info = '一二三十'.encode()

# 创建一个hash对象
# m = hashlib.md5(info)
m = hashlib.sha512(info)
# hash值
res = m.hexdigest() # 十六进制字符串

print(res)