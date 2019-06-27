import os
import shutil
import requests
import json
import coloredlogs
import logging

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

def log_info(stdin):
    coloredlogs.install()
    logging.info(stdin)


def log_warn(stdin):
    coloredlogs.install()
    logging.warn(stdin)


def log_err(stdin):
    coloredlogs.install()
    logging.error(stdin)

