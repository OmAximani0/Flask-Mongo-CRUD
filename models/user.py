from db.database import db

class User(db.Document):
    name = db.StringField(required=True)
    email = db.EmailField(required=True, uniq=True)
    password = db.StringField(password=True, required=True)