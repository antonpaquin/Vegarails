class CreateAnimes < ActiveRecord::Migration
  def change
    create_table :animes do |t|
      t.string :name
      t.integer :tvdb_id
      t.integer :sort_order

      t.timestamps null: false
    end
  end
end
