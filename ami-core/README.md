# MANAGE YOUR SERVERS 

Package Support

## STACK
- nginx
- mean | under construction
- gitlab | not tested
- lampp

## Application
- wordpress
- drupal
- magento
- joomla | under construction
- redmin | under contruction
- Firewalld
- composer

## Database
- mariadb
- mysql | not tested
- cockroachdb
- mongodb | under construction
- redis | undercontruction

## Programming Environment
- php7.2
- php5.6
- python3 flask framework environment
- python3 django framework environment
- node


# INSTALLING
## Requirements OS
Ubuntu Based
```
apt install ansible python-pip libmysqlclient-dev gcc
pip install mysql-python
```

Centos Based
```
yum install epel-release
yum install ansible python2-pip python2-devel mariadb-devel gcc
pip install mysql-python
```

## Requirements Apps

Debian Based
```
apt install python3 python3-pip python3-devel
sudo pip3 install -e .
```

Centos Based
```
yum install python36 python36-pip python36-devel
sudo pip3 install -e .
```

# RUNNING APP EXAMPLE
To see more examples, open the docs folder

## configure ami playbooks

Make a file with the name ami.yml | in ubuntu based change yum to apt
```
yum:
  hosts: all
  roles:
    - commons
    - mariadb
    - nginx
    - php
    - wordpress
  vars:
    mariadb:
      password: password
    wordpress:
      db_name: testing
      username: admin
      password: password
      wp_url: localhost
      email: meongbego@gmail.com
```
run playbook configure | wait report in playbook configured
```
$ ami playbook configure
2019-05-16 04:50:34 localhost.localdomain root[30300] INFO Playbook Configured
```
After this report now execute 
```
$ sudo ami playbook start
2019-05-16 04:50:34 localhost.localdomain root[30300] INFO Package Finished
```

Note : This Project under development
