import paramiko
import os
import string
from app.libs import utils

CURR_DIR = os.getcwd()

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())


def ssh_connect(host, username, key_filename=None):
    try:
        ssh.connect(host, username=username, key_filename=key_filename)
    except Exception as e:
        utils.log_err(e)
        raise e
    else:
        return ssh

def exec_command(ssh_object, command):
    _,stdout,_ = ssh_object.exec_command(str(command))
    result = stdout.read().decode("utf8")
    ssh_object.close()
    return result


def sync_file(ssh_object,path_file, path_remote):
    ftp_client= ssh_object.open_sftp()
    send = ftp_client.put(path_file, path_remote)
    send_progress = send.read()
    L = str.split(send_progress)
    for i in L:
        if str.find(i, '%')>-1:
            print(i)
    ftp_client.close()