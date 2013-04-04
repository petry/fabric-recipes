#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fabric.api import env
from fabric.operations import run
from recipes.gunicorn import GunicornDeploy
from recipes.utils import puts, required_envs


class DjangoDeploy(object):
    def __init__(self):
        super(DjangoDeploy, self).__init__()
        required_envs([
            'host_string'
        ])

        self.gunicorn = GunicornDeploy(release_path=env.remote_release_path)

    def setup(self):
        self.gunicorn.setup()

    def deploy(self):
        puts("Deploying Project...")
        self.collect_static()
        self.gunicorn.deploy()

    def collect_static(self):
        puts("Collecting static files")
        run('{0}/bin/python {1}/manage.py collectstatic --noinput'.format(env.remote_virtualenv_path,
                                                                          env.remote_current_path))

    def status(self):
        self.gunicorn.status()