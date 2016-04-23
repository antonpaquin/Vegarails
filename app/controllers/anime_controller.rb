class AnimeController < ApplicationController
  protect_from_forgery with: :null_session

  def index
    @anime = Anime.all;
    #Sort anime somehow so that first things are first
  end

  def add
    begin
      @anime = Anime.create(
        :name => params[:name],
        :tvdb_id => params[:id]
      )
      @success = true
    rescue
      @success = false
    end
    render :add, :layout => false
  end

  def addEpisode
    begin
      if params[:anime_id] != nil
        id = params[:anime_id]
      elsif params[:anime_name] != nil
        id = Anime.where(name: params[:anime_name]).take.id
      else
        id = 0
      end
      Aniepisode.create(
        :name => params[:name],
        :anime_id => id,
        :length => params[:length],
        :season => params[:season],
        :episode => params[:episode],
        :watched => (params[:watched] == 'true' ? true : false),
        :file => params[:file]
        )
        @success = true
      rescue
        @success = false
      end
      render :addEpisode, :layout => false
  end

  def sync
    begin
      require 'open-uri'
      json = JSON.parse params[:shows]
      #Beautiful!
      inDb = {} #List of shows already in the db
      ids = {} #Way to get an ID from a name with fewer DB lookups
      Anime.find_each do |a| #For all shows
        ids[a.name] = a.id
        inDb[a.name] = {}
        Aniepisode.where(anime_id: a.id).find_each do |e| #for all episodes under that show
          if not inDb[a.name].key?(e.season)
            inDb[a.name][e.season] = Set.new []
          end
          inDb[a.name][e.season].add(e.episode) #stick each ep number in an unordered set
        end
      end
      json.each do |a|
        #If the anime isn't in the DB, add it (and put its ID in ids)
        if Anime.where(name: a['name']).take == nil
          Anime.create(:name => a['name'], :tvdb_id => a['tvdb_id'])
          ids[a['name']] = Anime.where(name: a['name']).take.id
          begin
            Dir.mkdir('/var/www/html/Vegarails/public/anime/'+a['name'])
            open('/var/www/html/Vegarails/public/anime/'+a['name']+'/box.jpg', 'wb') do |file|
              file << open(a['thumb_url']).read
            end
          rescue
          end
        end
        a['seasons'].each do |s|
          s['episodes'].each do |e|
            aName = a['name']
            sNum = s['number'].to_s.rjust(2,'0')
            eNum = e['number'].to_s.rjust(2,'0')
            if Aniepisode.where(anime_id: ids[a['name']], season: s['number'], episode: e['number']).take == nil
              doSyncEpisode(a, s, e, ids)
            end
            if !File.exists?("/var/www/html/Vegarails/public/anime/#{aName}/s#{sNum}e#{eNum}.jpg")
              doWriteThumbnail(a, s, e)
            end
          end
        end
      end

      #Pull db -- get a list of all shows [ seasons [ episodes]] --> verification array
      #json.each do add/update db, remove from verification array
      #verification arrray.each do remove from db
      @success = true
    rescue Exception => e
      @success = false
      @error = e.message
      @trace = e.backtrace.inspect
    end
    render :sync, :layout => false
  end

  def delete
  end

  def edit
  end

  def show
  end

  def stats
  end

  # Not actions!
  def doSyncEpisode(anime, season, episode, ids)
    aName = anime['name']
    sNum = season['number'].to_s.rjust(2,'0')
    eNum = episode['number'].to_s.rjust(2,'0')
    frm = episode['format']
    Aniepisode.create(
      :name => episode['name'],
      :anime_id => ids[anime['name']],
      :length => 0,
      :season => season['number'],
      :episode => episode['number'],
      :watched => false,
      :file => "/Media/Anime/#{aName}/Season #{sNum}/#{aName} - s#{sNum}e#{eNum}.#{frm}"
      )
  end

  def doWriteThumbnail(anime, season, episode)
    require 'open-uri'
    aName = anime['name']
    sNum = season['number'].to_s.rjust(2,'0')
    eNum = episode['number'].to_s.rjust(2,'0')
    begin
      if episode['thumb_url'] == ''
        raise
      end
      open("/var/www/html/Vegarails/public/anime/#{aName}/s#{sNum}e#{eNum}.jpg", 'wb') do |file|
        file << open(episode['thumb_url']).read
      end
    rescue
    end
  end
end
