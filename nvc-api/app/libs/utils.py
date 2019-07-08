import os
import shutil
import requests
import json
import coloredlogs
import logging
import yaml
import dill
from app import redis_store

def get_redis(token):
    redis_dill = redis_store.get(token)
    redis_data = dill.loads(redis_dill)
    return redis_data

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

def parse_url_env(parse, region):
    keystone_url_env = parse.split(",")
    keystone_url= ""
    for k in keystone_url_env:
        data_env_split_equal = k.split("=")
        dt_region = data_env_split_equal[0].replace('"','')
        data_env = data_env_split_equal[1].replace('"','')
        if dt_region == region:
            keystone_url = data_env
    return keystone_url


def parse_opestack_admin(parse, region):
    openstack_data = parse.split(",")
    op_data_fix = dict()
    for k in openstack_data:
        data_env_split_equal = k.split("=")
        dt_region = data_env_split_equal[0].replace('"','')
        admin_domain_data = data_env_split_equal[1].replace('"','')
        if dt_region == region:
            op_data_fix = {
                dt_region: admin_domain_data
            }
    return op_data_fix

def parse_nvc_images(region):
    nvc_images_env = os.environ.get("NVC_IMAGE_ID", os.getenv("NVC_IMAGE_ID"))
    nvc_images_data = nvc_images_env.split(",")
    op_data_fix = dict()
    for k in nvc_images_data:
        data_env_split_equal = k.split("=")
        dt_region = data_env_split_equal[0].replace('"','')
        admin_domain_data = data_env_split_equal[1].replace('"','')
        if dt_region == region:
            op_data_fix = {
                dt_region: admin_domain_data
            }
    return op_data_fix

def log_info(stdin):
    coloredlogs.install()
    logging.info(stdin)

def log_warn(stdin):
    coloredlogs.install()
    logging.warn(stdin)

def log_err(stdin):
    coloredlogs.install()
    logging.error(stdin)

def read_file(file):
    if os.path.isfile(file):
        return True
    else:
        return False

def create_file(file, path, value=None):
    if path:
        default_path = str(path)
    f = open(default_path+"/"+file, "a+")
    f.write(value)
    f.close()
    try:
        return read_file(default_path+"/"+file)
    except Exception as e:
        log_err(e)

def rm_dir(path):
    try:
        return shutil.rmtree(path)
    except Exception as e:
        log_err(e)

def copy(src, dest):
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        log_err(e)


def check_folder(path):
    try:
        return os.path.isdir(path)
    except Exception as e:
        log_err(e)

def copyfile(src, dest):
    try:
        shutil.copyfile(src, dest)
    except OSError as e:
        log_err(e)

def create_folder(path):
    try:
        return os.makedirs(path)
    except Exception as e:
        log_err(e)

def yaml_writeln(stream, path):
    with open(path, '+w') as outfile:
        try:
            yaml.dump(stream, outfile, default_flow_style=False)
        except yaml.YAMLError as e:
            log_err(e)
        else:
            return True

def exec_command_parse(parse):
    try:
        data_parse = parse.split("\n")
        for i in data_parse:
            if i == '':
                data_parse.pop()
    except Exception as e:
        log_err(e)
    else:
        return data_parse
            
    
