from flask import Blueprint
from flask_restful import Api
from .auth import *
from .key import *
from .vm import *
from .command import *
from .health import *


api_blueprint = Blueprint("api", __name__, url_prefix='/api')
api = Api(api_blueprint)
api.add_resource(HealthCheck, "/health")
api.add_resource(LoginNow, "/login")
api.add_resource(GetPemKey, "/key/<stack_id>")

api.add_resource(GetListVm, "/nvc/list")

api.add_resource(PlaybookStart, "/playbook/start")
api.add_resource(PlaybookRemove, "/playbook/remove")
api.add_resource(PlaybookPing, "/playbook/ping")



