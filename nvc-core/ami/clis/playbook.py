from ami.clis.base import Base
from signal import signal, SIGINT
from ami.libs import utils
from ami.parser import parse
from ami.libs import ansible_lib, playbook_lib
import yaml
import os


class Playbook(Base):
    """
        usage:
        playbook configure [-f FILE]
        playbook start [-f FILE]
        playbook create [-p PACKGE] [-a APPS]

        Run ami playbook [command] [option]

        Options:
        -f file --file=FILE                                        File
        -p package --package=PACKAGE                               Package
        -a apps --apps=APPS                                        Application
        -i inventory --inventory=INVENTORY                         Inventory
        -h --help                                                  Print usage
    """
    def execute(self):
        app_dir = utils.app_cwd
        playbook_dir = parse.playbook_dir
        if self.args['create']:
            pkg = self.args['--package']
            apps = self.args['--apps']
            data_playbook = playbook_lib.playbook_create(pkg, apps)
            utils.yaml_writeln(data_playbook, app_dir+"/ami.yml")
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
                    path = utils.yaml_read("ami.yml")
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
                ami_file = self.args['--file']
            else:
                ami_file = playbook_dir+"/ami.yml"
            try:
                ansible_lib.playbook_file(playbook=ami_file, 
                                          inventory=playbook_dir+"/inventory")
            except Exception as e:
                utils.log_err(e)
            except KeyboardInterrupt:
                utils.log_warn("Prosess Cancelling")
                print("User Canceling Progress Note: if there is an error \
                        access password, please delete the roles \
                        package in ami.yml")
            else:
                utils.log_rep("Package Finished Setup")
            exit()
