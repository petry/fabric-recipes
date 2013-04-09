#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from fabric.contrib import files
from fabric.operations import sudo
from recipes import env
from recipes import scripts
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

    def setup_server(self, config_file=None):
        puts('installing NGINX')
        if not config_file:
            config_file = os.path.join(scripts.__path__[0], 'nginx_server.conf')
        install_packages([
            'nginx',
        ])
        puts('adding base HTTP Server config files')
        files.upload_template(filename=config_file,
                              destination="/etc/nginx/nginx.conf",
                              use_sudo=True)

    def setup_site(self, config_file=None):
        if not files.exists('/etc/init.d/nginx'):
            puts('nginx not found, running setup', m_type='warn')
            self.setup_server()


        puts('adding HTTP Server config files for project')
        if not config_file:
            config_file = os.path.join(scripts.__path__[0], 'nginx_site.conf')

        sudo("rm -f /etc/nginx/sites-enabled/%s" % env.project_name)

        files.upload_template(filename=config_file,
                              destination="/etc/nginx/sites-enabled/%s.conf" % env.project_name,
                              context=env,
                              use_sudo=True)
        restart_service('nginx')

    def status(self):
        host = env.host_string
        http_status(host=host, port="80", name='NGINX', run_local=True)
