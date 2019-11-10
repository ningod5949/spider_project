from Cryptodome.Cipher import AES

# 16个字节的密钥
key = b'1234567812345678'

cipher = AES.new(key, AES.MODE_EAX)

data = '今天星期四'.encode()

msg = cipher.encrypt(data)
print(msg)

# 解密
cipher2 = AES.new(key, AES.MODE_EAX, nonce=cipher.nonce)
res = cipher2.decrypt(msg)
print(res.decode('utf-8'))