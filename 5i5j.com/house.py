from  urllib import request
import re
import xlsxwriter

class House():
    #url基地址
    urls = []
    url = 'https://ty.5i5j.com/ershoufang/xiaodianqu/'


    #表达式
    rootPattern ='<div class="listCon">([\s\S]*?)</div>'
    #标题正则
    titlePattern ='<a .*?>(.*?)</a>'
    #房屋类型
    typePattern = '<p><i class="i_01"></i>([\s\S]*?)</p>'

    recentPattern = '<p><i class="i_03"></i>([\s\S]*?)</p>'

    #价钱
    PricePattern = '<p class="redC"><strong>([\d]*?)</strong>万</p>'

    #单价
    unitpricePattern = '<p>([\s\S]*?)</p>'

    def urls(self):
        link = []
        for index in range(1,21):
            info = [House.url+str(index)+'/']
            link.append(info)
        return link
    def __getContent(self):

        result = request.urlopen(House.url)
        htmls = result.read()
        htmls = str(htmls, encoding='utf-8')
        return htmls


    def __analysis(self,htmls):
        infos = []
        root_html = re.findall(House.rootPattern,htmls)
        for html in root_html:
            titile = re.findall(House.titlePattern,html)
            type = re.findall(House.typePattern,html)
            recent = re.findall(House.recentPattern,html)
            price = re.findall(House.PricePattern,html)
            unitPrice = re.findall(House.unitpricePattern,html)

            info = {"name":titile[0],"CBS":titile[1],"type":type[1],
                    "recent":recent[0],"price":price[0],'unitPrice':unitPrice[-1]}
            infos.append(info)
        return infos

    def __writeExcel(self,infos):
        workBook = xlsxwriter.Workbook('house.xlsx')
        workSheet = workBook.add_worksheet()
        workSheet.write('A1','房屋名称')
        workSheet.write('B1','CBS')
        workSheet.write('C1','类型')
        workSheet.write('D1','最近情况及发布时间')
        workSheet.write('E1','价格（万）')
        workSheet.write('F1','单价')
        for index in range(0,len(infos)):
            workSheet.write('A'+str(index+2),infos[index]['name'])
            workSheet.write('B'+str(index+2),infos[index]['CBS'])
            workSheet.write('C'+str(index+2),infos[index]['type'])
            workSheet.write('D'+str(index+2),infos[index]['recent'])
            workSheet.write('E'+str(index+2),infos[index]['price'])
            workSheet.write('F'+str(index+2),infos[index]['unitPrice'])
        workBook.close()




    def go(self):
        # links = house.urls()
        htmls = self.__getContent()
        infos = self.__analysis(htmls)
        self.__writeExcel(infos)

house = House()
house.go()