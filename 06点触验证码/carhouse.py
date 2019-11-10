import time
import random
import requests
from io import BytesIO
from PIL import Image
from selenium import webdriver
from chaojiying import Chaojiying_Client


USERNAME = '12345678'
PASSWORD = '12345678'
SOFT_ID = '900286'
CHAPTCHA_CYPE = '9004'

class CarHouse:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.chaojiying = Chaojiying_Client(USERNAME, PASSWORD, SOFT_ID)
        self.slider = None

    def login(self):
        self.driver.get('https://account.autohome.com.cn/')
        res = self.check_captcha()
        if res:
            print('校验成功')
        else:
            print('校验失败')

    def check_captcha(self):
        # 点击按钮触发验证码
        self.driver.find_element_by_xpath('//*[@id="embed-captcha"]/div/div[3]').click()
        time.sleep(1)
        # 区分是什么类型的验证码
        img = self.driver.find_elements_by_xpath('//img[@class="geetest_item_img"]')
        # 超级鹰检验结果
        data = None
        if img:
            img = img[0]
            # 下载验证码
            img_url = img.get_attribute('src')
            img_content = requests.get(img_url).content
            # 识别验证码
            data = self.chaojiying.PostPic(img_content, CHAPTCHA_CYPE)
            if data['err_no'] == 0:
                points = data['pic_str'].split('|')
                # 根据识别结果模拟点击
                for point in points:
                    x, y = point.split(',')
                    webdriver.ActionChains(self.driver).move_to_element_with_offset(img, xoffset=int(x), yoffset=int(y)).click().perform()
                    time.sleep(0.5 + random.random())
                self.driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/div/div/div[3]/a/div').click()
        # 判断是否为滑动验证码
        slider = self.driver.find_elements_by_xpath('//div[@class="geetest_slider_button"]')
        if slider:
            self.slider = slider[0]
            # 获取验证码完整背景图片
            full_image = self.get_full_image()
            # full_image.show()
            # 获取有缺口的验证码图片
            cut_image = self.get_cut_image()
            # cut_image.show()
            # 计算需要滑动的距离
            distance = self.get_distance(full_image, cut_image)
            # 计算滑动轨迹
            tracks = self.get_track(distance)
            # 滑动验证码
            self.slide(tracks)
        # 检验结果
        time.sleep(1)
        if self.driver.find_element_by_xpath(
                '//*[@id="embed-captcha"]/div/div[2]/div[2]/div/div[2]/span[1]').text == '验证成功':
            return True
        else:
            # 如果校验错误，通知平台校验错误
            if data:
                self.chaojiying.ReportError(data['pic_id'])
            else:
                print('验证错误')

    def get_full_image(self):
        # 移动到滑动按钮，触发显示完整背景图片
        webdriver.ActionChains(self.driver).move_to_element(self.slider).perform()
        time.sleep(2)
        # 截图
        self.driver.execute_script(
            "document.getElementsByClassName('geetest_canvas_fullbg geetest_fade geetest_absolute')[0].style.display='block'")
        self.driver.execute_script(
            "document.getElementsByClassName('geetest_canvas_fullbg geetest_fade geetest_absolute')[0].style.opacity= '1';")
        image_binary = self.driver.find_element_by_xpath(
            '/html/body/div[3]/div[2]/div[1]/div/div[1]/div[1]/div/a/div[1]/canvas').screenshot_as_png
        return Image.open(BytesIO(image_binary))

    def get_cut_image(self):
        # 左键点击holdon，触发显示有缺口的背景图片
        webdriver.ActionChains(self.driver).click_and_hold(self.slider).perform()
        time.sleep(0.5)
        # 截图
        image_binary = self.driver.find_element_by_xpath(
            '/html/body/div[3]/div[2]/div[1]/div/div[1]/div[1]/div/a/div[1]/div/canvas[1]').screenshot_as_png
        return Image.open(BytesIO(image_binary))

    def get_distance(self, full_image, cut_image):
        full_image.save('full_image.png')
        cut_image.save('cut_image.png')
        # 图片灰度化
        full_image = full_image.convert('L')
        cut_image = cut_image.convert('L')
        # 获取所有像素点
        full_pixels = full_image.load()
        cut_pixels = cut_image.load()
        w, h = full_image.size
        # 先找到活块左上角的那个点
        left = None
        for i in range(100):
            for j in range(h):
                # 判断两张图片的像素点的abs差值，找出不同点
                if abs(full_pixels[i, j] - cut_pixels[i, j]) > 50:
                    left = (i, j)
                    break
            if left:
                break
        # 再找到缺口左上角地那个点
        right = None
        for i in range(left[0] + 60, w):
            for j in range(left[1], h):
                # 判断两张图片的像素点的abs差值，找出不同点
                if abs(full_pixels[i, j] - cut_pixels[i, j]) > 50:
                    right = (i, j)
                    break
            if right:
                break
        # 计算距离
        return right[0] - left[0]

    def get_track(self, distance):
        '''
        拿到移动轨迹，模仿人的滑动行为，先匀加速后匀减速
        匀变速运动基本公式：
        ①v=v0+at
        ②s=v0t+(1/2)at²
        ③v²-v0²=2as
        :param distance: 需要移动的距离
        :return: 存放每0.2秒移动的距离
        '''
        # 初速度
        v = 0
        # 单位时间为0.2s来统计轨迹，轨迹即0.2内的位移
        t = 0.2
        # 位移/轨迹列表，列表内的一个元素代表0.2s的位移
        tracks = []
        # 当前的位移
        current = 0
        # 到达mid值开始减速
        mid = distance * 5 / 8
        distance += 10  # 先滑过一点，最后再反着滑动回来

        # 距离误差缩小到2像素以下
        while abs(distance - current) >= 2:
            if current < mid:
                # 加速度越小，单位时间的位移越小,模拟的轨迹就越多越详细
                a = random.randint(1, 3)  # 加速运动
            else:
                a = -random.randint(2, 4)  # 减速运动
            # 初速度
            v0 = v
            # 0.2秒时间内的位移
            s = v0 * t + 0.5 * a * (t ** 2)
            # 当前的位置
            current += s
            # 添加到轨迹列表
            tracks.append(round(s))
            # 速度已经达到v,该速度作为下次的初速度
            v = v0 + a * t
        # 反着滑动到大概准确位置
        for i in range(4):
            tracks.append(-random.randint(1, 3))
        random.shuffle(tracks)
        return tracks

    def slide(self, tracks):
        for track in tracks:
            webdriver.ActionChains(self.driver).move_by_offset(xoffset=track, yoffset=0).perform()
        time.sleep(0.5 + random.random())
        webdriver.ActionChains(self.driver).release().perform()


if __name__ == '__main__':
    ch = CarHouse()
    ch.login()
