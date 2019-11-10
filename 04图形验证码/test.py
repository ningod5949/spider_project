# import pytesseract
from PIL import Image
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# code = pytesseract.image_to_string(image)
# print(code)
image = Image.open('11.jpg')
#
# 文件名
# print(image.filename)

# 文件格式
# print(image.format)

# 文件模式
# print(image.mode)

# 文件大小
# print(image.size)

# 文件宽度
# print(image.width)

# 文件高度
# print(image.height)

# 文件信息
# print(image.info)

# 剪切
# croped_im = image.crop((0, 0, 200, 200))
# croped_im.save('14.jpg')

# 复制
# copy_im = croped_im.copy()
# copy_im.save('13.jpg')

# 粘贴
# croped_im = image.crop((0, 0, 300, 300))
# croped_im.show()
# image.paste(croped_im, (100, 100))
# image.save('12.jpg')

# 调整大小
# resized_im = image.resize((683, 728))
# resized_im.show()

# 调整大小，（制造缩略图）
# w, h = image.size
# image.thumbnail((w//2, h//2))
# image.show()

# 旋转图像
# image = image.rotate(45)
# image.show()
# image = image.rotate(45, expand=100)
# image.show()

# 翻转图像
# image = image.transpose(Image.FLIP_LEFT_RIGHT)
# image.show()
# image = image.transpose(Image.FLIP_TOP_BOTTOM)
# image.show()

# 获取图片通道名称
# image = image.getbands()
# print(image)

# 通过通道切割图片
# R, G, B = image.split()
# R.show()
# G.show()
# B.show()
# print((R, G, B))

# 获取单个通道的图片
# R = image.getchannel('R')
# R.show()

# 模式转化
# image = image.convert('L')
# image.show()

# 获取单个像素值
# image = image.getpixel((100,100))
# print(image)

# 加载图片全部数据
# pixdata = image.load()
# pixdata[1,1] = 255, 255, 255
# image.show()
# print(pixdata)
# print(pixdata[0,0])
# print(type(pixdata[0,1]))
# print([i for x in range(1) for y in range(1) for i in pixdata[x, y]])

# 获取所有像素内容
# image = image.getdata()
# image = image.getdata(band=0)
# image = image.getdata(band=1)
# image = image.getdata(band=2)
# print(image)
# print(list(image)[0])

# 关闭图片
image.show()
image.close()