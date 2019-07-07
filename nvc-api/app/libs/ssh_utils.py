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
    return result

def exec_command_n_decode(ssh_object, command):
    _,stdout,_ = ssh_object.exec_command(str(command))
    return stdout

def sync_file(ftp_client, path_file, path_remote):
    # Seharusnya ada return calback status
    try:
        ftp_client.put(path_file, path_remote)
    except Exception as e:
        utils.log_err(e)
    else:
        ftp_client.close()


def line_buffered(f):
    line_buf = []
    while not f.channel.exit_status_ready():
        data = f.read().decode('utf-8')
        data = data.split("\n")
        for i in data:
            if i != '':
                line_buf.append(i)
    return line_buf