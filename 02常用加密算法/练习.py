# from Cryptodome.Cipher import DES
# #
# #
# # key = b'12345678'
# # cipher = DES.new(key, DES.MODE_OFB)
# # data = '白'.encode()
# # msg = cipher.encrypt(data)
# # print(msg)
# # cipher2 = DES.new(key, DES.MODE_OFB,iv=cipher.iv)
# # res = cipher2.decrypt(msg)
# # print(res.decode('utf-8'))


# from Cryptodome.Cipher import DES3
#
# key = b'123456781234567212345671'
# cipher = DES3.new(key, DES3.MODE_CFB)
# data = 'bai'.encode()
# msg = cipher.encrypt(data)
# print(msg)
# cipher2 = DES3.new(key, DES3.MODE_CFB, iv=cipher.iv)
# res = cipher2.decrypt(msg)
# print(res.decode('utf-8'))

# from Cryptodome.Cipher import AES
#
# key = b'1234567812345678'
# cipher = AES.new(key, AES.MODE_EAX)
# data = 'bai'.encode()
# msg = cipher.encrypt(data)
# print(msg)
#
# cipher2 = AES.new(key, AES.MODE_EAX, nonce=cipher.nonce)
# res = cipher2.decrypt(msg)
# print(res.decode('utf-8'))

# from Cryptodome.PublicKey import RSA
# from Cryptodome.Cipher import PKCS1_OAEP

# def generate():
#     key = RSA.generate(1024)
#     private_key = key.export_key()
#     with open('private_key.pem', 'wb') as f:
#         f.write(private_key)
#     public_key = key.publickey().export_key()
#     with open('public_key.pem', 'wb') as f:
#         f.write(public_key)
#
# def encrypt(data):
#     public_key = RSA.import_key(open('public_key.pem').read())
#     cipher = PKCS1_OAEP.new(public_key)
#     msg = cipher.encrypt(data.encode())
#     print(msg)
#     return msg
#
# def decrypt(msg):
#     private_key = RSA.import_key(open('private_key.pem').read())
#     cipher = PKCS1_OAEP.new(private_key)
#     res = cipher.decrypt(msg)
#     print(res.decode('utf-8'))
#
# generate()
# data = '白'
# msg = encrypt(data)
# decrypt(msg)

# data = '今天星期五'.encode()
#
# # 网上收到的n值
# pubkey_n = '8d7e6949d411ce14d7d233d7160f5b2cc753930caba4d5ad24f923a505253b9c39b09a059732250e56c594d735077cfcb0c3508e9f544f101bdf7e97fe1b0d97f273468264b8b24caaa2a90cd9708a417c51cf8ba35444d37c514a0490441a773ccb121034f29748763c6c4f76eb0303559c57071fd89234d140c8bb965f9725'
#
# pubkey = RSA.RsaKey(n=int(pubkey_n, 16), e=65537)
# cipher = PKCS1_OAEP.new(pubkey)
# msg = cipher.encrypt(data)
# print(msg)

# import hashlib
#
# data = '白'.encode()
# msg = hashlib.md5(data)
# print(msg)
# print(msg.hexdigest())
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-06-21 16:01:24
# Project: novel_spider

#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-06-21 16:01:24
# Project: novel_spider

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://www.booktxt.net/8_8348/', callback=self.index_page, validate_cert=False)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        res = response.doc('dl dd a')
        titles = [title.text  for title in res]
        urls = [url.attr.href for url in res.items()]
        print(titles[8:])
        for i in range(8, len(urls)):
            self.crawl(urls[i], callback=self.detail_page, validate_cert=False, save={'title':titles[i]})

    @config(priority=2)
    def detail_page(self, response):
        content = response.doc('div[id="content"]').text()
        return {
        'title': response.save['title'],
        'content': content,
        }