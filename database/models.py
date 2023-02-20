from peewee import *


db = SqliteDatabase('favourites.db')


class Favourites(Model):
    user_id = TextField()
    title_id = TextField()
    title = TextField()

    class Meta:
        database = db


Favourites.create_table()

