from flask_restful import Resource, request, reqparse
from app.helpers.rest import response
from app.middlewares import auth
from app.helpers import session
from app.libs import ssh_utils
from app.libs import neo, utils
from app import root_dir
from app.models import model



class ReadlogPlaybook(Resource):
    @auth.login_required
    def get(self, stack_id, username):
        token = request.headers['Access-Token']
        redis_data = utils.get_redis(token)
        nvc_images = utils.parse_nvc_images(redis_data['region'])
        nvc_images = nvc_images[redis_data['region']]
        vm_remotes = neo.get_nvc_by_stack_id(token, stack_id, nvc_images)
        public_ip_vm = vm_remotes[0]['ip'][1]
        path_stack = root_dir+"/static/keys/"+redis_data['project_id']+"/"+stack_id
        try:
            ssh = ssh_utils.ssh_connect(public_ip_vm, username, path_stack+"/vm.pem")
            ssh.get_transport().is_active()
        except Exception as e:
            return response(401, message="Server Not Connected | "+str(e))
        else:
            res = ssh_utils.exec_command_n_decode(ssh, "cat /var/log/"+stack_id+".log")
            # res = ssh_utils.exec_command_n_decode(ssh, "cat /var/log/nvc.log")
            result = ssh_utils.line_buffered(res)
            return response(200, data=result)