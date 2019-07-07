from nvc.clis.base import Base
from signal import signal, SIGINT
from nvc.libs import utils
from nvc.parser import parse
from nvc.libs import ansible_lib, playbook_lib
import yaml
import os


class Playbook(Base):
    """
        usage:
        playbook configure [-f FILE]
        playbook start [-f FILE]
        playbook create [-p PACKAGE] [-a APPS]
        playbook remove [-f FILE]
        playbook ping [-u USERNAME]

        Run nvc playbook [command] [option]

        Options:
        -f file --file=FILE                                        File
        -p package --package=PACKAGE                               Package
        -a apps --apps=APPS                                        Application
        -i inventory --inventory=INVENTORY                         Inventory
        -u username --username=USERNAME                           Ping
        -h --help                                                  Print usage
    """
    def execute(self):
        app_dir = utils.app_cwd
        playbook_dir = parse.playbook_dir
        if self.args['create']:
            pkg = self.args['--package']
            apps = self.args['--apps']
            data_playbook = playbook_lib.playbook_create(pkg, apps)
            utils.yaml_writeln(data_playbook, app_dir+"/nvc.yml")
            exit()

        if self.args['configure']:
            path = None
            if self.args['--file']:
                try:
                    path = utils.yaml_read(self.args['--file'])
                except Exception as e:
                    utils.log_err(e)
            else:
                try:
                    path = utils.yaml_read("nvc.yml")
                except Exception as e:
                    utils.log_err(e)
                    exit()
            initial_data = parse.initial_parsed(path)
            try:
                parse.initial_tree(initial_data)
            except Exception as e:
                utils.log_err(e)
            except KeyboardInterrupt:
                utils.log_warn("Prosess Cancelling")
                utils.rm_dir(playbook_dir)
                utils.log_rep("Removing playbook cache")
            else:
                utils.log_rep("Playbook Configured")
            exit()

        if self.args['start']:
            path = None
            if self.args['--file']:
                nvc_file = self.args['--file']
            else:
                nvc_file = playbook_dir+"/nvc.yml"
            try:
                ansible_lib.playbook_file(playbook=nvc_file, 
                                          inventory=playbook_dir+"/inventory")
            except Exception as e:
                utils.log_err(e)
            except KeyboardInterrupt:
                utils.log_warn("Prosess Cancelling")
                print("User Canceling Progress Note: if there is an error \
                        access password, please delete the roles \
                        package in nvc.yml")
            else:
                utils.log_rep("Package Finished Setup")
            exit()

        if self.args['remove']:
            path = None
            if self.args['--file']:
                nvc_file = self.args['--file']
            else:
                nvc_file = "nvc.yml"
            obj_nvc = utils.yaml_read(nvc_file)
            for nvc_list in obj_nvc:
                for i in obj_nvc[nvc_list]['roles']:
                    if i != 'commons':
                        # call remove app builder
                        print("call remove app builder")
            exit()

        if self.args['ping']:
            if self.args['--username']:
                nvc_username = self.args['--username']
                os.system("groups "+nvc_username)
                 os.system("echo 'PONG | Agent Ready'")
            else:
                os.system("echo 'PONG | Agent Ready'")
            exit()