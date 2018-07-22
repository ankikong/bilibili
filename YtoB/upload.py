from urllib import request, parse
import re
import os
import json
import math
import time
import io
import gzip
import feedparser
import time
from xmlrpc import client


def download(url, *, dirs="", header=None):
    s = client.ServerProxy("http://192.168.1.231:6800/rpc")
    headers = {}
    if dirs != "":
        headers.update({"dir": dirs})
    opt = []
    if header is not None:
        for i in header:
            opt.append("{0}:{1}".format(i, header[i]))
        headers["header"] = opt
    s.aria2.addUri([url], headers)


def dezip(source, *, codeform="utf-8"):
    if source.getheader("Content-Encoding") == "gzip":
        tmp = io.BytesIO(source.read())
        dataunique = gzip.GzipFile(fileobj=tmp).read().decode(codeform)
    else:
        dataunique = source.read().decode(codeform)
    return dataunique


class Upload:
    def __init__(self, file, title, source):
        with open("./cookie.txt") as tmp:
            self.cookie = tmp.read()
        self.file = file
        self.title = title
        self.source = source
        # 10MB
        self.upload_size = 10 * 1024 * 1024
        self.file_size = os.path.getsize(file)
        self.mid = re.findall('DedeUserID=(.*?);', self.cookie + ';')[0]
        self.csrf = re.findall('bili_jct=(.*?);', self.cookie + ';')[0]
        self.header = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Referer': 'https://space.bilibili.com/{}/#!/'.format(self.mid),
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/5' +
                          '37.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'cookie': self.cookie,
            "Origin": "https://member.bilibili.com",
        }
        self.file_name = file.split("/")[-1]

    def first(self):
        url = "https://member.bilibili.com/preupload?os=upos&upcdn=ws&" +\
              "name={0}&size={1}&r=upos&profile=ugcupos%2Fyb&ssl=0".format(self.file_name, os.path.getsize(self.file))
        _req = request.Request(headers=self.header, url=url)
        _data = request.urlopen(_req).read().decode()
        _data = json.loads(_data)
        self.upos_uri = _data["upos_uri"].replace("upos:/", "").replace("/ugc/", "")
        self.biz_id = _data["biz_id"]
        self.endpoint = _data["endpoint"]
        self.auth = _data["auth"]

    def second(self):
        url = "http:{1}/ugc/{0}?uploads&output=json".format(self.upos_uri, self.endpoint)
        self.header["X-Upos-Auth"] = self.auth
        _req = request.Request(headers=self.header, url=url, data="".encode())
        while True:
            try:
                _data = request.urlopen(_req).read().decode()
                _data = json.loads(_data)
                self.upload_id = _data["upload_id"]
                break
            except (IndexError, KeyError):
                continue

    def third(self):
        url = "http:{0}/ugc/{1}?total={2}".format(self.endpoint, self.upos_uri, self.file_size)
        url2 = "&partNumber={0}&uploadId={1}&chunk={2}&chunks={3}&size={4}&start={5}&end={6}"
        total_chunk = math.ceil(self.file_size / self.upload_size)
        index = 0
        now_size = 0
        with open(self.file, "rb") as file:
            while True:
                part = file.read(self.upload_size)
                if not part:
                    break
                size = len(part)
                index += 1
                url_tmp = url2.format(index, self.upload_id, index - 1, total_chunk, size, now_size, now_size + size)
                now_size += size
                header = self.header.copy()
                # header["Content-Length"] = str(size)
                header['Accept'] = "*/*"
                header.pop("cookie")
                req = request.Request(url=url + url_tmp, headers=header, data=part, method='PUT')
                try:
                    res = request.urlopen(req, timeout=20).read()
                    print(res)
                except Exception:
                    pass

    def fourth(self):
        url = "http://member.bilibili.com/x/vu/web/add?csrf=" + self.csrf
        header = self.header.copy()
        header["Content-Type"] = "application/json;charset=UTF-8"
        header["csrf"] = self.csrf
        send_data = {"copyright": 2, "videos": [{"filename": self.upos_uri.split(".")[0],
                                                 "title": self.title,
                                                 "desc": ""}],
                     "source": self.source,
                     "tid": 98,
                     "cover": "",
                     "title": "【生肉/搬运】" + self.title,
                     "tag": "机械",
                     "desc_format_id": 0,
                     "desc": "本视频由爬虫抓取，并由爬虫上传\n有兴趣的可以在评论区提建议",
                     "dynamic": ""}
        req = request.Request(url=url, headers=header, data=json.dumps(send_data).encode())
        res = request.urlopen(req).read().decode()
        print(res)

    def main(self):
        self.first()
        self.second()
        self.third()
        self.fourth()


class GetVideo:
    def __init__(self, video_url):
        self.header = {
            "Accept": "application/json, text/javascript, */*",
            "Origin": "https://www.clipconverter.cc",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " +
                          "(KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://www.clipconverter.cc/",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6",
            "Cookie": "_ga=GA1.2.919755054.1527625981; _gid=GA1.2.2131623793.1527625981; __test; _gat=1",
            "Accept-Encoding": "gzip, deflate, br"
        }
        self.send_data = {
            "mediaurl": "",      "filename": "",     "filetype": "",     "format": "",          "audiovol": 0,
            "audiochannel": 2,   "audiobr": 128,     "videobr": 224,     "videores": "352x288", "videoaspect": "",
            "customres": "320x240",     "timefrom-start": 1,             "timeto-end": 1,       "id3-artist": "",
            "id3-title": "",     "id3-album": "ClipConverter.cc",        "auto": 0,             "hash": "",
            "image": "",         "org-filename": "", "videoid": "",      "pattern": "",         "server": "",
            "serverinterface": "",                   "service": "",      "ref": "",             "lang": "en",
            "client_urlmap": "none",                 "ipv6": "false",     "addon_urlmap": "",    "cookie": "",
            "addon_cookie": "",  "addon_title": "",  "ablock": 1,        "clientside": 0,       "addon_page": "none",
            "verify": "",        "result": "",       "again": "",        "addon_browser": "",   "addon_version": "",
        }
        self.url = "https://www.clipconverter.cc/check.php"
        self.send_data["mediaurl"] = video_url
        self.source = video_url

    def first(self):
        send = self.send_data.copy()
        req = request.Request(headers=self.header, url=self.url, data=parse.urlencode(send).encode())
        res = dezip(request.urlopen(req))
        print(res)
        data = json.loads(res)
        self.send_data["verify"] = data["verify"]
        self.send_data["server"] = data["server"]
        self.send_data["serverinterface"] = data["serverinterface"]
        self.send_data["filename"] = data["filename"]
        self.send_data["filetype"] = "MP4"
        self.send_data["id3-artist"] = data["id3artist"]
        self.send_data["id3-title"] = data["id3title"]
        self.send_data["image"] = data["thumb"]
        self.send_data["org-filename"] = data["filename"]
        self.send_data["videoid"] = data["videoid"]
        self.send_data["pattern"] = data["pattern"]
        self.send_data["server"] = data["server"]
        self.send_data["serverinterface"] = data["serverinterface"]
        self.send_data["service"] = data["service"]
        self.file_name = data["filename"]
        for i in data["url"]:
            if "1080" in i["text"] or "720" in i["text"]:
                self.send_data["url"] = i["url"]
                size = re.findall("#size=(.*?)#audio", i["url"])[0]
                self.send_data["url"] += '|' + size
                break
        req = request.Request(url=self.url, headers=self.header, data=parse.urlencode(self.send_data).encode())
        res = dezip(request.urlopen(req))
        data = json.loads(res)
        get_check = "https://www.clipconverter.cc/convert/{}/?ajax".format(data["hash"])
        req = request.Request(url=get_check, headers=self.header)
        res = dezip(request.urlopen(req))
        status_url = re.findall('statusurl = "(.*?)"', res)[0]
        while True:
            req = request.Request(url=status_url, headers=self.header)
            res = dezip(request.urlopen(req)).replace("(", "").replace(")", "")
            data = json.loads(res)
            if data["status"]["@attributes"]["step"] == "finished":
                self.download = download_url = data["downloadurl"].replace("http", "https")
                break
            time.sleep(1)
        return self.download, self.file_name


class Do:
    def __init__(self):
        self.rss_url = [
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCp68_FLety0O-n9QU6phsgw",
        ]

    def run(self):
        now = time.time()
        with open("data.txt", "r") as tmp:
            record = tmp.read()
        for i in self.rss_url:
            data = feedparser.parse(i)
            for j in data["entries"]:
                ti = time.mktime(time.strptime(j["updated"].split("+")[0], "%Y-%m-%dT%H:%M:%S"))
                if j["yt_videoid"] not in record and now - ti < 60 * 60 * 24 * 3:
                    getvideo = GetVideo(j["link"])
                    link, name = getvideo.first()
                    print("finished getting link")
                    download(link)
                    s = client.ServerProxy("http://192.168.1.231:6800/rpc")
                    while True:
                        time.sleep(60)
                        data = s.aria2.getGlobalStat()
                        if data["numActive"] == 0:
                            break
                    print("finish down")
                    Up = Upload("/mnt/usb1/aria/{}.mp4".format(name), title=name, source=j["link"])
                    Up.main()
                    print("finish upload")
                    record += j["yt_videoid"] + "\n"
        with open("data.txt", "w") as tmp:
            tmp.write(record)


if __name__ == "__main__":
    t = Upload("E:/Downloads/chrome/THE BICYCLE OF SPRINGS.mp4",
               "THE BICYCLE OF SPRINGS_test",
               "https://www.youtube.com/watch?v=N39uwTykTQk")
    t.main()
