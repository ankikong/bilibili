from urllib import request, parse
import re
import os
import json
import math


class Upload:
    def __init__(self, file, title, source):
        with open("./cookie.txt") as tmp:
            self.cookie = tmp.read()
        self.file = file
        self.title = title
        self.source = source
        # 10MB
        self.upload_size = 4 * 1024 * 1024
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
        self.restore = {"parts": []}

    def first(self):
        filename = parse.urlencode({"name": self.file_name})
        self.files = filename
        url = "https://member.bilibili.com/preupload?os=upos&upcdn=ws&" +\
              "{0}&size={1}&r=upos&profile=ugcupos%2Fyb&ssl=0".format(filename, os.path.getsize(self.file))
        _req = request.Request(headers=self.header, url=url)
        _data = request.urlopen(_req).read().decode()
        _data = json.loads(_data)
        self.upos_uri = _data["upos_uri"].replace("upos:/", "").replace("/ugc/", "")
        self.biz_id = _data["biz_id"]
        self.endpoint = _data["endpoint"]
        self.auth = _data["auth"]

    def second(self):
        url = "https:{1}/ugc/{0}?uploads&output=json".format(self.upos_uri, self.endpoint)
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
        url = "https:{0}/ugc/{1}?total={2}".format(self.endpoint, self.upos_uri, self.file_size)
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
                print(url_tmp)
                now_size += size
                header = self.header.copy()
                header["Access-Control-Request-Method"] = "PUT"
                header["Access-Control-Request-Headers"] = "x-upos-auth"
                req = request.Request(url=url + url_tmp, headers=header, method='OPTIONS')
                request.urlopen(req, timeout=20).read()
                # header.pop("Access-Control-Request-Method")
                # header.pop("Access-Control-Request-Headers")
                if size == self.upload_size:
                    header["Content-Length"] = str(size)
                else:
                    try:
                        header.pop("Content-Length")
                    except KeyError:
                        pass
                header['Accept'] = "*/*"
                header.pop("cookie")
                req = request.Request(url=url + url_tmp, headers=header, data=part, method='PUT')
                res = request.urlopen(req).read().decode()
                self.restore["parts"].append({"partNumber": index, "eTag": "etag"})
                print(res)
        url2 = "https:{0}/ugc/{1}?output=json&{2}&{4}&uploadId={3}&biz_id={4}"\
            .format(self.endpoint, self.upos_uri, self.files, self.upload_id, self.biz_id,
                    parse.urlencode({"profile": "ugcupos/yb"}))
        print(url2)
        header = self.header.copy()
        header.pop('cookie')
        header["Content-Type"] = "application/json; charset=UTF-8"
        print(header)
        print(json.dumps(self.restore).replace(" ", ""))
        req = request.Request(url=url2, headers=header, method="OPTIONS")
        request.urlopen(req).read()
        req = request.Request(url=url2, headers=header, data=json.dumps(self.restore).replace(" ", "").encode())
        res = request.urlopen(req).read().decode()
        print(res)

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
                     "desc": "本视频由爬虫抓取，并由爬虫上传\n有兴趣的可以在评论区提建议\n测试阶段，可能出现数据不准",
                     "dynamic": ""}
        req = request.Request(url=url, headers=header, data=json.dumps(send_data).replace(" ", "").encode())
        res = request.urlopen(req).read().decode()
        print(res)

    def main(self):
        self.first()
        self.second()
        self.third()
        self.fourth()

