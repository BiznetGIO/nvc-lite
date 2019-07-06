from nvc.libs import utils

app_dir = utils.app_cwd


def playbook_create_json(json, app_name):
    nvc_file = app_dir+"/"+app_name+"/nvc.yml"
    try:
        utils.yaml_writeln(json, nvc_file)
    except Exception as e:
        utils.log_err(e)
    else:
        return True


def playbook_create(pkg, apps=None):
    finish_data = list()
    item_rules = utils.nvc_config_roles(pkg)[apps]['rules']
    vars_item = utils.nvc_config_vars(pkg)['vars']['package']
    config_items = utils.nvc_config()['config'][pkg]['parameters']      
    data_package = dict()
    for i in config_items:
        try:
            default = config_items[i]['default']
        except Exception:
            default = None
    
        if default:
            a = None
            try:
                a = utils.question("Set Default Value "+i+" : ")
            except KeyboardInterrupt:
                utils.log_warn("User cancelation")
                exit()
            if not a:
                default = input("Insert Your Value : ")
        else:
            if i == 'roles':
                default = item_rules
                data_package[i] = default
            elif i == 'vars':
                utils.log_warn("Insert Variabel "+i)
                data_items_vars = dict()
                for ir in item_rules:
                    data_vars = dict()
                    for vi in vars_item[ir]['parameters']:
                        try:
                            default_vi = vars_item[ir]
                            default_vi = default_vi['parameters'][vi]['default']
                        except Exception:
                            default_vi = None
                        if not default_vi:
                            data_vars[vi] = input("Variabel "+ir+" | "+vi+" : ")
                    if data_vars != {}:
                        data_items_vars[ir] = data_vars
                data_package[i] = data_items_vars
            else:
                data_package[i] = default
        # data_package[i] = default
    finish_data.append(data_package)
    print(finish_data)
    return finish_data


def uninstalling_package(data):
    pass


def playbook_remove(path):
    try:
        utils.rm_dir(path)
    except Exception as e:
        utils.log_err(e)
    else:
        return True