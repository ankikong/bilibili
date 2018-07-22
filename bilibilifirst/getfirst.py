# -*- coding:UTF-8 -*-
from urllib import request, parse
import io
import gzip
import re
import json
import time


def dezip(source, *, codeform="utf-8"):
    if source.getheader("Content-Encoding") == "gzip":
        tmp = io.BytesIO(source.read())
        data = gzip.GzipFile(fileobj=tmp).read().decode(codeform)
    else:
        data = source.read().decode(codeform)
    return data


url = "https://api.bilibili.com/x/web-feed/feed?jsonp=jsonp&pn=1"
replyurl = "https://api.bilibili.com/x/v2/reply/add"
header = {
    "Connection": "keep-alive",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Origin": "https://www.bilibili.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome" +
                  "/63.0.3239.132 Safari/537.36",
    "Referer": "https://www.bilibili.com/video/av18420095/?spm_id_from=333.334.chief_recommend.22",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}
replydata = {
    "oid": 0,
    "type": 1,
    # message填你要发的话
    "message": "恕我直言，在座的各位，手速都不如我->_->",
    "plat": 1,
    "jsonp": "jsonp",
    "csrf": ""
}
hasreplied = [19283063]
with open("cookie.txt") as tmp:
    header["cookie"] = tmp.read()
replydata["csrf"] = re.findall("(?<=bili_jct=)[^;]*", header["cookie"])[0]
while True:
    req = request.Request(url=url + "&_=" + str(int(time.time()*1000)), headers=header)
    data = dezip(request.urlopen(req))
#    print(data)
    data = json.loads(data)
    tmp = data["data"]
    nowtime = int(time.time())
    for i in tmp:
        if i["type"] == 0:
            if i["archive"]["stat"]["reply"] < 10:
                replydata["oid"] = i["archive"]["aid"]
        elif i["type"] == 1:
            bangumiurl = "https://www.bilibili.com/bangumi/play/ep" + str(i["bangumi"]["new_ep"]['episode_id'])
            bangumreq = request.Request(headers=header, url=bangumiurl)
            bangumres = dezip(request.urlopen(bangumreq))
            aid = re.findall("(?<=av)\d+", bangumres)[0]
            replydata["oid"] = int(aid)
        if replydata["oid"] in hasreplied:
            break
        hasreplied.append(replydata["oid"])
        replyreq = request.Request(url=replyurl, data=parse.urlencode(replydata).encode(), headers=header)
        result = dezip(request.urlopen(replyreq))
        print(replydata["oid"], result)
    time.sleep(10)
