import binascii
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP  # RSA算法的填充方法

# 生成密钥对
def generate_key():
    key = RSA.generate(1024)        # 1024位数
    private_key = key.export_key()  # 私钥
    print(private_key)
    with open('private_key.pem', 'wb') as f:
        f.write(private_key)

    public_key = key.publickey().export_key() # 公钥
    print(public_key)
    with open('public_key.pem', 'wb') as f:
        f.write(public_key)


# 加密
def encrypt(data):
    # 导入公钥
    public_key = RSA.import_key(open('public_key.pem').read())
    # print(public_key.e)
    # print(public_key.n)
    # print(public_key)
    cipher = PKCS1_OAEP.new(public_key)
    # 加密
    msg = cipher.encrypt(data)
    return msg

# print(encrypt('今天星期五'.encode()))
msg = encrypt('今天星期五'.encode())
# print(binascii.b2a_hex(encrypt('今天星期五'.encode())))

# 解密
def decrypt(data):
    # 导入私钥
    private_key = RSA.import_key(open('private_key.pem').read())
    cipher = PKCS1_OAEP.new(private_key)
    res = cipher.decrypt(data)
    return res

# print(decrypt(msg).decode('utf_8'))