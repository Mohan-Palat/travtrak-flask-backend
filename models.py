# import * means import everything from peewee

from peewee import *
import datetime

# Connect to a Postgres database.
DATABASE = PostgresqlDatabase('travtrak', host='localhost', port=5432)

class Trek(Model):
    trip_name = CharField()
    date = CharField()
    image_url = CharField()
    designation = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Trek], safe=True)
    print("TABLES Created")