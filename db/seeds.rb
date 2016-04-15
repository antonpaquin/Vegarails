# This file should contain all the record creation needed to seed the database with its default values.
# The data can then be loaded with the rake db:seed (or created alongside the db with db:setup).
#
# Examples:
#
#   cities = City.create([{ name: 'Chicago' }, { name: 'Copenhagen' }])
#   Mayor.create(name: 'Emanuel', city: cities.first)


services = [
  #Name         #Category
  ['Anime',     0],
  ['Manga',     0],
  ['Webcomics', 0],
  ['FTP',       0],
  ['Settings',  0],
  ['Deluge',    1],
  ['Plex',      1]
]

anime = [
  #Name           #Count
  ['TestAnime',   1]
]

anime_episodes = [
  #Name             #Length   #Season   #Episode  #Watched  #File
  ['TestEpisode',   '25:00',  1,        1,        true,     '/home/pi/drive/*']
]

services.each do |name, category|
  Service.create(:name => name, :category => category)
end

anime.each do |name, count|
  Anime.create(:name => name, :count => count)
end

anime_episodes.each do |name, length, season, episode, watched, file|
  AnimeEpisode.create(:name => name, :length => length, :season => season, :episode => episode, :watched => watched, :file => file)
end
