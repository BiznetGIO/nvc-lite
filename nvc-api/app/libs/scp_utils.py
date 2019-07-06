import paramiko
import os

CURR_DIR = os.getcwd()

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())


def ssh_connect(host, username, key_filename=None):
    try:
        ssh.connect(host, username=username, key_filename=key_filename)
    except Exception as e:
        print(e)
        raise e
    else:
        return ssh