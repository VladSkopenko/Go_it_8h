from mongoengine import Document, StringField, BooleanField


class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    phone_number = StringField(required=True)
    message_sent = BooleanField(default=False)
    preferred_method = StringField(required=True)