from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.admin import Admin
from flask_jwt import JWT, jwt_required
from api_1_0 import ResourceManager

db = SQLAlchemy()
auth = HTTPBasicAuth()
admin = Admin()
jwt = JWT()


# @jwt_required
def auth_func(*args, **kwargs):
    print 'testing preprocessor'

    raise Exception

apimanager = ResourceManager(flask_sqlalchemy_db=db,
                             preprocessors=dict(GET_SINGLE=[auth_func])
                            )