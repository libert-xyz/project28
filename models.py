from app import db
from passlib.apps import custom_app_context as pwd_context
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, name):
        self.name = name

    def  __repr__(self):
        return '<User: %r>' %self.name

    def password_hash(self,password_clean):
        self.password = pwd_context.encrypt(password_clean)

    def verify_password(self,password_clean):
        if pwd_context.verify(password_clean, self.password):
            return True
        else:
            return False

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
