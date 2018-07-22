from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import common
import json


class Upload:
    def __init__(self):
        opt = webdriver.FirefoxOptions()
        # opt.add_argument("-headless")
        self.driver = webdriver.Firefox(executable_path="./geckodriver.exe", options=opt)
        self.driver.get("https://www.bilibili.com/")
        with open("./cookie.txt") as tmp:
            _tmp = json.loads(tmp.read())
            tmp.close()
            for i in _tmp:
                self.driver.add_cookie(i)
        self.driver.get("https://member.bilibili.com/video/upload.html")
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.NAME, 'file')))
        index = self.driver.find_element_by_name("file")
        index.send_keys("hello.mp4")


if __name__ == "__main__":
    u = Upload()

