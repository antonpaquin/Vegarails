class AnimeController < ApplicationController
  protect_from_forgery with: :null_session

  def index
    @anime = Anime.all;
    #Sort anime somehow so that first things are first
  end

  def add
    begin
      createAnime(httpParams)
      @success = true
    rescue Exception => e
      @success = false
      @error = e.message
      @trace = e.backtrace.inspect
    end
    render :apiResults, :layout => false
  end

  def addEpisode
    begin
      createEpisodeFromHttpParams(httpParams)
      @success = true
    rescue Exception => e
      @success = false
      @error = e.message
      @trace = e.backtrace.inspect
    end
    render :apiResults, :layout => false
  end

  def sync
    begin
      ids = {} #Way to get an ID from a name with fewer DB lookups
      Anime.find_each do |a| #For all shows
        ids[a.name] = a.id
      end
      JSON.parse(params[:shows]).each do |a|
        #If the anime isn't in the DB, add it (and put its ID in ids)
        if Anime.where(name: a['name']).take == nil
          createAnime({name: a['name'], id: a['tvdb_id'], thumb_url: a['thumb_url']})
          ids[a['name']] = Anime.where(name: a['name']).take.id
        end
        a['seasons'].each do |s|
          s['episodes'].each do |e|
            if Aniepisode.where(anime_id: ids[a['name']], season: s['number'], episode: e['number']).take == nil
              createEpisode(a, s, e, ids[a['name']])
            end
            if !File.exists?(episodeThumbnail(a['name'], s['number'], e['number']))
              writeEpisodeThumbnail(a, s, e)
            end #IF
          end #S - each
        end #A - each
      end #JSON - each
      @success = true
    rescue Exception => e
      @success = false
      @error = e.message
      @trace = e.backtrace.inspect
    end
    render :apiResults, :layout => false
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
  private

  def createAnime(params)
    if params[:sort_order] == nil
      params[:sort_order] = 0
    end

    #DB Add
    Anime.create(
      name: params[:name],
      tvdb_id: params[:id],
      sort_order: params[:sort_order]
      )

    #Support add
    if params[:thumb_url] != nil
      require 'open-uri'
      begin
        Dir.mkdir(showDir(a['name']))
      rescue #Directory probably already exists, daijoubu
      end
      begin
        open(showThumbnail(a['name']), 'wb') do |file|
          file << open(a['thumb_url']).read
        end
      rescue
      end
    end
  end

  def createEpisode(anime, season, episode, id)
    Aniepisode.create(
      :name => episode['name'],
      :anime_id => id,
      :season => season['number'],
      :episode => episode['number'],
      :watched => false,
      :file => episodeFile(aName, season['number'], episode['number'], episode['format'])
      )
  end

  def createEpisodeFromHttpParams(httpParams)
    if params[:anime_id] != nil
      id = params[:anime_id]
      name = Anime.where(id: id).take.name
    elsif params[:anime_name] != nil
      name = params[:anime_name]
      id = Anime.where(name: name).take.id
    else
      raise ArgumentError, 'Episode cannot be created without a name or id'
    end
    anime = {'name' => name}
    season = {'number' => httpParams[:season]}
    episode = {
      'number' => httpParams[:episode],
      'format' => httpParams[:file][-3,3],
      'name' => httpParams[:name]
    }
    createEpisode(anime, season, episode, id)
  end

  def writeEpisodeThumbnail(anime, season, episode)
    require 'open-uri'
    begin
      if episode['thumb_url'] == ''
        raise
      end
      open(episodeThumbnail(anime['name'], season['number'], episode['number']), 'wb') do |file|
        file << open(episode['thumb_url']).read
      end
    rescue
    end
  end

  def episodeThumbnail(aName, sNum, eNum)
    "/var/www/html/Vegarails/public/anime/#{aName}/s#{sNum.to_s.rjust(2,'0')}e#{eNum.to_s.rjust(2,'0')}.jpg"
  end

  def showThumbnail(aName)
    showDir(aName) + '/box.jpg'
  end

  def episodeFile(aName, sNum, eNum, frm)
    "/Media/Anime/#{aName}/Season #{sNum.to_s.rjust(2,'0')}/#{aName} - s#{sNum.to_s.rjust(2,'0')}e#{eNum.to_s.rjust(2,'0')}.#{frm}"
  end

  def showDir(aName)
    "/var/www/html/Vegarails/public/anime/#{aName}"
  end
end
