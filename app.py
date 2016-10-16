from flask import Flask,g
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager

#http://charlesleifer.com/blog/structuring-flask-apps-a-how-to-for-those-coming-from-django/

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

db = SQLAlchemy(app)
migrate = Migrate(app,db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"



from models import User
@login_manager.user_loader
def load_users(user_id):
    return User.query.filter_by(id=int(user_id)).first()
