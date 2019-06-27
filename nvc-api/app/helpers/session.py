from app import redis_store
import dill

def get_session(access_token):
    stored_data = redis_store.get(access_token)
    if not stored_data:
        return None
    data = dill.loads(stored_data)
    return data['session']

