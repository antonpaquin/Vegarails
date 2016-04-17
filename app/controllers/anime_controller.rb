class AnimeController < ApplicationController
  protect_from_forgery with: :null_session

  def index
    @anime = Anime.all;
    #Sort anime somehow so that first things are first
  end

  def add
    @anime = Anime.new(params[:anime])
  end

  def addEpisode
    begin
      Aniepisode.create(
        :name => params[:name],
        :anime_id => params[:anime_id],
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

  def delete
  end

  def edit
  end

  def show
  end

  def stats
  end
end
