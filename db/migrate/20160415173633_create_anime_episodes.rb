class CreateAnimeEpisodes < ActiveRecord::Migration
  def change
    create_table :anime_episodes do |t|
      t.belongs_to :customer, index: true
      t.string :name
      t.string :length
      t.integer :season
      t.integer :episode
      t.boolean :watched
      t.string :file

      t.timestamps null: false
    end
  end
end
