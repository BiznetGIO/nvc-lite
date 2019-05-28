from ami.clis.base import Base
from signal import signal, SIGINT
from ami.libs import utils
import yaml
import os


class Server(Base):
    """
        usage:
        server cpu
        server memory
        server disk

        Run ami server [command] [option]

        Options:
        -h --help                                                 Print usage
    """
    def execute(self):
        if self.args['cpu']:
            cpu_info = utils.get_cpu_info()
            for i in cpu_info:
                utils.log_rep(i+" : "+str(cpu_info[i]))
            exit()

        if self.args['memory']:
            cpu_info = utils.get_memory_info()
            for i in cpu_info:
                utils.log_rep("#### "+i+" #####")
                for a in cpu_info[i]:
                    utils.log_rep(a+" : "+str(cpu_info[i][a]))
            exit()
        
        if self.args['disk']:
            cpu_info = utils.get_disk_info()
            for i in cpu_info:
                utils.log_rep(i+" : "+str(cpu_info[i]))
            exit()