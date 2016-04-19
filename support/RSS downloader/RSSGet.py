import os
import requests
from bs4 import BeautifulSoup

os.chdir('/var/www/html/Vegarails/support/RSS downloader')
def main():
    openHistory()
    chain(
        getSources,
        foreach(
            sourceToPage,
            pageToSoup,
            soupToItems,
            foreach(
                checkUniqueItem,
                getTorrentLink,
                downloadTorrentFile,
                saveUniqueItem
                )
            )
        )
    closeHistory()

def chain(*funcs, arg = False):
    #control flow: call one thing after the other using the results of the last call
    #arg is the initial parameter passed to the first function
    if arg:
        r = funcs[0](arg)
    else:
        r = funcs[0]()
    for f in funcs[1:]:
        r = f(r)
    return r

def foreach(*funcs):
    #generates a function that, given an iter input, chains a set of funcs over each element
    def f(inp):
        res = []
        for n in inp:
            res.append(chain(*funcs, arg=n))
        return res
    return f

def getSources():
    #get all the rss links to crawl
    f = open('sources/nyaa.txt','r')
    return f.readlines()

def sourceToPage(link):
    #from website link, get the content of that page
    return requests.get(link).text

def pageToSoup(text):
    #from a bunch of xml, return a BS4 soup object
    return BeautifulSoup(text, "html.parser")

def soupToItems(soup):
    #given a nyaa rss feed thing, get all the items in it
    print(soup.prettify())
    return soup.channel.findAll('item')

uniqueName = ''
uniqueTable = set([])
def checkUniqueItem(item):
    #check if this thing has been downloaded before
    global uniqueName
    if(item.title.string not in uniqueTable):
        uniqueName = item.title.string
        return item
    else:
        return False

def getTorrentLink(item):
    #given a nyaa rss feed item, pull the DL link to the torrent from it
    if item:
        print('getTorrentLink')
        return item.link.string
    else:
        return False

def downloadTorrentFile(link):
    #given a torrent link, save it as a file
    if link:
        print('downloadTorrentFile')
        fname = generateFileName('torrent')
        f = open(fname,'wb')
        f.write(requests.get(link).content)
        f.close()
        return True
    else:
        return False

def saveUniqueItem(unique):
    if unique:
        print('saveUniqueItem')
        uniqueTable.add(uniqueName)
    else:
        pass #object is in table

def openHistory():
    global uniqueTable
    f = open('history.txt','r')
    uniqueTable = set([n[:-1] for n in f.readlines()])
    f.close()

def closeHistory():
    f = open('history.txt','w')
    for n in uniqueTable:
        f.write(n + '\n')
    f.close()

def generateFileName(extension):
    #create unique filenames for torrents by simply adding 1 to the last one
    l = os.listdir('files')
    if l:
        n = int(l[-1].split('.')[0])
        return 'files/' + str(n+1) + '.' + extension
    else:
        return 'files/' + '1.' + extension

main()
