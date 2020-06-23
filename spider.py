# -*- coding = Utf-8 -*-
# @Time : 2020/6/14 12:01
# @Author : 张
# @File : spider.py
# @software : PyCharm

import requests
import re



class Spider():
    def __init__(self):
        self.url = 'https://www.huya.com/g/2336'
        self.root_pattern = '<span class="txt">([\s\S]*?)</li>'
        self.name_pattern = '<i class="nick" title="([\s\S]*?)">([\s\S]*?)</i>'
        self.num_pattern = '<i class="js-num">([\s\S]*?)</i>'

    def getHTMLText(self):
        try:
            r = requests.get(self.url, timeout=30)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.text
        except:
            return ''

    def analysis(self, htmls):
        root_html = re.findall(self.root_pattern, htmls)
        anchors = []
        for html in root_html:
            name = re.findall(self.name_pattern, html)
            name_set = set(name[0])
            name = list(name_set)
            num = re.findall(self.num_pattern, html)
            anchor = {'name': name, 'number': num}
            anchors.append(anchor)
        return anchors

    def refine(self, anchors):
        result = lambda anchor: {
            'name': anchor['name'][0],
            'number': anchor['number'][0]
        }
        anchors = map(result, anchors)
        return anchors

    def sort(self, anchors):
        anchors = sorted(anchors, key=self.sortSeed, reverse=True)
        return anchors

    def sortSeed(self, anchors):
        r = re.findall('\d*.?\d*', anchors['number'])
        number = float(r[0])
        if '万' in anchors['number']:
            number *= 10000
        return number

    def show(self, anchors, num):
        formats = "{0:^10}\t{1:^{3}}\t{2:^10}"
        print(formats.format("排名", "名字", "人数", 20))
        for i in range(num):
            try:
                u = anchors[i]
                l = 20-len(u['name'].encode('GBK'))+len(u['name'])
                print(formats.format(str(i + 1), u['name'], u['number'], l))
            except:
                return ''

    def main(self):
        htmls = self.getHTMLText()
        anchors = self.analysis(htmls)
        anchors = list(self.refine(anchors))
        anchors = self.sort(anchors)
        self.show(anchors, 1000)


spider = Spider()
spider.main()
