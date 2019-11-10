from selenium import webdriver
from PIL import Image
from io import BytesIO
import time
import random

class HuXiu:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.driver.get('https://www.huxiu.com/')
        self.driver.find_element_by_xpath('//*[@id="top"]/div/ul[2]/li[3]/a').click()
        self.slider = None


    def login(self):
        self.slider = self.driver.find_element_by_xpath('//*[@id="login-modal"]/div/div/div/div[2]/div[1]/div[2]/div[1]/div/div[3]/div[2]')
        # 获取验证码完整背景图片
        full_image = self.get_full_image()
        # full_image.show()
        # 获取有缺口的验证码图片
        cut_image = self.get_cut_image()
        # cut_image.show()
        # 计算需要滑动的距离
        distance = self.get_distance(full_image, cut_image)
        print(distance)
        # 计算滑动轨迹
        # tracks = self.get_tracks(distance)
        # 滑动验证码
        res = self.slide(distance)
        if res:
            print('登录成功')

    def get_full_image(self):
        # 移动到滑动按钮，触发显示完整背景图片
        webdriver.ActionChains(self.driver).move_to_element(self.slider).perform()
        time.sleep(0.5)
        # 截图
        image_binary = self.driver.find_element_by_xpath('//*[@id="login-modal"]/div/div/div/div[2]/div[1]/div[2]/div[1]/div/div[1]/div[2]/div[1]/a[2]').screenshot_as_png
        return Image.open(BytesIO(image_binary))

    def get_cut_image(self):
        # 左键点击holdon，触发显示有缺口的背景图片
        webdriver.ActionChains(self.driver).click_and_hold(self.slider).perform()
        time.sleep(0.5)
        # 截图
        image_binary = self.driver.find_element_by_xpath(
            '//*[@id="login-modal"]/div/div/div/div[2]/div[1]/div[2]/div[1]/div/div[1]/div[2]/div[1]/a[1]').screenshot_as_png
        return Image.open(BytesIO(image_binary))

    def get_distance(self, full_image, cut_image):
        full_image.save('full_image.png')
        cut_image.save('cut_image.png')

        full_pixels = full_image.load()
        cut_pixels = cut_image.load()
        w,h = full_image.size
        left = None
        # 先找到活块左上角的那个点
        for i in range(100):
            for j in range(h):
                # 判断两张图片的像素点的abs差值，找出不同点
                if abs(full_pixels[i, j][0] - cut_pixels[i, j][0]) + abs(full_pixels[i, j][1] - cut_pixels[i, j][1]) + abs(full_pixels[i, j][2] - cut_pixels[i, j][2]) > 150:
                    left = (i, j)
                    break
            if left:
                break
        # 再找到缺口左上角地那个点
        right = None
        for i in range(left[0]+60, w):
            for j in range(left[1], h):
                # 判断两张图片的像素点的abs差值，找出不同点
                if abs(full_pixels[i, j][0] - cut_pixels[i, j][0]) + abs(
                        full_pixels[i, j][1] - cut_pixels[i, j][1]) + abs(
                        full_pixels[i, j][2] - cut_pixels[i, j][2]) > 150:
                    right = (i, j)
                    break
            if right:
                break
        # 计算距离
        return right[0] - left[0]

    def get_tracks(self, distance):
        pass

    def slide(self, distance):
        webdriver.ActionChains(self.driver).move_by_offset(xoffset=distance,yoffset=0).perform()
        time.sleep(0.5 + random.random())
        webdriver.ActionChains(self.driver).release().perform()
        res = self.driver.find_element_by_xpath('//*[@id="login-modal"]/div/div/div/div[2]/div[1]/div[2]/div[1]/div/div[1]/div[2]/div[2]/div/div[2]/span[1]')
        if res.text == '验证通过':
            return True
        else:
            return False

if __name__ == '__main__':
    hx = HuXiu()
    hx.login()