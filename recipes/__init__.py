#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import join
from fabric.api import env

class RecipeConfig(object):

    def __init__(self, env):
        self.env = env
        self._remote_build_path = join('/opt/projects/', self.project_name)
        self._remote_app_path = join(self._remote_build_path, 'app')

    @property
    def project_name(self):
        try:
            return self.env.project_name
        except AttributeError:
            return 'unnamed'

    @property
    def remote_app_path(self):
        try:
            return self.env.remote_app_path
        except AttributeError:
            return self._remote_app_path

    @property
    def remote_virtualenv_path(self):
        try:
            return self.env.remote_virtualenv_path
        except AttributeError:
            return join(self._remote_build_path, "virtualenv")

    @property
    def remote_release_path(self):
        try:
            return self.env.remote_release_path
        except AttributeError:
            return join(self._remote_app_path, "releases")

    @property
    def remote_current_path(self):
        try:
            return self.env.remote_current_path
        except AttributeError:
            return join(self._remote_app_path, "current")

    @property
    def gunicorn_port(self):
        try:
            return self.env.gunicorn_port
        except AttributeError:
            return 8800

    @property
    def project_domain(self):
        try:
            return self.env.project_domain
        except AttributeError:
            return "my-awesome-website.com"


config = RecipeConfig(env)

env.project_name = config.project_name
env.remote_virtualenv_path = config.remote_virtualenv_path
env.remote_release_path = config.remote_release_path
env.remote_current_path = config.remote_current_path
env.gunicorn_port = config.gunicorn_port
env.project_domain = config.project_domain
env.remote_app_path = config.remote_app_path
