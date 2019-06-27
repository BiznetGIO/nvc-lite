from flask_restful import Resource, reqparse
from flask import request, jsonify
from app.helpers.rest import *
from app.helpers.session import *
from app import redis_store
from neo.libs import login
from keystoneauth1 import session
from keystoneauth1.identity import v3
from app.middlewares import auth
from app.libs import utils
import os
import dill
import hashlib
import uuid
import arrow


class LoginNow(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('region', type=str, required=True)
        args = parser.parse_args()

        username = args['username']
        password = args['password']
        region = args['region']
        keystone_url_env = os.environ.get("KEYSTONE_URL","")
        openstack_domain = os.environ.get("KEYSTONE_DOMAIN", "neo.id")
        keystone_url = utils.parse_url_env(keystone_url_env, region)
        try:
            random_string = uuid.uuid4()
            raw_token = '{}{}'.format(random_string, username)

            access_token = hashlib.sha256(raw_token.encode(
                'utf-8')).hexdigest()
            now = arrow.now()
            project_id = login.get_project_id(username, password, keystone_url, openstack_domain)
            sess = login.generate_session(
                auth_url=keystone_url,
                username=username,
                password=password,
                user_domain_name= openstack_domain,
                project_id=project_id)
            user_id = sess.get_user_id()
            stored_data = {
                'user_id':user_id,
                'timestamp': now,
                'session': sess,
                'project_id': project_id
            }
            dill_object = dill.dumps(stored_data)
            redis_store.set(access_token, dill_object)
            redis_store.expire(access_token, 3600)

        except Exception as e:
            utils.log_err(e)
            return response(401, message=str(e))
        else:
            return response(200, message="Login Success", data={
                    'access_token':access_token,
                    "region": region
                })


class LogOutNow(Resource):
    @auth.login_required
    def get(self):
        try:
            # login.do_logout()
            redis_store.delete(request.headers['Access-Token'])
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, message="Logout Success")
