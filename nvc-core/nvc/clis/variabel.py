from nvc.clis.base import Base
from signal import signal, SIGINT
from nvc.libs import utils, vars_lib
import yaml
import os


class Variabel(Base):
    """
        usage:
        variabel show [-p PACKAGE]
        variabel show  [-p PACKAGE] [-a APPS]

        Run nvc variable [command] [option]

        Options:
        -p package --package=PACKAGE                              Set Distro Based | yum or apt
        -a apps --apps=APPS                                       set apps
        -h --help                                                 Print usage
    """
    def execute(self):
        if self.args['show']:
            os_name = self.args['--package']
            if self.args['--apps']:
                package = self.args['--apps']
                vars_lib.show_variabels(os_name, package)
                exit()
            vars_lib.show_variabels_all(os_name)
            exit()
