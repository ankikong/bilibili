from urllib import request
import io
import gzip
import re
import hashlib
doenloadhead = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)" + \
                  " Chrome/63.0.3239.108 Safari/537.36",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Origin": "https://www.bilibili.com",
    "Referer": "https://www.bilibili.com/video/av17907371/"
}
url = "http://interface.bilibili.com/playurl?"
key = "1c15888dc316e05a15fdd0a02ed6584f" # yes


def getcid(av):
    source = request.urlopen("https://www.bilibili.com/video/av"+str(av))
    if source.getheader("Content-Encoding") == 'gzip':
        tmp = io.BytesIO(source.read())
        source = gzip.GzipFile(fileobj=tmp).read().decode('utf-8')
    else:
        source = source.read().decode('utf-8')
    #print(source)
    cid = re.findall("(?<=cid=')\d*", source)
    if len(cid) == 0:
        cid = re.findall("(?<=cid=)\d+", source)
    return cid


def GetSign(data):
    tmp = data + key
    return str(hashlib.md5(tmp.encode("utf-8")).hexdigest())


def formurl(av, *, iscid=False):
    global url
    if iscid:
        cid = [str(av)]
    else:
        cid = getcid(av)
    print(cid)
    res = []
    for i in cid:
        tmpurl = "cid=" + i + "&player=1&quality=3"
        sign = GetSign(tmpurl)
        tmpurl = url + tmpurl + "&sign=" + sign
        res.append(tmpurl)
    return res


if __name__ == "__main__":
    url = formurl(32005501, iscid=True)
    print(url)


