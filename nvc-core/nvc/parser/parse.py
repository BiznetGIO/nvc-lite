from nvc.libs import utils

playbook_dir = utils.app_cwd+"/playbook"

# def get_repo():
#     return  utils.nvc_repo()

# def initial_parse(nvc_json):
#     repo = get_repo()
#     github_url = None
#     initial_data = dict()
#     for i in nvc_json:
#         data = dict()
#         for a in repo:
#             github_url = repo[a][i]['url']
#             parameter = repo[a][i]['parameters']
#             for params in parameter:
#                 params_value = None
#                 try:
#                     params_value = nvc_json[i][params]
#                 except Exception:
#                     params_value = None
#                 if params_value is None:
#                     params_value = parameter[params]['default']
#                 data[params] = params_value
#         initial_data={
#             "github": github_url,
#             "playbook": data
#         }
#     return initial_data


def initial_parsed(nvc_json):
    repo = utils.nvc_config()
    github_url = None
    initial_data = dict()
    packager = None
    for i in nvc_json:
        packager = i
        data = dict()
        for a in repo:
            github_url = repo[a][i]['url']
            parameter = repo[a][i]['parameters']
            for params in parameter:
                params_value = None
                try:
                    params_value = nvc_json[i][params]
                except Exception:
                    params_value = None
                if params_value is None:
                    try:
                        params_value = parameter[params]['default']
                    except Exception:
                        params_value = None
                data[params] = params_value
        initial_data = {
            "github": github_url,
            "playbook": data,
            "pkg": packager
        }
    return initial_data


def initial_tree(initial_data):
    github_url = initial_data['github']
    playbook = initial_data['playbook']
    packager = initial_data['pkg']
    roles_item = utils.nvc_config_roles(packager)
    checks = utils.template_git(github_url, playbook_dir)
    if not checks:
        utils.log_err("Repo Not Cloning")
        exit()
    else:
        utils.rm_dir(playbook_dir+"/nvc-core")
        utils.rm_dir(playbook_dir+"/nvc-heat")
        utils.copy(playbook_dir+"/nvc-package/roles", playbook_dir+"/roles")
        utils.copy(playbook_dir+"/nvc-package/vars", playbook_dir+"/vars")
        utils.rm_dir(playbook_dir+"/nvc-package")
    
    host = "[nvc_lite]\nlocalhost ansible_connection=local"
    utils.create_file("inventory", playbook_dir, host)
    checks = utils.yaml_writeln([playbook],playbook_dir+"/nvc.yml")
    remove_package_dir = utils.os.listdir(playbook_dir+"/roles")
    if not checks:
        utils.log_err("Playbook Not Created")
        exit()
    for i in playbook['roles']:
        handlers = None
        folder_path = playbook_dir+"/roles/"+i
        folder_task = folder_path+"/tasks"
        if not utils.check_folder(folder_path):
            utils.create_folder(folder_path)
        if i in remove_package_dir:
            index = remove_package_dir.index(i)
            remove_package_dir.pop(index)   
        handlers = roles_item[i]['handlers']
        tasks = roles_item[i]['tasks']
        if handlers:
            folder_handlers = folder_path+"/handlers"
            utils.create_folder(folder_handlers)
            utils.yaml_writeln(handlers, folder_handlers+"/all.yml")
        utils.create_folder(folder_task)
        utils.yaml_writeln(tasks, folder_task+"/main.yml")
    # Parse Variabels
    vars_data = initial_vars(playbook, packager)
    utils.yaml_writeln(vars_data, playbook_dir+"/vars/all.yml")
    # cleaning package
    for rm in remove_package_dir:
        utils.rm_dir(playbook_dir+"/roles/"+rm)


def initial_vars(playbook, packager):
    vars_config = utils.nvc_config_vars(packager)['vars']['package']
    vars_item = None
    try:
        vars_item = playbook['vars']
    except Exception:
        vars_item = None
    vars_data = dict()
    for i in playbook['roles']:
        data = dict()
        for a in vars_config[i]['parameters']:
            try:
                params = vars_item[i][a]
            except Exception:
                params = vars_config[i]['parameters'][a]['default']
            if params is list():
                params = str(params)
            data[a] = params
        vars_data[i] = data
    return vars_data
