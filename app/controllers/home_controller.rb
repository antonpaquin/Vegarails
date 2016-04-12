class HomeController < ApplicationController
  def show
    @services = {:self => ['Manga', 'Webcomics', 'Anime', 'Music', 'FTP'], :third => ['Deluge', 'Plex']}
  end
end
