import yaml
import os
import subprocess
import coloredlogs
import logging
import psutil
import shutil
import hashlib
import uuid
import fileinput
import requests
from nvc import __appname__
from dotenv import load_dotenv
import git


app_root = os.path.dirname(os.path.abspath(__file__))
app_home = os.path.expanduser("~")
app_cwd = os.getcwd()


def question(word):
    answer = False
    while answer not in ["y", "n"]:
        answer = input("{} [y/n]? ".format(word)).lower().strip()

    if answer == "y":
        answer = True
    else:
        answer = False
    return answer


def log_rep(stdin):
    coloredlogs.install()
    logging.info(stdin)


def log_warn(stdin):
    coloredlogs.install()
    logging.warn(stdin)


def log_err(stdin):
    coloredlogs.install()
    logging.error(stdin)


def template_git(url, dir):
    try:
        chk_repo = os.path.isdir(dir)
        if chk_repo:
            shutil.rmtree(dir)
        git.Repo.clone_from(url, dir)
        return True
    except Exception as e:
        log_err(e)
        return False


def yaml_writeln(stream, path):
    with open(path, '+a') as outfile:
        try:
            yaml.dump(stream, outfile, default_flow_style=False)
        except yaml.YAMLError as exc:
            print(exc)
        else:
            return True


def yaml_read(path):
    with open(path, 'r') as outfile:
        try:
            data = yaml.load(outfile, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            print(exc)
        else:
            return data


def nvc_config():
    return yaml_read(app_root+"/templates/config.yml")


def nvc_config_roles(pkg):
    return yaml_read(app_root+"/templates/"+pkg+"/roles/item.yml")


def nvc_config_vars(pkg):
    # return yaml_read(app_root+"/templates/"+pkg+"/vars/item.yml")
    return yaml_read(app_root+"/templates/"+pkg+"/vars/config.yml")


def get_cpu_info():
    cpu = psutil.cpu_times()
    count_cpu = psutil.cpu_count()
    cpu_data = {
        "user": cpu[0],
        "nice": cpu[1],
        "system": cpu[2],
        "idle": cpu[3],
        "count": count_cpu,
    }
    return cpu_data


def get_memory_info():
    memory = psutil.virtual_memory()
    swap = psutil.virtual_memory()
    mem_data = {
        "physmem": {
            "total": memory[0],
            "available": memory[1],
            "percent": memory[2],
            "used": memory[3],
            "free": memory[4]
        },
        "swap": {
          "total": swap[0],
            "available": swap[1],
            "percent": swap[2],
            "used": swap[3],
            "free": swap[4]
        }
    }
    return mem_data


def get_disk_info():
    disk = psutil.disk_usage('/')
    disk_data = {
        "total": disk[0],
        "used": disk[1],
        "free": disk[2],
        "percent": disk[3]
    }
    return disk_data


def create_file(file, path, value=None):
    if path:
        default_path = str(path)
    f = open(default_path+"/"+file, "a+")
    f.write(value)
    f.close()

    try:
        return read_file(default_path+"/"+file)
    except Exception as e:
        print(e)


def copy(src, dest):
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        print('Directory not copied. Error: %s' % e)


def check_folder(path):
    return os.path.isdir(path)


def copyfile(src, dest):
    try:
        shutil.copyfile(src, dest)
    except OSError as e:
        print('Directory not copied. Error: %s' % e)


def create_folder(path):
    return os.makedirs(path)


def read_file(file):
    if os.path.isfile(file):
        return True
    else:
        return False


def rm_dir(path):
    return shutil.rmtree(path)


def token_hash(string):
    random_string = uuid.uuid4()
    raw_token = '{}{}'.format(random_string, string)
    access_token = hashlib.sha256(raw_token.encode(
        'utf-8')).hexdigest()
    return access_token


def get_http(url, headers=None):
    send = requests.get(url, headers=headers)
    respons = send.json()
    return respons


def send_http(url, data = None, headers=None):
    send = requests.post(url, json=data, headers=headers)
    respons = send.json()
    return respons