from bilibili.videourl.xml import bilibilixml, bilibiliurl
from urllib import request
from io import BytesIO
import gzip
import down
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

av = input("input av number: ")
url = bilibiliurl.formurl(av)
for i in url:
    print(i)
    tmp = request.Request(url=i, headers=header)
    data = request.urlopen(tmp)
    if data.getheader("Content-Encoding") == "gzip":
        tmp = BytesIO(data.read())
        data = gzip.GzipFile(fileobj=tmp).read().decode("utf-8")
    else:
        data = data.read().decode("utf-8")
    print(data)
    data = bilibilixml.xmlres(data)
    print("size:", int(data.size/1024/1024), "M")
    # down.download(url=data.url, dirpath="E:\\tests\\", filename="1.mp4", threadnum=20, header=header)
"""
    with open("E:\\test\\1.flv", "wb") as tmp:
        req = request.Request(url=data.url, headers=header)
        flv = request.urlopen(req)
        while True:
            t = flv.read(4096)
            if not t:
                break
            tmp.write(t)
"""

