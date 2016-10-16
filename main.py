from app import app, db, manager, login_manager
from views import *
from models import *
from api_server import *

if __name__ == '__main__':
    #app.run()
    manager.run()
