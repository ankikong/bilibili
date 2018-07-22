from urllib import request
import json
import time
import threading
import re
api = "https://api.vc.bilibili.com/link_draw/v1/doc/doc_list?uid={0}&page_num=0&page_size=100&biz=all"
iwant = "QQ||qq||Qq||qQ||@||\d{8,10}||\d{11}||微信||\.com||\.net||\.org"


def get(i):
    url = api.format(i)
    req = request.Request(headers={"User-Agent": "have-fun(bilibili-cheeeeeeeeeeeeeeeer)"}, url=url)
    data = request.urlopen(req).read().decode()
    data = json.loads(data)
    if len(data["data"]["items"]) < 1:
        return
    for ii in data["data"]["items"]:
        aa = re.findall("", ii["description"])
        if len(aa) - aa.count('') > 0:
            print("{0}--{1}".format(i, ii["description"]))


if __name__ == "__main__":
    for i in range(30000, 40000):
        threading.Thread(target=get, args=(i, )).start()
        while len(threading.enumerate()) > 31:
            time.sleep(2)
