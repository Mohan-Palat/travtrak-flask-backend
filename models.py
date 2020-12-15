# import * means import everything from peewee

from peewee import *
import datetime
from flask_login import UserMixin

# Connect to a Postgres database.
DATABASE = PostgresqlDatabase('travtrak', host='localhost', port=5432)

class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE

class Trek(Model):
    trip_name = CharField()
    date = CharField()
    image_url = CharField()
    airline = CharField()
    confirmation_code = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Trek], safe=True)
    print("TABLES Created")