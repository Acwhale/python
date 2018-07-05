from urllib import  request
import  re
class Spider():
    #url地址
    url = 'https://www.panda.tv/cate/lol?pdt=1.24.s1.3.3j4r1vt315r'
    #正则表达式
    rootPattern = '<div class="video-info">([\s\S]*?)</div>'
    namePattern = '</i>([\s\S]*?)</span>'
    numberPattern = '<span class="video-number">([\s\S]*?)</span>'

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

    def __refine(self,anchors):
        l = lambda anchor:{
            'name':anchor['name'][0].strip(),'number':anchor['number'][0]
        }
        return map(l,anchors)

    def __sort(self,anchors):
        anchors = sorted(anchors,key=self.__sort_seed,reverse=True)
        return anchors

    def __sort_seed(self,anchor):
        result = re.findall('\d*',anchor['number'])
        number = float(result[0])
        if '万' in anchor['number']:
            number *= 10000
        return number
    def __show(self,anchors):
        for rank in range(0,len(anchors)):
            print('排序:' + str(rank+1) + ':' + anchors[rank]['name'] + "  "+anchors[rank]['number'])
    def go(self):
        htmls = self.__fetch_content()
        anchors = self.__analysis(htmls)
        anchors =list(self.__refine(anchors))
        anchors = self.__sort(anchors)
        self.__show(anchors)



spider = Spider()
spider.go()