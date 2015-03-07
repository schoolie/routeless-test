from flask import request
from flask.ext.restless import APIManager
from flask_jwt import jwt_required
from werkzeug.security import generate_password_hash




def new_user(data=None, **kw):
    print data
    username = data['username']
    password = data['password']
    password_hash = generate_password_hash(password)
    data.pop('password', None)
    data['password_hash'] = password_hash
    
    return data
    
@jwt_required
def auth_func(*args, **kwargs):
    pass
        
class ResourceManager(APIManager):

    def init_api(self, app):
        self.init_app(app)
        
        with app.app_context():
            from ..models import User
            self.create_api(User, 
                            app=app, 
                            methods=['GET', 'POST', 'DELETE'], 
                            preprocessors={
                                           'GET_SINGLE': [auth_func],
                                           'GET_MANY': [auth_func],
                                           'POST': [new_user],
                                          },
                           )

# class AuthManager(JWT):

    # from ..models import User
    # @self.authentication_handler
    # def authenticate(username, password):
        # user = User.query.filter(User.username==username).first()
        # if user.verify_password(password):
            # return user

    # @self.user_handler
    # def load_user(payload):
        # user = User.query.filter(User.username==payload['username']).first()
        # return user