from urllib import request
import json
import time
urljson = "https://api.bilibili.com/x/web-interface/index/icon"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (" +
                  "KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
}
req = request.Request(url=urljson, headers=header)
got = {}
cantfind = 0
found = 0
try:
    with open("data.txt", "r") as tmp:
        got.update(json.load(tmp))
except FileNotFoundError:
    print("first time")
for i in range(20000):
    data = request.urlopen(req).read().decode()
    jsons = json.loads(data)
    if jsons["data"]["icon"] in got.values():
        cantfind += 1
        if cantfind == 500:
            print("may be finished")
            break
        print("It is the same as the previous")
        continue
    cantfind = 0
    print(jsons["data"]["icon"])
    if jsons["data"]["title"] in got.keys():
        name = jsons["data"]["title"] + str(int(time.time()) % 4000)
    else:
        name = jsons["data"]["title"]
    got[name] = jsons["data"]["icon"]
    with open("E:\\test\\{}.gif".format(name), "wb") as tmp:
        getreq = request.Request(headers=header, url="http:" + jsons["data"]["icon"])
        tmp.write(request.urlopen(getreq).read())
        found += 1
with open("data.txt", "w") as tmp:
    json.dump(got, tmp)
