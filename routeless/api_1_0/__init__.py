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


class ResourceManager(APIManager):


    # def auth_func(self):
    #     print 'testing preprocessor...'
    #     assert True==False

    def init_api(self, app):
        self.init_app(app)

        # self.preprocessors={'GET':[self.auth_func]}

        with app.app_context():
            from ..models import User, Course, Event, CheckPoint, CheckPointLog, \
                Route, RoutePoint, LogPoint

            self.create_api( User, app=app,
                             methods=['GET', 'POST', 'DELETE'] )

            self.create_api( Course, app=app,
                             methods=['GET', 'POST', 'DELETE'] )

            self.create_api( Course, app=app,
                             methods=['GET', 'POST', 'DELETE'] )
            self.create_api( Event, app=app,
                             methods=['GET', 'POST', 'DELETE'] )
            self.create_api( CheckPoint, app=app,
                             methods=['GET', 'POST', 'DELETE'] )
            self.create_api( CheckPointLog, app=app,
                             methods=['GET', 'POST', 'DELETE'] )
            self.create_api( Route, app=app,
                             methods=['GET', 'POST', 'DELETE'] )
            self.create_api( RoutePoint, app=app,
                             methods=['GET', 'POST', 'DELETE'] )
            self.create_api( LogPoint, app=app,
                             methods=['GET', 'POST', 'DELETE'] )

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