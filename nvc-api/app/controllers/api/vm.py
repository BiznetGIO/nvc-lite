from app.helpers.rest import *
from neo.libs import vm
from neo.libs import orchestration as orch
from app.middlewares import auth
from app.helpers.session import *
from app.libs import neo, utils
from flask_restful import Resource, request


class GetListVm(Resource):
    @auth.login_required
    def get(self):
        nvc_images_data = list()
        redis_data = utils.get_redis(request.headers['Access-Token'])
        nvc_images = utils.parse_nvc_images(redis_data['region'])
        nvc_images = nvc_images[redis_data['region']]
        try:
            nvc_images_data = neo.get_nvc(request.headers['Access-Token'],
                                            nvc_images)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=nvc_images_data)
        