import xml.etree.ElementTree


class xmlres:
    def __init__(self, source):
        print(source)
        self.xml = xml.etree.ElementTree.fromstring(source)
        self.timelength = int(self.xml.find('timelength').text)
        self.format = self.xml.find("format").text
        self.quality = self.xml.find("quality").text
        tmp = self.xml.find("durl")
        self.order = int(tmp.find("order").text)
        self.size = int(tmp.find("size").text)
        self.length = int(tmp.find("length").text)
        self.url = tmp.find("url").text


if __name__ == "__main__":
    strs = open("E:\\bilibili.xml", "r").read()
    tmp = xmlres(strs)
    for i in tmp.__dict__:
        print(i, tmp.__dict__[i])
