# import * means import everything from peewee

from flask import current_app as app
from peewee import *
import datetime
from flask_login import UserMixin
import jwt
import time
import datetime, os, urllib.parse

# Connect to a Postgres database.
# DATABASE = PostgresqlDatabase('travtrak', host='localhost', port=5432)

if "DATABASE_URL" in os.environ:
    urllib.parse.uses_netloc.append('postgres')
    url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
    DATABASE = PostgresqlDatabase(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port)
else:
    DATABASE = os.environ.get('DATABASE_URL') or PostgresqlDatabase('travtrak', host='localhost', port=5432)

class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()


    def generate_auth_token(self, expires_in=600):
        return jwt.encode(
            {'id': self.id, 'exp': time.time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

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