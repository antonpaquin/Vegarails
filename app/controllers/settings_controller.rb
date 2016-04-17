class SettingsController < ApplicationController
  def index
  end

  def authenticate
    render :authenticate, :layout => false
  end
end
