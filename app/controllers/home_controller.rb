class HomeController < ApplicationController
  def show
    @services = {
      :self => Service.where(category: 0).all.map {|s| s.name},
      :third => Service.where(category: 1).all.map {|s| s.name}}
  end
end
