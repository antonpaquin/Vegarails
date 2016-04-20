import os
import shutil

os.chdir('/home/pi/drive')
class Struct(object): #This is magic don't worry
    pass
anime_path = '/home/pi/drive/Media/Anime'

def main():
    files = readTorrentDir()
    adjustNames(files)
    for f in files:
        doMove(d.name, d.season, d.epNum, d.src)

def readTorrentDir():
    torrents = [f for f in os.listdir('/home/pi/drive/torrents/Anime-bot/complete') if f[0:14] == '[HorribleSubs]']
    data = []
    for t in torrents:
        d = Struct()
        d.name = t[15:-16]
        d.epNum = int(t[-13:-11])
        d.src = t
        d.season = 1
        data.append(d)
    return data

def adjustNames(data):
    conf = getTorrentConfig()
    for d in data:
        if d.name in conf.keys():
            d.name = conf[d.name].name
            d.season = conf[d.name].season

def makePaths(data):
    for d in data:
        showPath = anime_path + '/' + d.name
        seasonPath = showPath + '/Season ' + rjust(d.season)
        if not os.path.exists(showPath):
            os.mkdir(showPath)
        if not os.path.exists(seasonPath):
            os.mkdir(seasonPath)

def getTorrentConfig():
    confFile = open('/var/www/html/Vegarails/support/torrentPaths.txt','r')
    conf = {}
    for l in confFile.readlines():
        key = l[:l.find('=')]
        value = Struct()
        value.name = l[l.find('=')+1:l.find('|')]
        value.season = int(l.strip()[l.find('|')+1:])
        conf[key] = value
    return conf

def doMove(name, season, episode, src):
    shutil.move('/home/pi/drive/torrents/Anime-bot/complete/'+src,
                '/home/pi/drive/Media/Anime/'+name+'/Season '+rjust(season)+'/'+name+' - s'+rjust(season)+'e'+rjust(episode)+src[src.find('.'):])

def rjust(num):
    return '0'*(2-len(str(num)))+str(num)

main()
