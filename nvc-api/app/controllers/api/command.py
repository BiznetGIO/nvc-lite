from flask_restful import Resource, request, reqparse
from app.helpers.rest import response
from app.middlewares import auth
from app.helpers import session
from app.libs import ssh_utils
from app.libs import neo, utils
from app import root_dir
from app.models import model



class PlaybookStart(Resource):
    @auth.login_required
    def post(self):
        result = []
        token = request.headers['Access-Token']
        json_data = request.get_json(force=True)
        project_id = json_data['project_id']
        stack_id = json_data['stack_id']
        username = json_data['username']
        app_stack = json_data['app_stack']
        path_stack = root_dir+"/static/keys/"+project_id+"/"+stack_id
        redis_data = utils.get_redis(token)
        nvc_images = utils.parse_nvc_images(redis_data['region'])
        nvc_images = nvc_images[redis_data['region']]
        vm_remotes = neo.get_nvc_by_stack_id(token, stack_id, nvc_images)
        public_ip_vm = vm_remotes[0]['ip'][1]
        try:
            ssh = ssh_utils.ssh_connect(public_ip_vm, username, path_stack+"/vm.pem")
            ssh.get_transport().is_active()
        except Exception as e:
            return response(401, message="Server Not Connected | "+str(e))
        else:
            if not utils.read_file(path_stack+"/nvc.yml"):
                utils.yaml_writeln(json_data['command'], path_stack+"/nvc.yml")
            else:
                utils.yaml_writeln(json_data['command'], path_stack+"/nvc.yml")
            try:
                ssh_utils.exec_command(ssh, "mkdir /tmp/"+app_stack)
                ftp = ssh.open_sftp()
                ssh_utils.sync_file(ftp, path_stack+"/nvc.yml","/tmp/"+app_stack+"/nvc.yml")
            except Exception as e:
                return response(401, message="Server Not Connected | "+str(e))
            try:
                # command_configure = "cd /tmp/"+app_stack+"; nvc playbook configure; sudo sh -c 'nvc playbook start' &"
                command_configure = "cd /tmp/"+app_stack+"; nvc playbook configure; nvc playbook start &"
                ssh_utils.exec_command_n_decode(ssh, command_configure)
            except Exception as e:
                return response(401, message="Server Not Connected | "+str(e))
            else:
                # redis_data = utils.get_redis(request.headers['Access-Token'])
                try:
                    user_data = model.get_by_id("tb_user", "project_id", project_id)[0]
                except Exception as e:
                    return response(401, message="User Not Found")
                
                insert_db = {
                    "id_user": user_data['id_user'],
                    "stack_id": stack_id,
                    "json_data": json_data['command'],
                    "action": "start"
                }
                try:
                    command_id = model.insert("tb_command", insert_db)
                except Exception as e:
                    return response(401, message=str(e))

                result = {
                    "stack_id": stack_id,
                    "username": username,
                    "command_id": str(command_id)
                }

            ssh.close()
            return response(200, data=result, message="Remote Success")


class PlaybookRemove(Resource):
    @auth.login_required
    def post(self):
        token = request.headers['Access-Token']
        json_data = request.get_json(force=True)
        command_id = json_data['command_id']
        username = json_data['username']
        try:
            data_command = model.get_by_id("tb_command", "id_command", command_id)[0]
        except Exception as e:
            return response(401, message="Command Data Not Found | "+str(e))
        try:
            data_user = model.get_by_id("tb_user", "id_user", str(data_command['id_user']))[0]
        except Exception as e:
            return response(401, message="User Not Found | "+str(e))
        
        stack_id = str(data_command['stack_id'])
        project_id = str(data_user['project_id'])
        path_stack = root_dir+"/static/keys/"+project_id+"/"+stack_id
        app_stack = json_data['app_stack']
        redis_data = utils.get_redis(token)
        nvc_images = utils.parse_nvc_images(redis_data['region'])
        nvc_images = nvc_images[redis_data['region']]
        vm_remotes = neo.get_nvc_by_stack_id(token, stack_id, nvc_images)
        public_ip_vm = vm_remotes[0]['ip'][1]

        try:
            ssh = ssh_utils.ssh_connect(public_ip_vm, username, path_stack+"/vm.pem")
            ssh.get_transport().is_active()
        except Exception as e:
            return response(401, message="Server Not Connected | "+str(e))
        else:
            if not utils.check_folder(path_stack+"/uninstall"):
                utils.create_folder(path_stack+"/uninstall")

            if not utils.read_file(path_stack+"/uninstall/nvc.yml"):
                utils.yaml_writeln(json_data['command'], path_stack+"/uninstall/nvc.yml")
            else:
                utils.yaml_writeln(json_data['command'], path_stack+"/uninstall/nvc.yml")

            try:
                ssh_utils.exec_command(ssh, "mkdir /tmp/"+app_stack+"/uninstall")
                ftp = ssh.open_sftp()
                ssh_utils.sync_file(ftp, path_stack+"/uninstall/nvc.yml","/tmp/"+app_stack+"/uninstall/nvc.yml")
            except Exception as e:
                return response(401, message="Server Not Connected | "+str(e))
            try:
                # command_configure = "cd /tmp/"+app_stack+"; nvc playbook configure; sudo sh -c 'nvc playbook start' &"
                command_configure = "cd /tmp/"+app_stack+"/uninstall; nvc playbook configure; nvc playbook start &"
                ssh_utils.exec_command_n_decode(ssh, command_configure)
            except Exception as e:
                return response(401, message="Server Not Connected | "+str(e))
            else:
                # redis_data = utils.get_redis(request.headers['Access-Token'])
                try:
                    user_data = model.get_by_id("tb_user", "project_id", project_id)[0]
                except Exception as e:
                    return response(401, message="User Not Found")
                
                insert_db = {
                    "id_user": user_data['id_user'],
                    "stack_id": stack_id,
                    "json_data": json_data['command'],
                    "action": "start"
                }
                try:
                    command_id = model.insert("tb_command", insert_db)
                except Exception as e:
                    return response(401, message=str(e))

                result = {
                    "stack_id": stack_id,
                    "username": username,
                    "command_id": str(command_id)
                }

            ssh.close()
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
        redis_data = utils.get_redis(request.headers['Access-Token'])
        nvc_images = utils.parse_nvc_images(redis_data['region'])
        nvc_images = nvc_images[redis_data['region']]
        path_key = root_dir+"/static/keys/"+project_id+"/"+stack_id+"/vm.pem"
        vm_remotes = neo.get_nvc_by_stack_id(token, stack_id, nvc_images)
        public_ip_vm = vm_remotes[0]['ip'][1]
        try:
            ssh = ssh_utils.ssh_connect(public_ip_vm, username, path_key)
        except Exception as e:
            return response(401, message="Server Not Connected | "+str(e))
        else:
            ping_status = ssh_utils.exec_command(ssh, "nvc playbook ping -u "+username)
            ssh.close() 
            return response(200, data= str(ping_status), message="Server Connected")