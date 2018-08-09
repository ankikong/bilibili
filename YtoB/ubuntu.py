# -*- coding:utf-8 -*-
from urllib import request, parse
import re
import json
import io
import gzip
import feedparser
import time
from selenium import webdriver, common
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import os
import sys
os.chdir(sys.path[0])


def json_rpc(method, *, url="", dirs="", speed=0, out="", param=None):
    send = {"jsonrpc": "2.0", "id": "qwer", "method": method, "params": []}
    if param is not None:
        send["params"] = param
    if method == "aria2.addUri":
        setting = {"max-download-limit": str(speed) + "M", "out": out}
        if dirs != "":
            setting["dir"] = dirs
        send["params"].append([url])
        send["params"].append(setting)
    return request.urlopen('http://localhost:6800/jsonrpc', data=json.dumps(send).encode()).read().decode()


def dezip(source, *, code_form="utf-8"):
    if source.getheader("Content-Encoding") == "gzip":
        tmp = io.BytesIO(source.read())
        data_unique = gzip.GzipFile(fileobj=tmp).read().decode(code_form)
    else:
        data_unique = source.read().decode(code_form)
    return data_unique


class GetSubtitle:
    def __init__(self, url, file):
        self.url = url
        header = [("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)")]
        opnr = request.build_opener()
        opnr.addheaders = header
        opnr.open("http://www.lilsubs.com/")
        res = opnr.open("http://www.lilsubs.com/", data=parse.urlencode({"url": url}).encode()).read().decode()
        url = re.findall('name="sub_url" value="(.*?)"', res)[0]
        title = re.findall('name="title" value="(.*?)"', res)[0]
        send = {"site": "www.youtube.com", "title": title, "lang": "all", "sub_url": url}
        f = opnr.open("http://www.lilsubs.com/download.php", data=parse.urlencode(send).encode())
        with open(file, "wb") as tmp:
            tmp.write(f.read())


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
            "client_urlmap": "none",                 "ipv6": "true",     "addon_urlmap": "",    "cookie": "",
            "addon_cookie": "",  "addon_title": "",  "ablock": 1,        "clientside": 0,       "addon_page": "none",
            "verify": "",        "result": "",       "again": "",        "addon_browser": "",   "addon_version": "",
        }
        self.url = "https://www.clipconverter.cc/check.php"
        self.send_data["mediaurl"] = video_url
        self.source = video_url
        self.id = video_url.split("=")[1]

    def first(self):
        send = self.send_data.copy()
        req = request.Request(headers=self.header, url=self.url, data=parse.urlencode(send).encode())
        res = dezip(request.urlopen(req))
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
        file_name = data["filename"]
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
        # print(status_url)
        while True:
            req = request.Request(url=status_url, headers=self.header)
            res = dezip(request.urlopen(req)).replace("(", "").replace(")", "")
            data = json.loads(res)
            if data["status"]["@attributes"]["step"] == "finished":
                download_url = data["downloadurl"].replace("http", "https")
                break
            time.sleep(4)
            print("wait for cc finishing " + data["status"]["@attributes"]["info"])
        new_name = ""
        for i in file_name:
            if i.isnumeric() or i.isalpha() or i.isspace():
                new_name += i
        print(new_name)
        self.get_cover()
        return download_url, new_name

    def get_cover(self):
        url = "https://i1.ytimg.com/vi/{}/maxresdefault.jpg".format(self.id)
        json_rpc("aria2.addUri", url=url, out=self.id + ".jpg")


class Do:
    def __init__(self):
        """
        rss订阅地址，
        [标签]
        [分区选择]
        """
        self.rss_url = [
            ["https://www.youtube.com/feeds/videos.xml?channel_id=UCe_vXdMrHHseZ_esYUskSBw",
             ["CrazyRussianHacker", "熊叔实验室", "网络爬虫", "python爬虫"],
             ["科技", "趣味科普人文"]
             ],
            ["https://www.youtube.com/feeds/videos.xml?channel_id=UCp68_FLety0O-n9QU6phsgw",
             ["colinfurze", "英国疯子", "网络爬虫", "python爬虫"],
             ["科技", "机械"]
             ],
            ["https://www.youtube.com/feeds/videos.xml?channel_id=UCasG9kJWi1eVxM0QkyqKVJQ",
             ["Hand Tool Rescue", "翻新", "网络爬虫", "python爬虫"],
             ["科技", "机械"]
             ],
            ["https://www.youtube.com/feeds/videos.xml?channel_id=UCAuUUnT6oDeKwE6v1NGQxug",
             ["TED", "演讲", "网络爬虫", "python爬虫"],
             ["科技", "演讲"]
             ],
            ["https://www.youtube.com/feeds/videos.xml?channel_id=UCsooa4yRKGN_zEE8iknghZA",
             ["TED-Ed", "演讲", "网络爬虫", "python爬虫"],
             ["科技", "演讲"]
             ],
        ]

    def run(self):
        path = json.loads(json_rpc("aria2.getGlobalOption"))["result"]["dir"].replace('\\', '/')
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get("https://www.bilibili.com/")
        with open("cookie.txt", "r") as ___tmp:
            cookie = ___tmp.read()
            cookie = json.loads(cookie)
            for i in cookie:
                driver.add_cookie(i)
        with open("data.txt", "r") as tmp:
            record = tmp.read()
        for i in self.rss_url:
            data = feedparser.parse(i[0])
            for j in data["entries"]:
                if j["yt_videoid"] not in record:
                    name = ""
                    for _ in j["title"]:
                        if _.isnumeric() or _.isalpha() or _.isspace():
                            name += _
                    print("start: ", j["link"])
                    time.sleep(10)
                    if name not in str(json_rpc("aria2.tellStopped", param=[0, 10000])):
                        getvideo = GetVideo(j["link"])
                        link, name = getvideo.first()
                        print("finished getting link")
                        # download(url=link, header={"out": name + ".mp4"})
                        _ = json_rpc("aria2.addUri", url=link, out=name + ".mp4")
                        _ = json.loads(_)["result"]
                        while True:
                            time.sleep(6)
                            data = json.loads(json_rpc("aria2.tellStatus", param=[_]))
                            total = int(data["result"]["totalLength"])
                            complete = int(data["result"]["completedLength"])
                            if total == complete:
                                break
                            print("aria downloading: {0}M/{1}M".format(int(complete/1024/1024), int(total/1024/1024)))
                    print("finish down")
                    up = Upload2(url=j["link"],
                                 video_path=path,
                                 video="{}.mp4".format(name),
                                 tag=i[1],
                                 title=name,
                                 block=i[2],
                                 driver=driver)
                    up.start()
                    print("finish upload")
                    with open("data.txt", "a") as tmp:
                        tmp.write(j["yt_videoid"] + "\n")
                    record += j["yt_videoid"] + "\n"
                    os.remove(path + "/{}.mp4".format(name))
                    os.remove(path + "/{}.jpg".format(j["yt_videoid"]))
        driver.close()


class Upload2:
    def __init__(self, url, video_path, video, tag, title, block, driver):
        self.url = url
        self.video_path = video_path + "/"
        self.video = video
        self.video_desc = "本视频由爬虫抓取，并由爬虫上传\n有兴趣的可以进群提建议\n联系群号：849883545\n" +\
            "如有侵犯，请私聊\n"
        self.tag = tag
        self.title = "【生肉/搬运】" + title
        self.block = block
        self.driver = driver
        self.id = url.split("=")[1]

    def start(self):
        self.driver.get("https://member.bilibili.com/video/upload.html")
        a = self.driver.find_element_by_id("bili-upload-btn")
        sou = self.driver.page_source
        idd = re.findall('(?<=rt_rt)[^"]*', sou)[0]
        idd = "rt_rt" + idd
        _d = a.find_element_by_id(idd).find_element_by_name("file")
        _d.send_keys(self.video_path + self.video)
        time.sleep(10)
        try:
            while True:
                self.driver.find_element_by_class_name("guide-tip-btn-v2-item").click()
                time.sleep(3)
        except common.exceptions.WebDriverException:
            pass
        while True:
            res = self.driver.find_element_by_class_name("upload-status-intro").get_attribute("innerHTML")
            if res == '上传完成':
                print("upload finished")
                time.sleep(10)
                break
            else:
                print(res)
            time.sleep(10)
        self.driver.find_element_by_class_name("cover-v2-preview")\
            .find_element_by_xpath("./input").send_keys(self.video_path + self.id + ".jpg")
        time.sleep(1)
        self.driver.find_element_by_class_name("cover-chop-modal-v2-foot").find_element_by_xpath("./div[1]").click()
        time.sleep(4)
        self.driver.find_elements_by_class_name("check-radio-v2-name")[1].click()
        self.driver.find_element_by_class_name("copyright-v2-source-input-wrp").find_element_by_class_name(
            "input-box-v2-1-val").send_keys(self.url)
        self.driver.find_element_by_class_name("select-item-cont").click()
        blocks = self.driver.find_elements_by_class_name("drop-cascader-pre-item")
        for i in blocks:
            if self.block[0] in i.find_element_by_class_name("pre-item-content").get_attribute("innerHTML"):
                i.click()
                time.sleep(1)
                for j in self.driver.find_elements_by_class_name("drop-cascader-list-item"):
                    if self.block[1] in j.find_element_by_class_name("item-main").get_attribute("innerHTML"):
                        j.click()
                        time.sleep(1)
                        break
                break
        tag = self.driver.find_element_by_id("content-tag-v2-container").find_element_by_class_name(
            "input-box-v2-1-val")
        tag.send_keys("youtube\n")
        for i in self.tag:
            time.sleep(1)
            tag.send_keys(i)
            time.sleep(1)
            tag.send_keys(Keys.ENTER)
        self.driver.find_element_by_class_name("content-desc-v2-container").find_element_by_class_name(
            "text-area-box-v2-val").send_keys(self.video_desc)
        for i in range(80):
            _ = self.driver.find_element_by_class_name("content-title-v2-container")
            _.find_element_by_class_name("input-box-v2-1-val").send_keys(Keys.BACKSPACE)
        self.driver.find_element_by_class_name("content-title-v2-container"
                                               ).find_element_by_class_name("input-box-v2-1-val").send_keys(self.title)
        self.driver.find_element_by_class_name("submit-btn-group-add").click()
        print("all finished")


if __name__ == "__main__":
    d = Do()
    d.run()
    # GetSubtitle("https://www.youtube.com/watch?v=FyiMhcKxmVs", file="E:/a.srt")
