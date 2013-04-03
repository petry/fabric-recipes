#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fabric.api import env
from fabric.operations import run
from recipes.gunicorn import GunicornDeploy
from recipes.nginx import NginxDeploy
from recipes.utils import server_upgrade, puts, install_packages, required_envs
from recipes.project import ProjectDeploy


class DjangoDeploy(object):
    def __init__(self):
        super(DjangoDeploy, self).__init__()
        required_envs([
            'host_string'
        ])

        self.project = ProjectDeploy()
        self.nginx = NginxDeploy()

    def setup(self):
        puts("setup new project...")
        install_packages(
            [
                'git-core',
                'python-virtualenv'
            ]
        )
        server_upgrade()
        self.nginx.setup_server()

        self.deploy()

    def deploy(self):
        puts("Deploying Project...")
        self.project.deploy()
        self.collect_static()
        self.nginx.setup_site()

    def collect_static(self):
        puts("Collecting static files")
        run('{0}/bin/python {1}/manage.py collectstatic --noinput'.format(env.remote_virtualenv_path,
                                                                          env.remote_current_path))

    def status(self):
        self.nginx.status()