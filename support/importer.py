#THIS IS SHITTY CODE! IT WAS ONLY MEANT TO BE USED ONCE. REWRITE IT IF YOU NEED TO USE IT!
raise
import requests
import os
from bs4 import BeautifulSoup
import zipfile
from io import BytesIO
from pprint import pprint

addUrl = 'http://vega.local/anime/addEpisode'
tvdb_apikey = '8A508F4E2D203BF4'

def addAnime(name, anime_name, season, episode, watched):
    data = {
        'name': name,
        'anime_name': anime_name,
        'length': '0',
        'season': season,
        'episode': episode,
        'watched': 'true' if watched else 'false',
        'file': '/Media/Anime/'+anime_name+'/Season '+just(season)+'/'+anime_name+' - s'+just(season)+'e'+just(episode)+'.mkv'
    }
    requests.post(addUrl, data)

def addMajor(name):
    os.mkdir('/var/www/html/Vegarails/public/anime/'+name)
    endpoint = 'http://vega.local/anime/add'
    data = {
        'name': name
    }
    requests.post(endpoint, data)

def just(i):
    return '0'*(2-len(str(i)))+str(i)

def go():
    os.chdir('/home/pi/drive/Media/Anime')
    for d in os.listdir(): #for each show
        try:
            addMajor(d)
        except Exception:
            continue
        sid = getSeriesId(d)
        if sid != -1:
            info = getSeriesInfo(sid)
        else:
            continue
        for s in os.listdir(d): #for each season
            try:
                season = int(s[-1])
            except Exception:
                continue
            seasonInfo = [se.parent for se in info.find_all('seasonnumber', text=str(season))]
            for e in os.listdir(d+'/'+s):
                episode = int(e[-6:-4])
                episodeinfo = [ep for ep in seasonInfo if ep.episodenumber.string == str(episode)][0]
                name = episodeinfo.episodename.string
                addAnime(name, d, str(season), str(episode), False)
                f = open('/var/www/html/Vegarails/public/anime/'+d+'/s'+just(season)+'e'+just(episode)+'.jpg','wb')
                r = requests.get('http://thetvdb.com/banners/'+episodeinfo.filename.string)
                f.write(r.content)
                f.close()



def getSeriesId(name):
    r = requests.get('http://thetvdb.com/api/GetSeries.php?seriesname=' + requests.utils.quote(name))
    soup = BeautifulSoup(r.text, "html5lib")
    num = len(soup.find_all('series'))
    if num==0:
        print('Nothing found for '+name+'! Skipping')
        return -1
    elif num>1:
        series = soup.find_all('series')
        for s in series:
            print(s.overview.string)
            print('y to accept:')
            if input() == 'y':
                return s.id.string
        print('None accepted!')
        return -1
    else:
        return soup.find('series').id.string


def getSeriesInfo(sid):
    r = requests.get('http://thetvdb.com/api/'+tvdb_apikey+'/series/'+sid+'/all/en.zip')
    f = zipfile.ZipFile(BytesIO(r.content)).open('en.xml')
    soup = BeautifulSoup(f.read(), "html5lib")
    f.close()
    return soup

go()
