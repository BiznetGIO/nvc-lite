from nvc.clis.base import Base
from signal import signal, SIGINT
from nvc.libs import utils
from nvc.parser import parse
from nvc.libs import playbook_lib
import yaml
import os


class Rm(Base):
    """
        usage:
        rm playbook [-f FILE]
        rm roles [-r ROLES]

        Run nvc rm [command] [option]

        Options:
        -f file --file=FILE                                       File
        -r roles --roles=ROLES                                    Rm Roles
        -h --help                                                 Print usage
    """
    def execute(self):
        app_dir = utils.app_cwd
        playbook_dir = parse.playbook_dir
        if self.args['playbook']:
            # check args file
            if self.args['--file']:
                file = self.args['--file']
                app_dir = os.path.dirname(file)
                if app_dir == "":
                    app_dir = utils.app_cwd
                else:
                    app_dir = app_dir
            else:
                app_dir = utils.app_cwd
            try:
                playbook_lib.playbook_remove(app_dir+"/playbook")
            except Exception as e:
                utils.log_err(e)
                exit()
            except KeyboardInterrupt:
                utils.log_warn("User cancelation this process")
                exit()
            else:
                utils.log_rep("Delete Playbook Successfully")
            exit()
        
        if self.args['roles']:
            roles_item = self.args['--roles']
            if not roles_item:
                roles_item = input("Insert Name Roles: ")
            try:
                nvc_file = utils.yaml_read(app_dir+"/nvc.yml")
            except Exception as e:
                utils.log_err(e)
                exit()
            a = 0
            for i in nvc_file['yum']['roles']:
                if roles_item == i:
                    nvc_file['yum']['roles'].pop(a)
                    nvc_file['yum']['vars'].pop(i)
                a = a+1
            try:
                if utils.read_file(app_dir+"/nvc.yml"):
                    os.remove(app_dir+"/nvc.yml")
                utils.yaml_writeln(nvc_file, app_dir+"/nvc.yml")
            except Exception as e:
                utils.log_err(e)
                exit()
            else:
                utils.log_rep("Roles Deleted Successfully")
            exit()
