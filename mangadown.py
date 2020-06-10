from bs4 import BeautifulSoup as bs
import requests , shutil, os
oriDir = r"C:\Users\Ghass\Desktop\mangadown"
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
        print(npageurl)
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
search = input("Enter a manga to search  ")
sl = "https://manga.ae/manga/search:" + search
r = requests.get(sl)
c = r.content
soup = bs(c,"html.parser")
mcontainer = soup.find_all("div",{"class":"mangacontainer"})
if len(mcontainer) < 1:
    print("No Manga With that name Found !!")
else :
    print ("Those mangas are found , Select one")
    for i in mcontainer :
        link = i.find("a")["href"]
        linklen = len(link)
        dash = "-"*int(linklen/2)
        print(dash + str(mcontainer.index(i)+1) + dash)
        name = i.find_all("a")[1].text
        print(name)
        namear = i.find_all("a")[2].text
        print(namear)
        
        print(link)
    selected = int(input("select a number  "))-1
    ml = mcontainer[selected].find("a")["href"]
    mn = mcontainer[selected].find_all("a")[1].text.replace(":","")
    nc = requests.get(ml).content
    nsoup = bs(nc,"html.parser")
    chaptersbox = nsoup.find("ul",{"class":"new-manga-chapters"})
    chapters = chaptersbox.find_all("li")
    chapters.reverse()
    print(str(len(chapters)) + " chapters Found...")
    os.mkdir(mn)
    
    dwchoice = int(input("1 Download All   2 Download by chapter  3 download by range"))
    if  dwchoice == 1:
        for chapter in chapters :
            os.chdir(oriDir+"/"+mn)
            cl = chapter.find("a")["href"]
            downloader(cl)
            
    elif dwchoice == 2 :
        os.chdir(oriDir+"/"+mn)
        choosenchap = int(input("choose a chapter  "))
        cl = chapters[choosenchap-1].find("a")["href"]
        downloader(cl)
        
    elif dwchoice == 3 :
        Rfrom = int(input("choose a starting chapter  "))
        Rto = int(input("choose an End chapter  "))
        for i in range (Rfrom, Rto+1):
            os.chdir(oriDir+"/"+mn)
            cl = chapters[i-1].find("a")["href"]
            downloader(cl)
            
        
    
        
