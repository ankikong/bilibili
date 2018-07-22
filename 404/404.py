from urllib import request
import headers
import tool
import json
file = "E:\\test\\404\\"
api = "http://www.bilibili.com/activity/web/view/data/31"
req = request.Request(headers=headers.bilibiliheader, url=api)
data = tool.dezip(request.urlopen(req))
data = json.loads(data)
try:
    with open(file + "data.txt") as tmp:
        down = tmp.read()
except FileNotFoundError:
    down = []
for i in data["data"]["list"]:
    if i["id"] in down:
        continue
    down.append(i["id"])
    print(i["data"]["img"])
    req = request.Request(headers=headers.bilibiliheader, url="http:" + i["data"]["img"])
    res = request.urlopen(req)
    with open(file + str(i["id"] + ".png"), "wb") as tmp:
        tmp.write(res.read())
with open(file + "data.txt", "w") as tmp:
    for i in down:
        tmp.write(i + " ")
