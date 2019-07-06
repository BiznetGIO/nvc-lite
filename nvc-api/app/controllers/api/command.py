from flask_restful import Resource, request, reqparse
from app.helpers.rest import response
from app.middlewares import auth
from app.helpers import session
from app.libs import ssh_utils
from app.libs import neo
from app import root_dir



class PlaybookStart(Resource):
    @auth.login_required
    def post(self):
        token = request.headers['Access-Token']
        json_data = request.get_json(force=True)
        project_id = json_data['project_id']
        stack_id = json_data['stack_id']
        username = json_data['username']
        path_key = root_dir+"/static/keys/"+project_id+"/"+stack_id+"/vm.pem"
        vm_remotes = neo.get_nvc_by_stack_id(token, stack_id)
        public_ip_vm = vm_remotes[0]['ip'][1]
        try:
            ssh = ssh_utils.ssh_connect(public_ip_vm, username, path_key)
        except Exception as e:
            return response(401, message="Server Not Connected | "+str(e))
        else:
            # send jsonfile
            return response(200, data=json_data, message="REMOTE CONNECTED")


class PlaybookRemove(Resource):
    @auth.login_required
    def post(self):
        json_data = request.get_json(force=True)
        return response(200, data=json_data)


class PlaybookPing(Resource):
    @auth.login_required
    def post(self):
        token = request.headers['Access-Token']
        parser = reqparse.RequestParser()
        parser.add_argument('project_id', type=str, required=True)
        parser.add_argument('stack_id', type=str, required=True)
        parser.add_argument('username', type=str, required=True)
        args = parser.parse_args()

        project_id = args['project_id']
        stack_id = args['stack_id']
        username = args['username']

        path_key = root_dir+"/static/keys/"+project_id+"/"+stack_id+"/vm.pem"
        vm_remotes = neo.get_nvc_by_stack_id(token, stack_id)
        public_ip_vm = vm_remotes[0]['ip'][1]
        try:
            ssh_utils.ssh_connect(public_ip_vm, username, path_key)
        except Exception as e:
            return response(401, message="Server Not Connected | "+str(e))
        else:
            return response(200, message="Server Connected")