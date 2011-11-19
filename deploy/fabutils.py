# -*- coding: utf-8 -*-
from fabric.context_managers import settings
from fabric.api import env, run, sudo

class Print:
    colors = {
        'blue':'\033[94m',
        'green':'\033[92m',
        'red':'\033[91m',
        'yellow':'\033[93m',
    }

    @classmethod
    def _get_color(cls, color):
        return cls.colors[color]

    @classmethod
    def text(cls, text, color):
        return "%s%s%s" % (cls._get_color(color),  text, '\033[0m')


def puts(msg):
    fabric_put( Print.text(msg, 'blue') )

def install_packages(packages):
    with settings(warn_only=True):
        sudo("aptitude -y install %s" % (' '.join(packages),))

def server_upgrade():
    Print.text('updating server', 'blue')
    with settings(warn_only=True):
        sudo("aptitude -y update")
        sudo("aptitude -y full-upgrade")


def restart_service(service):
    sudo("service %s stop" % (service,))
    sudo("service %s start" % (service,))


    