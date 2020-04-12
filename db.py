from peewee import *

db = SqliteDatabase('relay.db')
# db = PostgresqlDatabase('my_app', user='postgres', password='secret', host='10.1.0.9', port=5432)
class Participant(Model):
    line_mid = CharField(unique=True)
    email_id = CharField()
    name = TextField()

    class Meta:
        database = db

class ChatBubble(Model):
    timestamp = IntegerField()
    user_id = CharField()
    message = TextField()

    class Meta:
        database = db

db.connect()
db.create_tables([Participant, ChatBubble])