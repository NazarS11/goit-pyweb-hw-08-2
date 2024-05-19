from mongoengine import Document, StringField, BooleanField, EmailField

class Contact(Document):
    full_name = StringField(required=True)
    email = EmailField(required=True)
    phone = StringField(required=True)
    notify_by = StringField(required=True)
    message_sent = BooleanField(default=False)
    additional_info = StringField()
