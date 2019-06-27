from neo.libs import utils, vm, network
from glanceclient import Client as image_client

def get_image_client(session):
    img = image_client('2', session=session)
    return img


def get_list(session):
    img = get_image_client(session)
    img_list = list()
    try:
        img_list = img.images.list()
    except Exception:
        return None
    return img_list


class neoApi():
    def neo_get_stack():
        list_stack = utils.get_index(utils.repodata())
        return list_stack

    def neo_get_project(templates):
        list_project = utils.get_index(utils.repodata()[templates])
        return list_project

    def neo_get_image(session):
        images = get_list(session)
        data = []
        for i in images:
            obj = {
                'id': i['id'],
                'name': i['name'],
                'status': i['status']
            }
            data.append(obj)
        return data

    def neo_get_flavour(session):
        flavor = [{attr:value for attr,value in flav.__dict__.items()} for flav in vm.get_flavor(session)]
        data = []
        for i in flavor:
            obj = {
                'id': i['id'],
                'name': i['name'],
                'ram': i['ram'],
                'cpu': i['vcpus'],
                'disk': i['disk']
            }
            data.append(obj)
        return data

    def neo_get_key(session):
        list_key = vm.get_keypairs(session)
        return list_key

    def neo_get_network(session):
        return [
            net['name'] for net in network.get_list(session)
            if net['name'] != 'Public_Network'
        ]
