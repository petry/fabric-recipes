#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fabric.api import env
from fabric.operations import run
from recipes.gunicorn import GunicornDeploy
from recipes.nginx import NginxDeploy
from recipes.utils import server_upgrade, puts, install_packages, required_envs
from recipes.project import create_folder_for_project, upload_project, install_pip_dependancies, python_enviroment


class DjangoDeploy(object):

    def __init__(self):
        super(DjangoDeploy, self).__init__()
        required_envs([
            'remote_virtualenv_path',
        ])
        self.nginx = NginxDeploy()
        self.gunicorn = GunicornDeploy()

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
        self.gunicorn.setup()

        self.deploy()

    def deploy(self):
        puts("Deploying Project...")
        create_folder_for_project()
        python_enviroment()
        upload_project()
        install_pip_dependancies()
        self.collect_static()
        self.gunicorn.deploy()
        self.nginx.setup_site()

    def collect_static(self):
        puts("Collecting static files")
        run('{0}/bin/python {1}/manage.py collectstatic --noinput'.format(env.remote_virtualenv_path,
                                                                          env.release_path))
