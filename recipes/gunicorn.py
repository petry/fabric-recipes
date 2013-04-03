#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from fabric.contrib import files
from fabric.operations import sudo
from fabric.state import env
from recipes import scripts
from recipes.utils import puts, required_envs


class GunicornDeploy(object):

    def __init__(self, release_path):
        super(GunicornDeploy, self).__init__()
        self.release_path = release_path
        required_envs([
            'project_name',
            'gunicorn_port'
        ])

    def deploy(self, config_file=None):
        puts('transferring gunicorn configurarion and restart')
        if not config_file:
            config_file = os.path.join(scripts.__path__[0], 'gunicorn_django_site')

        files.upload_template(filename=config_file,
                              destination="/etc/default/gunicorn_django-%s" % env.project_name,
                              context=env,
                              use_sudo=True)
        sudo('/etc/init.d/gunicorn_django restart %s' % env.project_name, pty=False)

    def setup(self, config_file=None):
        puts('Add Gunicorn init script')
        if not config_file:
            config_file = os.path.join(scripts.__path__[0], 'gunicorn_django_server')

        files.upload_template(filename=config_file,
                              destination="/etc/init.d/gunicorn_django",
                              use_sudo=True)
        sudo('chmod +x /etc/init.d/gunicorn_django')