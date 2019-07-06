from flask_restful import Resource, reqparse, request
from app.helpers.rest import *
from app.middlewares import auth
from app.helpers.session import *
from app.libs.neo import neoApi
from neo.libs import orchestration as orch
from app import root_dir, redis_store
from app.libs import utils
import dill, os


class GetPemKey(Resource):
    @auth.login_required
    def get(self, stack_id):
        private_key = None
        static_dir = root_dir+"/static"
        redis_dill = redis_store.get(request.headers['Access-Token'])
        redis_data = dill.loads(redis_dill)
        project_id = redis_data['project_id']
        try:
            private_key = orch.get_pkey_from_stack(stack_id, 
                session=get_session(request.headers['Access-Token']))
        except Exception as e:
            return response(401, message=str(e))
        else:
            try:
                path_keys = static_dir+"/keys/"+project_id+"/"+stack_id
                if not utils.check_folder(path_keys):
                    utils.create_folder(path_keys)
                    utils.create_file("vm.pem",path_keys, private_key)
                else:
                    utils.create_file("vm.pem",path_keys, private_key)
                os.chmod(path_keys+"/vm.pem", 0o600)
            except Exception as e:
                return response(401, message="Key Not Generate")
            else:
                return response(200, message="Generate key success")