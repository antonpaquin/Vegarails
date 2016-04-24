class CreateAniepisodes < ActiveRecord::Migration
  def change
    create_table :aniepisodes do |t|
      t.integer :anime_id
      t.string :name
      t.integer :season
      t.integer :episode
      t.boolean :watched
      t.string :file

      t.timestamps null: false
    end
  end
end
