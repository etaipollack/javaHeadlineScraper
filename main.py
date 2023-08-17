# Etai Pollack
# -*- coding: utf-8 -*-
import webbrowser
import urllib.request
import requests
from bs4 import BeautifulSoup

def generateWebpage(linkDict, newsName):
    fout = open("headlines.html", "w")
    fout.write("""
<!DOCTYPE HTML>
<HTML>
<HEAD>
    <TITLE> HEADLINES </TITLE>\n
    <link rel="stylesheet" href="mystyle.css">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
</HEAD>
<BODY>
""")
    fout.write("    <H1> Today's News for " + newsName + "</H1>\n")
    fout.write("    <ul>\n")

    for key, value in linkDict.items():
        fout.write('        <LI><a target="_blank" href="' + key + '">' + value + '</a></LI>\n')
    
    fout.write("    </ul>\n")
    fout.write("</BODY>\n")
    fout.write("</HTML>\n")
    fout.close()

def getHeadline(linkList, newsName):
    links = dict()
    for curLink in linkList:
        urlHeadline = curLink
        responseHeadline = requests.get(urlHeadline)
        soupHeadline = BeautifulSoup(responseHeadline.text, 'html.parser')
        headlinesList = soupHeadline.find('body').find_all('h1')
        headline = ""
        for cur in headlinesList:
            headline = str(cur.text.strip())
        links[str(curLink)] = headline
    generateWebpage(links, newsName)


def getCNN():
    url='https://www.cnn.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    headlineLinks = soup.find('body').find_all('div')

    tempList = []
    print("Loading (This might take a while)...")
    for cur in headlineLinks:
        curLink = str(cur)
        if curLink.find('data-link-type="article"') != -1 :
            linkPart1 = curLink[curLink.find('href="/'):]
            linkPart2 = linkPart1[6:linkPart1.find('">')]
            tempList.append("https://www.cnn.com" + linkPart2)

    noDuplicateLinkList = list(set(tempList))
    getHeadline(noDuplicateLinkList, "CNN")


def getBBC():
    url='https://www.bbc.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    headlineLinks = soup.find_all("a", class_="block-link__overlay-link")

    tempList = []

    for link in headlineLinks:
        link_url = link["href"]
        if link_url.find("https") != 0:
            tempList.append("https://bbc.com/" + str(link_url))
        else:
            tempList.append(str(link_url))

    getHeadline(tempList, "BBC")

def getNYT():
    url='https://www.nytimes.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    headlineLinks = soup.find_all("a", class_="css-9mylee")

    links = dict()

    for link in headlineLinks:
        link_url = link["href"]
        h3element = link.find_all("h3")
        headline = ""
        if str(link_url) != "https://www.nytimes.com/games/wordle/index.html" and str(link_url) != "https://www.nytimes.com/spotlight/wordle-review" and str(link_url) != "https://nytimes.com/games/digits" and str(link_url) != "https://www.nytimes.com/puzzles/spelling-bee" and str(link_url) != "https://www.nytimes.com/crossword" and str(link_url) != "https://www.nytimes.com/puzzles/letter-boxed" :
            for cur in h3element:
                headline = cur
                links[str(link_url)] = str(headline)

    url = 'https://www.nytimes.com/section/todayspaper'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    headlineLinks = soup.find_all("div", class_="css-141drxa")

    for link in headlineLinks:
        link_url = str(link.find_all("a"))
        link_url = "https://nytimes.com" + link_url[link_url.find('href="') + 6 : link_url.find('">')]
        h2element = link.find_all("h2")
        headline = ""
        if str(link_url) != "https://www.nytimes.com/games/wordle/index.html" and str(link_url) != "https://www.nytimes.com/spotlight/wordle-review" and str(link_url) != "https://nytimes.com/games/digits" and str(link_url) != "https://www.nytimes.com/puzzles/spelling-bee" and str(link_url) != "https://www.nytimes.com/crossword" and str(link_url) != "https://www.nytimes.com/puzzles/letter-boxed" :
            for cur in h2element:
                headline = cur
                links[str(link_url)] = str(headline)
        

    generateWebpage(links, "New York Times")

def start():
    user_choice = input("Hello, welcome to HeadlineScraper v1.1.2. The current news sources to recieve a headline are New York Times(0), BBC(1), and CNN(2)")
    if user_choice == "0":
        getNYT()
    elif user_choice == "1":
        getBBC()
    elif user_choice == "2":
        getCNN()
    else:
        print("That was not a correct choice.")
        start()




start()















