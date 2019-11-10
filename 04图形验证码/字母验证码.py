import pytesseract
from PIL import Image


class Captcha:
    def __init__(self, img_file=None):
        if img_file:
            self.img = Image.open(img_file)
        else:
            self.img = img_file

    def convert_two_value(self):
        # 增强对比度
        self.img = self.img.point(lambda x: x * 1.2)
        # 获取尺寸
        w, h = self.img.size
        # 灰度化
        self.img = self.img.convert('L')
        # 获取所有的像素点
        pixels = self.img.load()
        total = []
        for i in range(w):
            for j in range(h):
                total.append(pixels[i, j])
        # 计算平均值
        avg = sum(total) // len(total)
        self.img = self.img.point(lambda x: 0 if x < avg else 255)

    def noise_reduction(self):
        w, h = self.img.size
        pixels = self.img.load()
        # 先处理四边
        # 顶边
        for i in range(w):
            pixels[i, 0] = 255
        # 底边
        for i in range(w):
            pixels[i, h-1] = 255
        # 左边
        for i in range(h):
            pixels[0, i] = 255
        # 右边
        for i in range(h):
            pixels[w-1, i] = 255
        # 处理其他点
        for i in range(1, w-1):
            for j in range(1, h-1):
                sum = pixels[i, j-1] + pixels[i, j + 1] + pixels[i-1, j] + pixels[i+1, j] + pixels[i-1, j-1] + pixels[i-1, j+1] + pixels[i+1, j-1] + pixels[i+1, j+1]
                if sum // 255 > 5:
                    pixels[i, j] = 255
    def image_to_string(self):
        self.convert_two_value()
        self.noise_reduction()
        self.img.show()
        return pytesseract.image_to_string(self.img)

if __name__ == '__main__':
    img_path = input('输入你要识别的验证码路径》》：').strip()
    ctp = Captcha(img_path)
    res = ctp.image_to_string()
    print(res)
    # res = Image.open('1.jpg')
    # res.show()