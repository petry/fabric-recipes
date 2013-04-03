#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from fabric.colors import green, red
from fabric.contrib import files
from fabric.operations import sudo, local
from fabric.state import env
from recipes import scripts
from recipes.gunicorn import GunicornDeploy
from recipes.utils import puts, install_packages, restart_service, required_envs, http_status


class NginxDeploy(object):

    def __init__(self):
        super(NginxDeploy, self).__init__()
        required_envs([
            'project_name',
            'project_domain',
            'gunicorn_port'
        ]
        )
        self.gunicorn = GunicornDeploy(release_path=env.remote_release_path)

    def setup_server(self, config_file=None):
        self.gunicorn.setup()

        puts('installing NGINX')
        if not config_file:
            config_file = os.path.join(scripts.__path__[0], 'nginx_server.conf')
        install_packages([
            'nginx',
        ])
        puts('adding HTTP Server config files for project')
        files.upload_template(filename=config_file,
                              destination="/etc/nginx/nginx.conf",
                              use_sudo=True)
        restart_service('nginx')

    def setup_site(self, config_file=None):
        self.gunicorn.deploy()

        if not config_file:
            config_file = os.path.join(scripts.__path__[0], 'nginx_site.conf')
        puts('adding HTTP Server config files')

        sudo("rm -f /etc/nginx/sites-enabled/%s" % env.project_name)

        files.upload_template(filename=config_file,
                              destination="/etc/nginx/sites-enabled/%s.conf" % env.project_name,
                              context=env,
                              use_sudo=True)
        restart_service('nginx')


    def status(self):
        host = env.host_string
        http_status(host=host, port="80", name='NGIX', run_local=True)

        self.gunicorn.status()