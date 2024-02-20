from mongoengine import Document, connect, StringField, DateField, ListField, ReferenceField
from password import user, password

connect(db="web_19", host=f"mongodb+srv://{user}:{password}@goitlearn.x6ks5fo.mongodb.net/?retryWrites=true&w=majority")


class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    author = ReferenceField(Author)
    quote = StringField(required=True)
    tags = ListField(StringField())

