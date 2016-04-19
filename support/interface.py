import os
import shutil

os.chdir('/home/pi/drive')

def rjust(num):
    return '0'*(2-len(str(num)))+str(num)

def doMove(name, season, episode, src):
    shutil.move('/home/pi/drive/torrents/Anime-bot/complete/'+src,
                '/home/pi/drive/Media/Anime/'+name+'/Season '+rjust(season)+'/'+name+' - s'+rjust(season)+'e'+rjust(episode)+src[src.find('.'):])

torrents = [f for f in os.listdir('/home/pi/drive/torrents/Anime-bot/complete') if f[0:14] == '[HorribleSubs]']

data = [(t[15:t.find('-')-1], int(t[-13:-11]), t) for t in torrents]

confFile = open('/var/www/html/Vegarails/support/torrentPaths.txt','r')
conf = {}
for l in confFile.readlines():
    key = l[:l.find('=')]
    name = l[l.find('=')+1:l.find('|')]
    season = int(l.strip()[l.find('|')+1:])
    conf[key] = (name, season)

for d in data:
    if d[0] in conf.keys():
        name = conf[d[0]][0]
        season = conf[d[0]][1]
    else:
        name = d[0]
        season = 1
    if not os.path.exists('/home/pi/drive/Media/Anime/'+name):
        os.mkdir('/home/pi/drive/Media/Anime/'+name)
    if not os.path.exists('/home/pi/drive/Media/Anime/'+name+'/Season '+rjust(season)):
        os.mkdir('/home/pi/drive/Media/Anime/'+name+'/Season '+rjust(season))
    doMove(name, season, d[1], d[2])
