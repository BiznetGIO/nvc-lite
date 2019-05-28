from nvc.libs import utils


def show_variabels_all(packet_manager):
    vars_config = utils.nvc_config_vars(packet_manager)['vars']['package']
    for i in vars_config:
        print("\033[1;31;40m package: "+i)
        for a in vars_config[i]['parameters']:
            try:
                default = vars_config[i]['parameters'][a]['default']
            except Exception:
                default = "None"
            print("\033[1;33;40m  variabel: "+a)
            print("\033[1;32;40m  default: "+str(default))
        print("\n")


def show_variabels(packet_manager, package):
    vars_config = utils.nvc_config_vars(
        packet_manager)['vars']['package'][package]['parameters']
    print("\033[1;31;40m package: "+package)
    for i in vars_config:
        try:
            default = vars_config[i]['default']
        except Exception:
            default = "None"
        print("\033[1;33;40m  variabel: "+i)
        print("\033[1;32;40m  default: "+str(default))
        print("\n")