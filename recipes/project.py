#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
import os
from os.path import join
from fabric.context_managers import cd
from fabric.contrib import files
from fabric.operations import local, run, put, sudo
from recipes import env
from recipes.django import DjangoDeploy
from recipes.utils import create_directories, required_envs, server_upgrade, install_packages, puts
from recipes import config

class ProjectDeploy(object):
    def __init__(self):
        self.django = DjangoDeploy()
        self.extra_packages = env.extra_packages
        
    def create_folder(self):
        create_directories(config._remote_app_path, env.user, '0750')
        create_directories(config.remote_release_path, env.user, '0750')

    def upload(self):
        release_number = datetime.now().strftime('%Y%m%d%H%M%S')
        arquivo_tar = "/tmp/{0}-{1}.tar.gz".format(config.project_name, release_number)
        self.release_path = os.path.join(config.remote_release_path, release_number)

        self.package(arquivo_tar)
        self.send_to_server(arquivo_tar)
        self.unpackage_on_server(arquivo_tar)
        self.link_on_current_folder(release_number)

    def package(self, arquivo_tar):
        local("git archive --format=tar HEAD | gzip >{0}".format(arquivo_tar))

    def send_to_server(self, arquivo_tar):
        run('mkdir %s' % self.release_path)
        put(arquivo_tar, arquivo_tar)
        local("rm {0}".format(arquivo_tar))

    def unpackage_on_server(self, arquivo_tar):
        with cd(self.release_path):
            run('tar zxf {0} --pax-option="delete=SCHILY.*"'.format(arquivo_tar))
            run('rm {0}'.format(arquivo_tar))

    def link_on_current_folder(self, release_number):
        with cd(env.remote_app_path):
            run('rm -f current')
            run('ln -snf releases/{0} current'.format(release_number))

    def install_pip_dependancies(self):
        run("{0}/bin/pip install -r {1}/requirements.txt".format(env.remote_virtualenv_path, self.release_path))

    def create_python_enviroment(self):
        install_packages(
            [
                'python-virtualenv'
            ]
        )

        virtualenv_bin_file = join(env.remote_virtualenv_path, "bin/activate")
        if not files.exists(virtualenv_bin_file):
            create_directories(env.remote_virtualenv_path, env.user, '0750')
            run("virtualenv --distribute --no-site-packages %s" % env.remote_virtualenv_path)

    def install_pil(self):
        sudo('apt-get build-dep python-imaging -qy')
        if not files.exists('/usr/lib/libfreetype.so'):
            sudo('ln -s /usr/lib/`uname -i`-linux-gnu/libfreetype.so /usr/lib/')
        if not files.exists('/usr/lib/libjpeg.so'):
            sudo('ln -s /usr/lib/`uname -i`-linux-gnu/libjpeg.so /usr/lib/')
        if not files.exists('/usr/lib/libz.so'):
            sudo('ln -s /usr/lib/`uname -i`-linux-gnu/libz.so /usr/lib/')

    def deploy(self):
        if not files.exists('/usr/bin/git'):
            puts('new fresh server :D', m_type='warn')
            self.setup()

        puts("deploying your project")
        self.create_folder()
        self.create_python_enviroment()
        self.upload()
        self.install_pip_dependancies()
        self.django.deploy()

    def setup(self):
        puts("setup new project")
        server_upgrade()
        self.install_pil()
        install_packages(
            self.extra_packages +
            [
                'git-core',
                'curl',
            ]
        )

    def status(self):
        self.django.status()
