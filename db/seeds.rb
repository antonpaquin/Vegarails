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

services.each do |name, category|
  Service.create(:name => name, :category => category)
end
