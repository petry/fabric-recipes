#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from fabric.contrib import files
from fabric.operations import sudo
from fabric.state import env
from recipes import scripts
from recipes.utils import puts


def gunicorn_deploy(config_file=None):
    if not config_file:
        config_file = os.path.join(scripts.__path__[0], 'gunicorn_django_site')

    puts('transferring gunicorn configurarion and restart')
    files.upload_template(filename=config_file,
                          destination="/etc/default/gunicorn_django-%s" % env.project_name,
                          context=env,
                          use_sudo=True)
    sudo('/etc/init.d/gunicorn_django restart %s' % env.project_name, pty=False)


def gunicorn_setup(config_file=None):
    if not config_file:
        config_file = os.path.join(scripts.__path__[0], 'gunicorn_django_server')

    puts('Add Gunicorn init script')
    files.upload_template(filename=config_file,
                          destination="/etc/init.d/gunicorn_django",
                          use_sudo=True)
    sudo('chmod +x /etc/init.d/gunicorn_django')