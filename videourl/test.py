from urllib import request
import hashlib
import time
from io import BytesIO
import gzip
import json
import os
"""
        public const string _appSecret = "560c52ccd288fed045859ed18bffd973";
        public const string _appKey = "1d8b6e7d45233436";
        public const string _appSecret_VIP = "9b288147e5474dd2aa67085f716c560d";
        public const string _appSecret_PlayUrl = "1c15888dc316e05a15fdd0a02ed6584f";
    http://bangumi.bilibili.com/api/season_v3?_device=android&_ulv=10000&build=411005&platform=android&appkey=
    1d8b6e7d45233436&ts={0}000&type=bangumi&season_id={1}
    "1c15888dc316e05a15fdd0a02ed6584f"
"""


def down(urltmp, num):
    req = request.Request(headers=header, url=urltmp)
    flv = request.urlopen(req)
    file = "E:\\test\\" + str(num) + ".flv"
    with open(file, "wb") as filetmp:
        filetmp.write(flv.read())


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
url = "https://bangumi.bilibili.com/player/web_api/playurl/?"
# url = "http://interface.bilibili.com/playurl?"
data = "cid={0}&module=bangumi&player=1&otype=json&type=flv&quality={1}&ts={2}".format(31178873, 4, int(time.time()))
tmp = data + "9b288147e5474dd2aa67085f716c560d"
sign = str(hashlib.md5(tmp.encode()).hexdigest())
urltmp = url + data + "&sign=" + sign
req = request.Request(headers=header, url=urltmp)
data = request.urlopen(req)
if data.getheader("Content-Encoding") == "gzip":
    tmp = BytesIO(data.read())
    data = gzip.GzipFile(fileobj=tmp).read().decode("utf-8")
else:
    data = data.read().decode("utf-8")
print(data)
sou = json.loads(data)
tmp = sou["durl"]
num = 1
with open("E:\\test\\file.txt", "w") as filelist:
    for i in tmp:
        urltmp = i["url"]
        print(urltmp)
        req = request.Request(headers=header, url=urltmp)
        flv = request.urlopen(req)
        file = "E:\\test\\" + str(num) + ".flv"
        with open(file, "wb") as filetmp:
            filetmp.write(flv.read())
        filelist.write("file '" + str(num) + ".flv'\n")
        num += 1
os.system("ffmpeg -f concat -i {0} -c copy {1}".format("E:\\test\\file.txt", "E:\\tests\\aaa.flv"))
