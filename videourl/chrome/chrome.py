# coding:utf-8
from urllib import request
import re
from selenium import webdriver
import json
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import io
import gzip
import down
import os
import time

"""
https://www.bilibili.com/video/av19890612#page=2
"""


def dezip(source, *, codeform="utf-8"):
    if source.getheader("Content-Encoding") == "gzip":
        tmp = io.BytesIO(source.read())
        dataunique = gzip.GzipFile(fileobj=tmp).read().decode(codeform)
    else:
        dataunique = source.read().decode(codeform)
    return dataunique


file = "E:\\test\\chrome\\"
filetmp = file + "tmp\\"
header = {
    "Connection": "keep-alive",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Origin": "https://www.bilibili.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome" +
                  "/63.0.3239.132 Safari/537.36",
    "Referer": "https://www.bilibili.com/video/av18420095/?spm_id_from=333.334.chief_recommend.22",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9"
}
f = open("./cookie.txt")
cookie = json.loads(f.read().replace("\n", ""))
f.close()
url = ""
d = DesiredCapabilities.CHROME
d['loggingPrefs'] = {'performance': 'ALL'}
sources = input("input video url or av number:")
option = webdriver.ChromeOptions()
# option.add_argument('headless')
# option.add_argument('cookie="{}"'.format(cookie))
driver = webdriver.Chrome(chrome_options=option)

if sources.isdigit():
    sourceurl = "https://www.bilibili.com/video/av" + sources
else:
    sourceurl = sources
driver.get("https://www.bilibili.com/")
for i in cookie:
    driver.add_cookie(i)
driver.get(sourceurl)
# 如果获取不到链接,请打开sleep（2）
# time.sleep(2)
for entry in driver.get_log('performance'):
    try:
        a = re.findall("sign=", str(entry))[1]
        url = json.loads(entry["message"])["message"]["params"]["response"]["url"]
        break
    except IndexError:
        continue
title = driver.title.replace(" ", "").replace("\n", "").replace(".", "").replace(":", "_").split("_")[0]
print(title)
driver.close()
if url == "":
    print("wrong source url")
    raise RuntimeError
print("get url successfully")
req = request.Request(url=url, headers=header)
data = dezip(request.urlopen(req))
print("get real url successfully")
data = json.loads(data)
if len(data["durl"]) > 1:
    try:
        os.mkdir(filetmp)
    except FileExistsError:
        pass
    history = open(filetmp + "data.txt", "w")
    for i in data["durl"]:
        down.download(i["url"], filetmp, str(i["order"]) + ".flv", header=header, threadnum=2)
        history.write("file '{0}{1}.flv'\n".format(filetmp, str(i["order"])))
    history.close()
    if len(data["durl"]) > 1:
        os.system("ffmpeg -f concat -safe 0 -i {0} -c copy {1}.flv".format(filetmp + "data.txt", file + title))
    for i in os.listdir(filetmp):
        os.remove(filetmp + i)
    os.removedirs(filetmp)
else:
    down.download(data["durl"][0]["url"], file, title + ".flv", header=header)
driver.quit()

#  title + ".flv"
