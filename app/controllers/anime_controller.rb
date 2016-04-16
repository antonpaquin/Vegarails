class AnimeController < ApplicationController
  def index
    @anime = Anime.all;
    #Sort anime somehow so that first things are first
  end

  def add
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
