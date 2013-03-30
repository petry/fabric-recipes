from datetime import datetime
import os
from os.path import join
from fabric.context_managers import cd
from fabric.contrib import files
from fabric.operations import local, run, put
from fabric.state import env
from recipes.utils import create_directories

__author__ = 'petry'


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


def python_enviroment():
    virtualenv_bin_file = join(env.remote_virtualenv_path, "bin/activate")
    if not files.exists(virtualenv_bin_file):
        create_directories(env.remote_virtualenv_path, env.user, '0750')
        run("virtualenv --distribute --no-site-packages %s" % env.remote_virtualenv_path)