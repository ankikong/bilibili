from urllib import request
url = "http://api.bilibili.com//playurl?aid={0}&page=1&platform=android&quality=0&type=jsonp".format(input("av:"))
doenloadhead = {
    "User-Agent": "Freedoooooom/MarkII",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Origin": "https://www.bilibili.com",
    "Referer": "https://www.bilibili.com/video/av17907371/",
    "Upgrade-Insecure-Requests": 1,
    "Cookie": "fts=1509709625; buvid3=26421748-7FA8-4108-966F-5728E8B41FB41982infoc; UM_distinctid=15f81b" +
              "4ca17e9-0fb7d8d64e62a6-c303767-1fa400-15f81b4ca18294; rpdid=iwiqmmoqmidoswlmwlxiw; pgv_pvi" +
              "=8088246272; pgv_si=s4351379456; _cnt_pm=0; _cnt_notify=0; DedeUserID=23207406; DedeUserID" +
              "__ckMd5=d8f03070e37650e8; SESSDATA=342df4e4%2C1519219816%2Cac49ab39; bili_jct=15e8a41c6c20" +
              "37c056a8de51cddd4afe; im_notify_type_23207406=0; LIVE_BUVID=49b131422c0259c76ce63f335353f1" +
              "12; LIVE_BUVID__ckMd5=14719b40e61d873c; sid=ka8bt5ie; finger=edc6ecda; BANGUMI_SS_21754_RE" +
              "C=173159; purl_token=bilibili_1518059929; BANGUMI_SS_21542_REC=173290; _dfcaptcha=6f38ffdf" +
              "ddba5e7e97f0f7ae307af97b",
}
# doenloadhead.pop("Cookie")
req = request.Request(headers=doenloadhead, url=url)
data = request.urlopen(req).read().decode()
print(data)
