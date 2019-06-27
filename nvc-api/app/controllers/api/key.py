from flask_restful import Resource, reqparse, request
from app.helpers.rest import *
from app.middlewares import auth
from app.helpers.session import *
from app.libs.neo import neoApi
from neo.libs import orchestration as orch
from app import root_dir


class GetPemKey(Resource):
    @auth.login_required
    def get(self, stack_id):
        private_key = None
        static_dir = root_dir+"/static"
        try:
            private_key = orch.get_pkey_from_stack(stack_id, session=get_session(request.headers['Access-Token']))
        except Exception as e:
            return response(401, message=str(e))
        else:
            print(root_dir)
            print(private_key)
            return response(200, message="Generate key success")