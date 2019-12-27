import requests
from bs4 import BeautifulSoup
import os
response=requests.get("http://xxxx")
response_text=BeautifulSoup(response.text,"html.parser")
page_numbers=int(response_text.find_all("a",class_="page-numbers")[-2].text.split(" ")[1])      #拿到网站首页的总页码
for page_number in range(1,page_numbers+1):
    page_number=str(page_number)
    page_url="http://xiuren.me/page/"+page_number       #根据总页码，拼接页码页面的URL
    response=requests.get(page_url)
    response_text=BeautifulSoup(response.text,"html.parser")
    img_lis=response_text.find_all("li",class_="i_list")        #获取当前页面上的所有图片图册，以列表形式输出
    for img_li in img_lis:
        img_li_href=img_li.a.get("href")       #获取每个图册的URL
        response=requests.get(img_li_href)
        response_text=BeautifulSoup(response.text,"html.parser")
        img_title=response_text.find("h1").text         #获取文章标题
        for i in ['\\','/',':','*','?','"','<','>','!','|']:        #去除文章标题包含的特殊符号
                while i in img_title:
                    img_title = img_title.strip().replace(i, '')
        img_path="D:\\爬虫\\images\\"+img_title
        if not os.path.exists(img_path):
            os.mkdir(img_path)          #创建由文章标题命名的文件夹，以文章标题分类存放图片
            img_href=response_text.find_all("img")                      #找到所有的img标签，并以列表显示
            for img in img_href:                                        #循环img_href（所有的img标签列表）
                img_name=img.get("src").split("/")[-1].split(".")[0]                                 #取出每个img中的图片alt属性
                if img_name.isdigit():
                    download_img=requests.get(img.get("src"))               #取出每个img中的src链接
                    file_path=img_path+"\\"+img_name+".jpg"       #根据图片alt来拼接保存的地址和图片文件名
                    with open(file_path,"wb") as file:                      #以二进制的形式写入到文件中，没有该文件即创建写入
                        file.write(download_img.content)
            print("图片保存完成")


