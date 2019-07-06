from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.v3 import client
from keystoneclient.v3 import users
from app.models import model


def generate_session(username, password,
                     auth_url, user_domain_name, project_id=None):
    try:
        auth = v3.Password(
            username=username,
            password=password,
            project_id=project_id,
            auth_url=auth_url,
            user_domain_name=user_domain_name,
            reauthenticate=True,
            include_catalog=True)
        sess = session.Session(auth=auth)
    except Exception as e:
        print(e)
        raise e
    else:
        return sess

def get_project_id(sess):
    keystone = client.Client(session=sess)
    project_list = [
        t.id for t in keystone.projects.list(user=sess.get_user_id())
    ]

    return project_list[0]

def check_user_id(user_id):
    try:
        data_user = model.get_by_id("tb_user", "user_id_openstack", user_id)[0]
    except Exception as e:
        return False
    else:
        return True
    
    
