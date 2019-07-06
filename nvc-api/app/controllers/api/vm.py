from app.helpers.rest import *
from neo.libs import vm
from neo.libs import orchestration as orch
from app.middlewares import auth
from app.helpers.session import *
from app.libs import neo
from flask_restful import Resource, request
import os


nvc_images = os.environ.get("NVC_IMAGE_ID", os.getenv("NVC_IMAGE_ID"))

class GetListVm(Resource):
    @auth.login_required
    def get(self):
        nvc_images_data = list()
        try:
            nvc_images_data = neo.get_nvc(request.headers['Access-Token'])
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=nvc_images_data)
        