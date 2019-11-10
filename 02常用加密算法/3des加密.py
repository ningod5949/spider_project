from Cryptodome.Cipher import DES3


# 需要24字节的长度的key，一般随机生成
# 本质上就是三次des的key的串联， k1，k2，k3
# 当k1=k2=k3时， des3就是des

key = b'12345678qwertyuiasdfghjk'

# 创建一个密码对象
cipher = DES3.new(key, DES3.MODE_CFB)
# 待加密数据
data = '今天星期四'.encode()

msg = cipher.encrypt(data)

print(msg)

cipher2 = DES3.new(key, DES3.MODE_CFB, iv=cipher.iv)

res = cipher2.decrypt(msg)

print(res.decode('utf-8'))