from urllib import  request
import  re
class Spider():
    #url地址
    url = 'https://www.panda.tv/cate/lol?pdt=1.24.s1.3.3j4r1vt315r'
    #正则表达式
    rootPattern = '<div class="video-info">([\s\S]*?)</div>'
    namePattern = '</i>([\s\S]*?)</span>'
    numberPattern = '<span class="video-number">([\s\S]*?)</span>'

    #获取内容
    def __fetch_content(self):
        result = request.urlopen(Spider.url)
        htmls = result.read()
        htmls = str(htmls,encoding = 'utf-8')
        return  htmls

    def __analysis(self,htmls):
        root_html = re.findall(Spider.rootPattern,htmls)
        anchors = []
        for html in root_html:
            name = re.findall(Spider.namePattern,html)
            number = re.findall(Spider.numberPattern,html)
            anchor = {'name':name,'number':number}
            anchors.append(anchor)
        return anchors
    #精炼数据
    def __refine(self,anchors):
        l = lambda anchor:{
            'name':anchor['name'][0].strip(),'number':anchor['number'][0]
        }
        return map(l,anchors)

    def __sort(self,anchors):
        pass
    def go(self):
        htmls = self.__fetch_content()
        anchors = self.__analysis(htmls)
        anchors =list(self.__refine(anchors))



spider = Spider()
spider.go()