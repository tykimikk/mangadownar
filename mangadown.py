from bs4 import BeautifulSoup as bs
import requests , shutil, os
from termcolor import colored, cprint 
oriDir = os.getcwd()
def downloader(url):
    r = requests.get(url)
    c = r.content
    soup = bs(c,"html.parser")
    lastpage = howManypage(soup)
    chapnum = url.split("/")[-3]
    os.mkdir(chapnum)
    os.chdir(os.getcwd()+"/"+chapnum)
    for i in range (1, lastpage+1):
        pageurl = url.split("/")
        del pageurl[-1]
        del pageurl[-1]
        npageurl = "/".join(pageurl)+"/" + str(i)
        cprint(npageurl,"magenta")
        imgurl = getImgurl(npageurl)
        pagename = imgurl.split("/")[-1]
        r = requests.get(imgurl, stream = True)
        # Check if the image was retrieved successfully
        if r.status_code == 200:
            r.raw.decode_content = True
            with open(pagename,'wb') as f:
                shutil.copyfileobj(r.raw, f)
def howManypage(c):
    return int(c.find("div",{"class":"showchapterpagination"}).find_all("a")[5].text)
def getImgurl(url):
    r = requests.get(url)
    c = r.content
    soup = bs(c,"html.parser")
    return soup.find("div",{"id":"showchaptercontainer"}).find("a").find("img")["src"]
cprint("---------------------------------------------" , "magenta")    
cprint("----------  Manga Down By Ghassen  ----------","magenta","on_white")
cprint("---------------------------------------------" , "magenta")
cprint("Enter a manga name ","white")
cprint("------------------","magenta")
search = input()
sl = "https://manga.ae/manga/search:" + search
r = requests.get(sl)
c = r.content
soup = bs(c,"html.parser")
mcontainer = soup.find_all("div",{"class":"mangacontainer"})
if len(mcontainer) < 1:
    cprint("Zannen . No Manga with same name Found !!","red")
else :
    
    cprint("---------------------------------------------" , "magenta")
    for i in mcontainer :
        link = i.find("a")["href"]
        linklen = len(link)
        dash = "-"*int(linklen/2)
        
        name = i.find_all("a")[1].text
        cprint(str(mcontainer.index(i)+1)+ " - " +name,"magenta")
        # namear = i.find_all("a")[2].text
        
        cprint("---------------------------------------------" , "magenta")
        # cprint(link,"white")
    cprint("Yuupi , Select one Onegaishimassu","green")    
    cprint("Choose a number ..  ","green")    
    selected = int(input())-1
    ml = mcontainer[selected].find("a")["href"]
    mn = mcontainer[selected].find_all("a")[1].text.replace(":","")
    nc = requests.get(ml).content
    nsoup = bs(nc,"html.parser")
    chaptersbox = nsoup.find("ul",{"class":"new-manga-chapters"})
    chapters = chaptersbox.find_all("li")
    chapters.reverse()
    cprint(str(len(chapters)) + " Chapters found...","grey")
    os.mkdir(mn)
    cprint("1 Download all   2 Download by chapter  3 Download by range","magenta")
    dwchoice = int(input())
    if  dwchoice == 1:
        x=1
        for chapter in chapters :
            
            os.chdir(oriDir+"/"+mn)
            cl = chapter.find("a")["href"]
            try:
                downloader(cl)
                cprint("Reminder : To force stop press Ctrl+C twice","red")
            except:
                pass
            cprint(str(x)+" Chapters Downloaded")
            x+=1
    elif dwchoice == 2 :
        os.chdir(oriDir+"/"+mn)
        cprint("Choose one chapter","green" )
        choosenchap = int(input())
        cl = chapters[choosenchap-1].find("a")["href"]
        try :
            downloader(cl)
        except:
            pass    
        cprint("One Chapter Downloaded")
    elif dwchoice == 3 :
        cprint("choose first chapter","green")
        Rfrom = int(input())
        cprint("choose last chapter","green")
        Rto = int(input())
        x=1
        for i in range (Rfrom, Rto+1):
            os.chdir(oriDir+"/"+mn)
            cl = chapters[i-1].find("a")["href"]
            try:
                downloader(cl)
            except:
                pass
            cprint(str(x)+" Chapters Downloaded")    
            x+=1
            
        
   
        
