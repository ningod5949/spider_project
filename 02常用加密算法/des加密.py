import binascii
from Cryptodome.Cipher import DES


key = b'-8B key-'  # 字节只能是ascii码， key必须是8个字节， 64位
# 创建一个加密对象
# iv 参数需要是一个8字节的二进制数据， 初始化向量
# DES.MODE_OFB 加密模式， 加密解密必须一致
cipher = DES.new(key, DES.MODE_OFB, iv=b'12345678')
# 待加密数据，二进制数据
data = '今天星期四'.encode()
# 加密
msg = cipher.encrypt(data)
print(msg)
# 十六进制字符串
print(binascii.b2a_hex(msg))
# 解密过程
# 创建一个解密对象
cipher2 = DES.new(key, DES.MODE_OFB, iv=b'12345678')
# 解密
res = cipher2.decrypt(msg)
# 解密结果
print(res.decode('utf-8'))