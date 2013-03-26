#!/usr/bin/env python
# encoding: utf-8
import sys
import os
from datetime import datetime

from fabric.contrib import files
from fabric.operations import run
from fabric.api import env, local, sudo
from fabutils import install_packages, restart_service, create_directories, puts
from os.path import join

from fabric.api import *
from fabric.context_managers import settings as _settings


def nginx_setup_server(server_config_file):
    puts('installing NGINX')
    install_packages([
        'nginx',
    ])

    puts('adding HTTP Server config files for project')
    files.upload_template(filename=server_config_file,
                          destination="/etc/nginx/nginx.conf",
                          use_sudo=True)
    restart_service('nginx')


def python_enviroment():
    virtualenv_bin_file = join(env.remote_virtualenv_path, "bin/activate")
    if not files.exists(virtualenv_bin_file):
        create_directories(env.remote_virtualenv_path, env.user, '0750')
        run("virtualenv --distribute --no-site-packages %s" % env.remote_virtualenv_path)


def gunicorn_setup(gunicorn_server_script):
    puts('Add Gunicorn init script')
    files.upload_template(filename=gunicorn_server_script,
                          destination="/etc/init.d/gunicorn_django",
                          use_sudo=True)
    sudo('chmod +x /etc/init.d/gunicorn_django')


def create_folder_for_project():
    create_directories(env.remote_app_path, env.user, '0750')
    create_directories(env.remote_release_path, env.user, '0750')


def upload_project():
    env.release_number = datetime.now().strftime('%Y%m%d%H%M%S')
    env.release_path = os.path.join(env.remote_release_path, env.release_number)
    env.arquivo_tar = "/tmp/{0}-{1}.tar.gz".format(env.project_name, env.release_number)

    package_project(env.arquivo_tar)
    send_project_to_server(env.arquivo_tar)
    unpackage_projet_on_server(env.arquivo_tar)
    link_project_on_current_folder(env.release_number)


def package_project(arquivo_tar):
    local("git archive --format=tar HEAD | gzip >{0}".format(arquivo_tar))


def send_project_to_server(arquivo_tar):
    run('mkdir %s' % env.release_path)
    put(arquivo_tar, arquivo_tar)
    local("rm {0}".format(arquivo_tar))


def unpackage_projet_on_server(arquivo_tar):
    with cd(env.release_path):
        run('tar zxf {0} --pax-option="delete=SCHILY.*"'.format(env.arquivo_tar))
        run('rm {0}'.format(env.arquivo_tar))

def link_project_on_current_folder(release_number):
    with cd(env.remote_app_path):
        run('rm -f current')
        run('ln -snf releases/{0} current'.format(release_number))

def install_pip_dependancies():
    run("{0}/bin/pip install -r {1}/requirements.txt".format(env.remote_virtualenv_path, env.release_path))


def collect_static():
    run('{0}/bin/python {1}/manage.py collectstatic --noinput'.format(env.remote_virtualenv_path, env.release_path))


def gunicorn_deploy(gunicorn_project_config_file):
    puts('transferring gunicorn configurarion and restart')
    files.upload_template(filename=gunicorn_project_config_file,
                          destination="/etc/default/gunicorn_django-%s" % env.project_name,
                          context=env,
                          use_sudo=True)
    sudo('/etc/init.d/gunicorn_django restart %s' % env.project_name, pty=False)



def nginx_setup_site(nginx_project_config_file):
    puts('adding HTTP Server config files')

    sudo("rm -f /etc/nginx/sites-enabled/%s" % env.project_name)

    files.upload_template(filename=nginx_project_config_file,
                          destination="/etc/nginx/sites-enabled/%s.conf" % env.project_name,
                          context=env,
                          use_sudo=True)
    restart_service('nginx')
