#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fabric.api import env
from fabric.operations import run
from recipes.utils import server_upgrade, puts, install_packages, required_envs
from recipes.gunicorn import gunicorn_deploy, gunicorn_setup
from recipes.nginx import nginx_setup_server, nginx_setup_site
from recipes.project import create_folder_for_project, upload_project, install_pip_dependancies, python_enviroment


class DjangoDeploy(object):

    def __init__(self):
        required_envs([
            'remote_virtualenv_path',
            'release_path'
        ])
        super(DjangoDeploy, self).__init__()

    def setup(self):
        puts("setup new project...")
        install_packages(
            [
                'git-core',
                'python-virtualenv'
            ]
        )
        server_upgrade()
        nginx_setup_server()
        gunicorn_setup()

        self.deploy()

    def deploy(self):
        puts("Deploying Project...")
        create_folder_for_project()
        python_enviroment()
        upload_project()
        install_pip_dependancies()
        self.collect_static()
        gunicorn_deploy()
        nginx_setup_site()

    def collect_static(self):
        puts("Collecting static files")
        run('{0}/bin/python {1}/manage.py collectstatic --noinput'.format(env.remote_virtualenv_path, env.release_path))
