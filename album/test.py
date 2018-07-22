from urllib import request
import json
"""
http://163.177.151.23:80
http://123.207.17.166:80
http://178.131.39.57:8080
http://124.133.230.254:80
http://116.199.115.78:80
http://121.8.98.197:80
http://113.113.95.27:80
http://110.252.103.106:80
http://220.181.163.231:80
"""
api = "https://api.vc.bilibili.com/link_draw/v1/doc/doc_list?uid={0}&page_num=1&page_size=100&biz=all"


def get(start, stop, ip):
    hand = request.ProxyHandler({"http": ip})
    opener = request.build_opener(hand)
    opener.addheaders = [("User-Agent", "have-fun(bilibili-cheeeeeeeeeeeeeeeer)")]
    for i in range(start, stop):
        global api
        url = api.format(i)
        data = opener.open(url).read().decode()
        print(data)


laststop = 0
get(1, 2, "http://220.181.163.231:80")
