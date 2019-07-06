from app.helpers.rest import *
from neo.libs import vm
from neo.libs import orchestration as orch
from app.middlewares import auth
from app.helpers.session import *
from flask_restful import Resource, request
import os


nvc_images = os.environ.get("NVC_IMAGE_ID", os.getenv("NVC_IMAGE_ID"))

class GetListVm(Resource):
    @auth.login_required
    def get(self):
        obj_data = []
        try:
            session_data = get_session(request.headers['Access-Token'])
            list_vm = vm.get_list(session=session_data)
        except Exception as e:
            return response(401, data=str(e))
        else:
            for i in list_vm:
                power_state = getattr(i, 'OS-EXT-STS:power_state')
                for network_name, network in i.networks.items():
                    data = {
                        'id': i.id,
                        'name': i.name,
                        'status': i.status,
                        'image': i.image,
                        'network': network_name,
                        'ip': network,
                        'key_name': i.key_name,
                        'flavor': i.flavor,
                        'power_state': power_state

                    }
                    obj_data.append(data)
        obj_vm = list()
        obj_stack = list()
        stack = orch.get_list(session=session_data)
        for stack_list in stack:
            data_stack = {
                'id': stack_list[0],
                'name': stack_list[1],
                'status': stack_list[2],
                'created': stack_list[3],
                'update': stack_list[4]
            }
            obj_stack.append(data_stack)
        
        for vm_list in obj_data:
            if vm_list['image']['id'] == nvc_images:
                for stack_row in obj_stack:
                    if vm_list['name'] == stack_row['name']:
                        obj_vm.append({
                            "id": vm_list['id'],
                            "stack_id": stack_row['id'],
                            "stack_name": stack_row['name'],
                            "name": vm_list['name'],
                            "status": vm_list['status'],
                            "image": nvc_images,
                            "network": vm_list['network'],
                            "ip": vm_list['ip'],
                            "key_name": vm_list['key_name'],
                            "power_state": vm_list['power_state'],
                            "stack_status": stack_row['status']
                        })
        
        return response(200, data=obj_vm)
        