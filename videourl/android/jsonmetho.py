from urllib import request
import re
import json
import gzip
import io
import os
"""
{
  "season_id": "21542",
  "avid": null,
  "title": "紫罗兰永恒花园",
  "cover": "http://i0.hdslb.com/bfs/bangumi/b6e3986355efc081b7f4aaf9f576c9ce8116e193.jpg",
  "source": {
    "av_id": 18415142,
    "cid": 30111683,
    "website": "bangumi",
    "webvideo_id": ""
  },
  "ep": {
    "av_id": 18415142,
    "page": "1",
    "danmaku": 30111683,
    "cover": "http://i0.hdslb.com/bfs/archive/4d487b25fb9f8fd7c52a234c35d78e87715b2b5e.jpg",
    "episode_id": 173287,
    "index": "2",
    "index_title": ""
  },
  "page_data": null,
  "is_completed": false,
  "total_bytes": 0,
  "downloaded_bytes": 0,
  "type_tag": "lua.hdflv2.bb2api.bd",
  "prefered_video_quality": 112,
  "guessed_total_bytes": 0,
  "total_time_milli": 0,
  "danmaku_count": 3000,
  "time_update_stamp": 1517319993136,
  "time_create_stamp": 1517319993136
}
"""


def dezip(source, *, codeform="utf-8"):
    if source.getheader("Content-Encoding") == "gzip":
        tmp = io.BytesIO(source.read())
        data = gzip.GzipFile(fileobj=tmp).read().decode(codeform)
    else:
        data = source.read().decode(codeform)
    return data


header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " +
              "(KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
# url = input()
url = "http://bangumi.bilibili.com/anime/21754/"
data = dezip(request.urlopen(url))
ep = re.findall('(?<=data-newest-ep-id=")\d+', data)[1]
url = "https://www.bilibili.com/bangumi/play/ep" + ep
req =request.Request(headers=header, url=url)
data = dezip(request.urlopen(req))
data = re.findall('(?<=window.__INITIAL_STATE__=)[^;]*', data)[0]
js = json.loads(data)
for i in js["epList"]:
    source = {}
    source["season_id"] = js["mediaInfo"]["season_id"]
    source["avid"] = "null"
    source["title"] = js["mediaInfo"]["title"]
    source["cover"] = js['mediaInfo']["cover"].encode("UTF-8").decode("UTF-8")
    source["source"] = {}
    source["source"]["av_id"] = i["aid"]
    source["source"]["cid"] = i["cid"]
    source["source"]["website"] = "bangumi"
    source["source"]["webvideo_id"] = ""
    source["ep"] = {}
    source["ep"]["av_id"] = i["aid"]
    source["ep"]["page"] = i['page']
    source["ep"]["danmaku"] = i["cid"]
    source["ep"]["cover"] = i["cover"].encode("UTF-8").decode("UTF-8")
    source["ep"]["episode_id"] = i["ep_id"]
    source["ep"]["index"] = i["index"]
    source["ep"]["index_title"] = i["index_title"]
    source["page_data"] = "null"
    source["is_completed"] = "false"
    source["total_bytes"] = 0
    source["downloaded_bytes"] = 0
    source["type_tag"] = "lua.hdflv2.bb2api.bd"
    source["prefered_video_quality"] = 112
    source["guessed_total_bytes"] = 0
    source["total_time_milli"] = 0
    source["danmaku_count"] = 3000
    print(json.dumps(source))
    try:
        os.makedirs("E:\\tests\\" + str(i["ep_id"]))
    except:
        pass
    with open("E:\\tests\\" + str(i["ep_id"]) + "\\entry.json", "w", encoding="utf8") as tmp:
        tmp.write(str(source).replace("'", '"').encode("utf-8").decode("UTF-8"))
