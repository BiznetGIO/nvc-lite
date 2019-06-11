from functools import wraps
from app.helpers.rest import *
from app import redis_store
from neo.libs import login
from flask import request
import hashlib



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'Access-Token' not in request.headers:
            return response(400, message=" Invalid access token ")
        else:
            access_token = request.headers['Access-Token']
            stored_data = redis_store.get('{}'.format(access_token))
            if not stored_data:
                return response(400, message=" Invalid access token ")

        return f(*args, **kwargs)
    return decorated_function