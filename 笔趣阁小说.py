#-*- codeing = utf-8 -*-
#@time: 2020/7/27 14:58
#@Author : ZhangJianMing
#@File : 笔趣阁小说.py
#@software: PyCharm

'''
    此程序用于下载笔趣阁（网址：https://www.duquanben.com/book/monthvisit/0/1/）
    月排行榜的小说（按页下载）
'''
from bs4 import BeautifulSoup     #网页解析，获取数据
import re       #正则表达式，进行文字匹配
import urllib.request,urllib.error      #制定url，获取网页数据
import requests

def main():
    baseurl = "https://www.duquanben.com/book/monthvisit/0/"

    #1.爬取网页
    datalist = getData(baseurl)

    #3.保存数据


#小说链接
findLink = re.compile('<a href="(.*?)" target="_blank">')
#小说名字
findTitle = re.compile('<li class="two"><a href=".*?" target="_blank">(.*?)全文阅读</a></li>')
#章节链接
findChapter = re.compile('<a href="(.*?)">')
#章节名字
findChName = re.compile('<li><a href=".*?">(.*?)</a></li>')
#小说内容
findTxt = re.compile('<div id="htmlContent" class="contentbox" style="font-size: 20px; color: rgb(0, 0, 0);">(.*?)</div>')
#爬取网页
def getData(baseurl):
    #一.爬取小说排行
    datalist = []
    x = 0       #小说标题计数
    for i in range(0,1):                #下载的页数[开始页数，结束页数)
        url1 = baseurl +str(i+1)        #排行页面链接
        html1 = askURL(url1)
        # print(html)
    #2.1 解析数据
        soup1 = BeautifulSoup(html1,"html.parser")
        for item in soup1.find_all('li',class_="two"):
             # print(item)
            data = []       #保存一部小说的链接以及名字
            item = str(item)

            #获取小说链接
            link = re.findall(findLink,item)
            data.append(link)   #保存小说链接
            titles = re.findall(findTitle,item)
            titles = str(titles)
            titles = titles.strip("[")  # 去掉[
            titles = titles.rstrip("]")  # 去掉]
            titles = re.sub(" ", "", titles)  # 去掉空格
            titles = re.sub("\'", "", titles)  # 去掉多余的”
            if(titles == ''):continue
            # print(titles)         #测试小说名字
            data.append(titles)     #保存小说名字
            datalist.append(data)
    # print(datalist)       #测试小说排行

    #二 .爬取小说章节
    # i = 1
    for data in datalist:
        url2 = data[0]       #小说页面链接
        url2 = str(url2)
        url2 = url2.strip("[")          #去掉[
        url2 = url2.rstrip("]")         #去掉]
        # url2 = url2.strip()
        # url2 = url2.rstrip()
        url2 = re.sub(" ","",url2)      #去掉空格
        url2 = re.sub("\'","",url2)     #去掉多余的”
        if(url2 == ""):continue
        # print("%d : "%i+url2)
        # i = i +1
        #test : 多了“ “ 导致无法找到适配器
        # html2 = askURL("https://www.duquanben.com/xiaoshuo/28/28536/")
        # url = "https://www.duquanben.com/xiaoshuo/28/28536/"
        # if(url == url2):print("same")
        # else:print("NO same")
        # print("url:",url)
        # print("url2:",url2)
        html2 = askURL(url2)

        #2.2解析数据
        soup2 = BeautifulSoup(html2,"html.parser")
        datalist2 = []
        for item in soup2.find_all("li"):
            # print(item)
            data2=[]        #保存章节名以及链接
            item = str(item)

            #获取章节链接
            ChapterLink =str(re.findall(findChapter,item))
            ChapterLink = ChapterLink.strip("[")  # 去掉[
            ChapterLink = ChapterLink.rstrip("]")  # 去掉]
            if ChapterLink == "":continue
            ChapterLink = re.sub("'","",ChapterLink)
            ChapterLink = url2 + ChapterLink    #获得章节完整链接
            data2.append(ChapterLink)

            #获取章节名字
            chName = re.findall(findChName,item)
            chName = str(chName)
            chName = chName.strip("[")
            chName = chName.strip("]")
            chName = re.sub("'","",chName)
            # print(chName)
            data2.append(chName)
            datalist2.append(data2)
            # print(data2[1])
        # print(datalist2)      #测试章节获取


        # for data3 in datalist2:
        #     name = data3[1]
        #     print(name)
        # print(datalist2)
        #三.爬取小说内容
        z = 0               #章节计数
        print("第%d本"%x+datalist[x][1])       #小说名字
        for data in datalist2:
            url3 = data[0]      # 小说页面链接
            url3 = str(url3)
            url3 = url3.strip("[")  # 去掉[
            url3 = url3.rstrip("]")  # 去掉]
            url3 = re.sub(" ", "", url3)  # 去掉空格
            url3 = re.sub("\'", "", url3)  # 去掉多余的”
            if (url3 == ""): continue
            # print("%d:"%i+url3)       #测试章节链接
            html3 = askURL(url3)

            #2.3解析数据
            soup3 = BeautifulSoup(html3,"html.parser")
            # print(type(datalist2[1][1]))
            for item in zip(soup3.find_all('div',class_="contentbox")):  #得到小说一章的内容
                item = str(item)
                item = item.replace('&nbsp;', ' ')      #根据html规则手动转变文本
                item = item.replace('<br/>', '\n')
                item = item.replace('\n\n\n\n', '\n')
                item = item.replace(',)','')
                item = re.sub('<script.*?>(.*?)</script>','',item)  #去掉多余内容
                item = re.sub('<a .*?>(.*?)</a>','',item)
                item = re.sub(r'<div .*?>', '', item)
                item = re.sub(r'</div>', '', item)
                # print(item)     #测试小说内容

                textTitle = datalist2[z][1]
                print(textTitle)      #测试章节名
                z = z + 1
                item = textTitle+"\n"+item
                # print(item)      #测试整个章节

                save("F:\python_GET\小说\%s.txt"%(datalist[x][1]),item)

        x = x + 1
            # print(datalist3)
            # break       #测试一章是否能打印成功
        # break       #由于章节过多，循环一次进行测试
#得到指定一个url的内容

#保存小说
def save(filename, contents):                       #（文件名，保存数据）
    fh = open(filename, 'a', encoding='utf-8')      #在文本末尾写入
    fh.write(contents)
    fh.close()


def askURL(url):
    head ={                     #模拟浏览器头部信息，向豆瓣服务器发送消息
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
    }
                            #用户代理表示告诉豆瓣服务器，我们是什么类型的机器/浏览器（本质上是告诉浏览器，我们可以接受什么水平的文件）

    try:
        r = requests.get(url,headers=head,timeout=10)
        # 如果状态不是200，引发HTTPError异常
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        # print(r.text)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
        print("产生异常")
    # print(r.text)
    return r.text


































if __name__ == '__main__':
    print("开始爬取......")
    main()
    print("爬取成功！")