from fabric.contrib import files
from fabric.operations import run
import os
from fabric.api import env, local, sudo, prompt
from fabutils import install_packages, restart_service, new_user, \
    server_upgrade, create_directories, puts


env.project_name = "project"
env.project_dir = os.path.realpath(os.path.join(os.path.dirname(env.real_fabfile), ".."))

env.user = "usr_%s" % env.project_name
env.password = env.user
env.host_string = '127.0.0.1:2222'

env.server_user = env.user
env.server_project_dir = '/srv/%s/' % env.project_name
env.server_home_dir = '/home/%s/' % env.server_user
env.enviroment_dir = '%senviroment/' % env.server_home_dir

def nginx_server_base_configuration():
    puts('adding HTTP Server config files for project')
    files.upload_template("%s/deploy/nginx/server.conf" % env.project_dir,
                          "/etc/nginx/nginx.conf",
                          use_sudo=True)
    restart_service('nginx')

def nginx_setup():
    puts('installing NGINX')
    install_packages([
        'nginx',
    ])
    nginx_server_base_configuration()

def nginx_server_project_configuration():
    puts('adding HTTP Server config files')

    sudo("rm -f /etc/nginx/sites-enabled/default")
    sudo("rm -f /etc/nginx/sites-enabled/%s" % env.project_name)

    files.upload_template("%s/deploy/nginx/site.conf" % env.project_dir,
                          "/etc/nginx/sites-enabled/%s.conf" % env.project_name,
                          context=env,
                          use_sudo=True)
    restart_service('nginx')

def deploy():
    puts("Deploying Project...")
    nginx_server_project_configuration()

def setup():
    server_upgrade()
    nginx_setup()
    deploy()

