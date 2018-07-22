import os
from urllib import request
import headers
from bilibili.caap.test import findblack
import time

url = "http://live.bilibili.com/FreeSilver/getCaptcha"
req = request.Request(headers=headers.bilibiliheader, url=url)
for i in range(10):
    data = request.urlopen(req)
    file = "s{}.png".format(i)
    with open(file, "wb") as tmp:
        tmp.write(data.read())
    data = findblack(file)
    print(data)
#    os.remove("{}.png".format(i))
    time.sleep(5)
