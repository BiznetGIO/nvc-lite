import os
import shutil
import requests
import json

def send_http(url, data, headers=None):
    send = requests.post(url, data=data, headers=headers)
    respons = send.json()
    return respons['data']

def get_http(url, param=None, header=None):
    json_data = None
    if param:
        json_data = param
    get_func = requests.get(url, params=json_data, headers=header)
    data = get_func.json()
    return data
