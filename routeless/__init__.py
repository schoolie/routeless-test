from flask import Flask
from config import config
from extensions import db, auth, admin, jwt, apimanager

# from OpenSSL import SSL

# context = SSL.Context(SSL.SSLv23_METHOD)
# context.use_privatekey_file('yourserver.key')
# context.use_certificate_file('yourserver.crt')
    
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    jwt.init_app(app)
    admin.init_app(app)

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

    return app

    
from routeless import views, models