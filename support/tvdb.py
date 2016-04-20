import requests
from bs4 import BeautifulSoup
import pickle
from io import BytesIO
from zipfile import ZipFile
import sys

api_key = '8A508F4E2D203BF4'
sys.setrecursionlimit(3500) #Allow pickling some very nested structures

try:
    f = open('tvdb.pk','rb')
    localCache = pickle.load(f)
except Exception:
    print('TVDB localCache empty, initializing empty')
    localCache = {}
finally:
    f.close()

def getEpisodeThumb(show, season, episode):
    verifyCache(show, season, episode)
    if localCache[show]['seasons'][season]['episodes'][episode]['thumb_url'] == '':
        populate(show)
    return localCache[show]['seasons'][season]['episodes'][episode]['thumb_url']

def getShowThumb(show):
    verifyCache(show)
    if localCache[show]['box_url'] == '':
        populate(show)
    return localCache[show]['box_url']

def getTvdbId(show):
    verifyCache(show)
    if localCache[show]['id'] == '':
        endpoint = 'http://thetvdb.com/api/GetSeries.php?seriesname=' + show
        r = requests.get(endpoint)
        soup = BeautifulSoup(r.text, 'lxml')
        firstResult = soup.find('series')
        localCache[show]['id'] = str(firstResult.seriesid.string)[:]
        #Something in the localCache was pickling to some massive xml blob which
        #basically included the whole downloaded file from TVDB. Force
        #everything to absolutely be a primitive no matter what, problem goes
        #away.
    return localCache[show]['id']

def getEpisodeName(show, season, episode):
    verifyCache(show, season, episode)
    if localCache[show]['seasons'][season]['episodes'][episode]['name'] == '':
        populate(show)
    return localCache[show]['seasons'][season]['episodes'][episode]['name']

def verifyCache(show, season=-1, episode=-1):
    if show not in localCache.keys():
        localCache[str(show)[:]] = {
        'box_url':'',
        'seasons':{},
        'id':''
        }
    if season != -1 and season not in localCache[show]['seasons'].keys():
        localCache[show]['seasons'][int(season)+0] = {
        'episodes':{}
        }
    if episode != -1 and episode not in localCache[show]['seasons'][season]['episodes'].keys():
        localCache[show]['seasons'][season]['episodes'][int(episode)+0] = {
        'name':'',
        'thumb_url':''
        }

def populate(show):
    showId = getTvdbId(show)
    endpoint = 'http://thetvdb.com/api/{apikey}/series/{showId}/all/en.zip'.format(apikey=api_key, showId=showId)
    r = requests.get(endpoint)
    z = ZipFile(BytesIO(r.content))
    dataFile = z.open('en.xml')
    data = BeautifulSoup(dataFile.read(),'lxml')
    dataFile.close()
    bannerFile = z.open('banners.xml')
    banners = BeautifulSoup(bannerFile.read(),'lxml')
    bannerFile.close()

    box_url = ''
    for b in banners.find_all('banner'):
        if b.bannertype.string == 'fanart':
            box_url = 'http://thetvdb.com/banners/'+b.bannerpath.string
            break
    localCache[show]['box_url'] = str(box_url)[:]
    seasons = set([int(s.string) for s in data.find_all('seasonnumber') if s.string != '0'])
    for season in seasons:
        localCache[show]['seasons'][int(season)+0] = {'episodes':{}}
        episodes = [e for e in data.find_all('episode') if int(e.seasonnumber.string) == season]
        for episode in episodes:
            number = int(episode.episodenumber.string)
            epName = episode.episodename.string
            epThumb = 'http://thetvdb.com/banners/'+episode.filename.string
            localCache[show]['seasons'][season]['episodes'][int(number)+0] = {
                'name':str(epName)[:],
                'thumb_url':str(epThumb)[:]
            }

def close():
    f = open('tvdb.pk','wb')
    pickle.dump(localCache, f)
    f.close()
'''
Sync:
    Anything in the JSON not in DB should be added
    Anything in DB not in JSON should be removed
    New anime get a new public/Anime/- folder + a downloaded box.jpg
    New episodes get a new downloaded se*ep*.jpg
'''
