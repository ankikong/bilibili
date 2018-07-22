from urllib import request
import json
# 在这里填写文件下载路径，
filefull = "E:\\test\\1\\"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (" +
                  "KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
}
source = "https://www.bilibili.com/index/index-icon.json"
req = request.Request(url=source, headers=header)
data = request.urlopen(req).read().decode()
data = json.loads(data)
data = data["fix"]
try:
    with open("topright.txt") as tmp:
        got = json.load(tmp)
except FileNotFoundError:
    print("first time to run")
    got = {}
num = 0
filefull += "{}.gif"
for i in data:
    if i["id"] in got.keys():
        continue
    req = request.Request(headers=header, url="http:" + i["icon"])
    print(i["title"])
    with open(filefull.format(i["title"] + i["id"]), "wb") as tmp:
        tmp.write(request.urlopen(req).read())
    got[i["id"]] = i["title"]
with open("topright.txt", "w") as tmp:
    json.dump(got, tmp)
print("finished")
