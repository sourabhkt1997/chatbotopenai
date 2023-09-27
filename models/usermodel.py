from mongoengine import Document, StringField, DateTimeField

class User(Document):
    username=StringField(required=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
   
