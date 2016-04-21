import os
import requests
import tvdb
import json

animeDir = '/home/pi/drive/Media/Anime'
syncEndPoint = 'http://vega.local/anime/sync'

os.chdir(animeDir)

def main():
    data = buildJSON()
    r = requests.post(syncEndPoint, {'shows':json.dumps(data)})
    log = open('/var/www/html/Vegarails/support/importerLog.html','w')
    log.write(r.text)
    log.close()

def buildJSON():
    shows = os.listdir(animeDir)
    jdat = []
    for show in shows:
        shName = show
        seasons = [f for f in os.listdir(animeDir + '/' + show) if f != 'Specials']
        seasonsL = []
        for season in seasons:
            seNum = int(season[-2:])
            episodes = os.listdir(animeDir + '/' + show + '/' + season)
            episodesL = []
            for episode in episodes:
                epNum = int(episode[-6:-4])
                frmat = episode[-3:]
                epName = tvdb.getEpisodeName(shName, seNum, epNum)
                epThumb = tvdb.getEpisodeThumb(shName, seNum, epNum)
                episodesL.append({
                    'number':epNum,
                    'format':frmat,
                    'name':epName,
                    'thumb_url':epThumb
                })
            seasonsL.append({
                'number':seNum,
                'episodes':episodesL
            })
        jdat.append({
            'name':shName,
            'thumb_url':tvdb.getShowThumb(shName),
            'tvdb_id':tvdb.getTvdbId(shName),
            'seasons':seasonsL
        })
    return jdat

main()

''' Example JSON:
{
   "shows":[
      {
         "name":"Bakuon",
         "thumb_url":"http://tvdb.com/banners/???.jpg",
         "tvdb_id":"696969696969",
         "seasons":[
            {
               "number":1,
               "episodes":[
                  {
                     "number":1,
                     "format":"mkv",
                     "name":"Motahbaiku - s01e01.mkv",
                     "thumb_url":"tvdb.com/banners/???.jpg"
                  }
               ]
            }
         ]
      }
   ]
}
'''
