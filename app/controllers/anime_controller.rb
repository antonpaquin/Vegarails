class AnimeController < ApplicationController
  protect_from_forgery with: :null_session
  #skip_before_filter :verify_authenticity_token, :if => Proc.new { |c| c.request.format == 'application/json' }


  def index
    @anime = Anime.all;
    #Sort anime somehow so that first things are first
  end

  def add
    begin
      @anime = Anime.create(
        :name => params[:name],
        :count => 0
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
      @json = JSON.parse params[:shows]
      @success = true
    rescue
      @success = false
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
end
