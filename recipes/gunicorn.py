#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from fabric.contrib import files
from fabric.operations import sudo
from recipes import env
from recipes import scripts
from recipes.nginx import NginxDeploy
from recipes.utils import puts, required_envs, http_status, install_packages, restart_service


class GunicornDeploy(object):

    def __init__(self, release_path):
        super(GunicornDeploy, self).__init__()
        self.release_path = release_path
        self.nginx = NginxDeploy()

        required_envs([
            'project_name',
            'gunicorn_port'
        ])

    def deploy(self, config_file=None):
        if not files.exists('/etc/init.d/gunicorn'):
            puts('gunicorn init script not found, running setup', m_type='warn')
            self.setup()

        puts('transferring gunicorn configurarion and restart')
        if not config_file:
            config_file = os.path.join(scripts.__path__[0], 'gunicorn_project.conf')

        files.upload_template(filename=config_file,
                              destination="/etc/gunicorn.d/%s" % env.project_name,
                              context=env,
                              backup=False,
                              use_sudo=True)
        restart_service('gunicorn')
        self.nginx.setup_site()

    def setup(self):
        puts('Installing Gunicorn')
        install_packages([
            'gunicorn=0.13.4-1',
        ])

    def status(self):
        http_status(host=env.host_string, port=env.gunicorn_port,  name='Gunicorn')
        self.nginx.status()
