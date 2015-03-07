from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth
from flask_jwt import JWT, jwt_required
from flask_debugtoolbar import DebugToolbarExtension

from api_1_0 import ResourceManager
# from api_1_0 import AuthManager
from config import config
from core import db

# from OpenSSL import SSL

# context = SSL.Context(SSL.SSLv23_METHOD)
# context.use_privatekey_file('yourserver.key')
# context.use_certificate_file('yourserver.crt')
           
@jwt_required
def auth_func(*args, **kwargs):
    pass
    
apimanager = ResourceManager(flask_sqlalchemy_db=db,
                             preprocessors=dict(GET_MANY=[auth_func])
                            )
jwt = JWT()
auth = HTTPBasicAuth()
toolbar = DebugToolbarExtension()

    
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    jwt.init_app(app)
    toolbar.init_app(app)
    print toolbar
    
    apimanager.init_api(app)
        
    from views import views
    app.register_blueprint(views)

    from models import User
    @jwt.authentication_handler
    def authenticate(username, password):
        user = User.query.filter(User.username==username).first()
        if user.verify_password(password):
            return user

    @jwt.user_handler
    def load_user(payload):
        user = User.query.filter(User.username==payload['username']).first()
        return user
        
    print app.url_map
    
    return app

    
from routeless import views, models