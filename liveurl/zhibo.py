from urllib import request
import json
import re
import os
import datetime
import time
import threading
"""
https://api.live.bilibili.com/bili/getRoomInfo/9617619 
https://api.live.bilibili.com/room/v1/Room/playUrl?cid=5440&quality=0&platform=web
"""
doenloadhead = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)" +
                  " Chrome/63.0.3239.108 Safari/537.36",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Origin": "https://www.bilibili.com",
    "Referer": "https://www.bilibili.com/video/av17907371/"
}
filedir = "E:\\test\\"
# 227933 193584, 52717408
upmid = [9617619]
infourl = "https://api.live.bilibili.com/bili/getRoomInfo/"
addrurl = "https://api.live.bilibili.com/room/v1/Room/playUrl?cid="


def Record(upmid):
    while True:
        upstat = request.urlopen(infourl + str(upmid)).read().decode().replace("(", "").replace(")", "").replace(";", "")
        data = json.loads(upstat)
        if data["data"]["roomStatus"] == 1 and data["data"]["liveStatus"]:
            print("General URL")
            cid = re.findall("\d+", data["data"]["url"])[0]
            urldata = request.urlopen(addrurl + cid).read().decode()
            roomurl = json.loads(urldata)["data"]["durl"][0]["url"]
            req = request.Request(headers=doenloadhead, url=roomurl)
            getreal = request.urlopen(req)
            tmp = str(datetime.datetime.now()).replace(" ", "_").replace(".", "_").replace(":", "_")
            """
            realurl = getreal.geturl()
            
            command = 'ffmpeg -i "{0}" -c copy "{1}{2}.flv"'.format(realurl, filedir, tmp)
            os.system(command)
            """
            """
            with open(filedir + "{}.flv".format(tmp), "wb") as t:
                while True:
                    da = getreal.read(128 * 1024)
                    t.write(da)
            """
            os.system('./ffplay "{}"'.format(getreal))
        time.sleep(60)


for i in upmid:
    threadpoor = []
    t = threading.Thread(target=Record, args=(i, ))
    t.start()
