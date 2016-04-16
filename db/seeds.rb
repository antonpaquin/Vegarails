# This file should contain all the record creation needed to seed the database with its default values.
# The data can then be loaded with the rake db:seed (or created alongside the db with db:setup).
#
# Examples:
#
#   cities = City.create([{ name: 'Chicago' }, { name: 'Copenhagen' }])
#   Mayor.create(name: 'Emanuel', city: cities.first)


services = [
#  Name         Category
  ['Anime',     0],
  ['Manga',     0],
  ['Webcomics', 0],
  ['FTP',       0],
  ['Settings',  0],
  ['Deluge',    1],
  ['Plex',      1]
]

anime = [
#  Name            Count
  ['Kuma Miko',    2 ],
  ['Katanagatari', 12],
  ['Monogatari',   26],
  ['Kyousougiga',  10]
]

def plexform(name, ep, season)
  '/home/pi/drive/Media/Anime/' + name + '/Season 0' + season + '/' + name + ' - s0' + season + 'e0' + ep + '.mkv'
end
anime_episodes = [
#  Name                                Anime_id   Length   Season   Episode  Watched  File
  ['Time for Bear and Girl to Part',   1,         '25:00', 1,       1,       true,    plexform('Kuma Miko', '1', '1')    ],
  ['A Hard Road',                      1,         '25:00', 1,       1,       false,   plexform('Kuma Miko', '2', '1')    ],
  ['Kanna, the Cutting Sword',         2,         '0',     1,       1,       true,    plexform('Katanagatari', '1', '1') ],
  ['Namakura, the Decapitation Sword', 2,         '0',     1,       2,       true,    plexform('Katanagatari', '2', '1') ],
  ['Tsurugi, the Sword of Thousand',   2,         '0',     1,       3,       true,    plexform('Katanagatari', '3', '1') ],
  ['Hari, the Slender Sword',          2,         '0',     1,       4,       true,    plexform('Katanagatari', '4', '1') ],
  ['Yoroi, the Rebel Sword',           2,         '0',     1,       5,       true,    plexform('Katanagatari', '5', '1') ],
  ['Kanazuchi, the Twin Swords',       2,         '0',     1,       6,       true,    plexform('Katanagatari', '6', '1') ],
  ['Bita, the Evil Sword',             2,         '0',     1,       7,       true,    plexform('Katanagatari', '7', '1') ],
  ['Sai, the Minute',                  2,         '0',     1,       8,       true,    plexform('Katanagatari', '8', '1') ],
  ['Nokogiri, the Sword of Kings',     2,         '0',     1,       9,       true,    plexform('Katanagatari', '9', '1') ],
  ['Hakari, the Sword of Truth',       2,         '0',     1,       10,      true,    plexform('Katanagatari', '10', '1')],
  ['Mekki, the Poison Sword',          2,         '0',     1,       11,      true,    plexform('Katanagatari', '11', '1')],
  ['Juu, the Flame Sword',             2,         '0',     1,       12,      true,    plexform('Katanagatari', '12', '1')]
]

services.each do |name, category|
  Service.create(:name => name, :category => category)
end

anime.each do |name, count|
  Anime.create(:name => name, :count => count)
end

anime_episodes.each do |name, anime_id, length, season, episode, watched, file|
  Aniepisode.create(:name => name, :anime_id => anime_id, :length => length, :season => season, :episode => episode, :watched => watched, :file => file)
end
