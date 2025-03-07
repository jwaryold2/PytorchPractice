from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from dotenv import load_dotenv
import requests
import re
import os

#Function Declarations

#Retrieves a find all div class soup, then obtains the title strings for each manga adding to a list and returning the list
#titleArray - the list of manga titles retrieved from the find all soup
def CleanTitleRetrieve(soupfa):
    titleArray=[]
    for x in range(len(soupfa)):
        titleArray.append(soupfa[x].find_all("a", {"class": "tooltip"})[1].text)
    return titleArray

#Retrieves the uncleaned ie (title-titile-title) version for better use later on
def UncleanTitleRetrievel(soupfa):
    unclean = []
    for x in range(len(soupfa)):
        unclean.append(iuf[x].find_all("a")[0].get("href")[len("https://www.mangakakalot.gg/manga/"):])
    return unclean

#Retrieving the link for every manga prechapter choice
def PreChapterLink(soupfa):
    link=[]
    for x in range(len(soupfa)):
        link.append(iuf[x].find("a", {"class":"tooltip"}).get("href")+"/chapter-")
    return link

#retrieve chapter numbers for specific manga
def ChapterNumberRetrieval(manganame):
    req2 = Request(f"https://www.mangakakalot.gg/manga/{manganame}",
                   headers={'User-Agent': 'Mozilla/5.0'})
    html_page = urlopen(req2).read()
    soup2 = BeautifulSoup(html_page, 'html.parser')

    chapters = soup2.find_all("div", {"class": "row"})
    chapters = chapters[1:]
    return(chapters[0].find("a").text.split(" ")[1])


req = Request("https://www.mangakakalot.gg/", headers={'User-Agent': 'Mozilla/5.0'})
html_page = urlopen(req).read()

soup = BeautifulSoup(html_page, 'html.parser')
doreamon = soup.find_all('div', {"class":"doreamon"})

#Retrieving itemupdate first boxes
iuf = soup.find_all("div", {"class":"itemupdate first"})
