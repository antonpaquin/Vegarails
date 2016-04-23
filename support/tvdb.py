import requests
from bs4 import BeautifulSoup
import pickle
from io import BytesIO
from zipfile import ZipFile
import sys

api_key = '8A508F4E2D203BF4'
sys.setrecursionlimit(3500) #Allow pickling some very nested structures
tvdb_file = '/var/www/html/Vegarails/support/tvdb.pk'
populated = []

try:
    f = open(tvdb_file,'rb')
    localCache = pickle.load(f)
except Exception:
    print('TVDB localCache empty, initializing empty')
    localCache = {}
finally:
    f.close()

def getEpisodeThumb(show, season, episode):
    verifyCache(show, season, episode)
    cached = localCache[show]['seasons'][season]['episodes'][episode]['thumb_url']
    if cached == '' or cached == 'http://thetvdb.com/banners/None':
        populate(show)
    verifyCache(show, season, episode)
    cached = localCache[show]['seasons'][season]['episodes'][episode]['thumb_url']
    if cached == 'http://thetvdb.com/banners/None':
        return ''
    return cached

def getShowThumb(show):
    verifyCache(show)
    if localCache[show]['box_url'] == '':
        populate(show)
    verifyCache(show)
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
    verifyCache(show)
    return localCache[show]['id']

def getEpisodeName(show, season, episode):
    verifyCache(show, season, episode)
    if localCache[show]['seasons'][season]['episodes'][episode]['name'] == '':
        populate(show)
    verifyCache(show, season, episode)
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
    if show in populated:
        return
    else:
        populated.append(show)
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
            number = int(episode.episodenumber.string)+0
            epName = str(episode.episodename.string)[:]
            epThumb = 'http://thetvdb.com/banners/'+str(episode.filename.string)[:]
            localCache[show]['seasons'][season]['episodes'][int(number)+0] = {
                'name':str(epName)[:],
                'thumb_url':str(epThumb)[:]
            }
    close()

def close():
    f = open(tvdb_file,'wb')
    pickle.dump(localCache, f)
    f.close()
'''
Sync:
    Anything in the JSON not in DB should be added
    Anything in DB not in JSON should be removed
    New anime get a new public/Anime/- folder + a downloaded box.jpg
    New episodes get a new downloaded se*ep*.jpg
'''
