#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from fabric.contrib import files
from fabric.operations import sudo
from recipes import env
from recipes import scripts
from recipes.nginx import NginxDeploy
from recipes.utils import puts, required_envs, http_status, install_packages


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
        puts('transferring gunicorn configurarion and restart')
        if not config_file:
            config_file = os.path.join(scripts.__path__[0], 'gunicorn_project.conf')

        files.upload_template(filename=config_file,
                              destination="/etc/gunicorn.d/%s" % env.project_name,
                              context=env,
                              backup=False,
                              use_sudo=True)
        sudo('/etc/init.d/gunicorn restart %s' % env.project_name, pty=False)
        self.nginx.setup_site()

    def setup(self, config_file=None):
        install_packages([
            'gunicorn=0.13.4-1',
        ])
        self.nginx.setup_server()

    def status(self):
        http_status(host=env.host_string, port=env.gunicorn_port,  name='Gunicorn')
        self.nginx.status()
