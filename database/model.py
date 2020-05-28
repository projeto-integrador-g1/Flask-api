from .db import db

class User(db.Document):
    user_name = db.StringField(required=True)
    user_email = db.StringField(required=True)
    user_imgs = db.StringField(required=False)

class GeoInfo(db.Document):
    user_id = db.StringField(required=True)
    geo_coord = db.StringField(required=True)