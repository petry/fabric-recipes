# -*- coding: utf-8 -*-
from fabric.context_managers import settings
from fabric.api import sudo
from fabric.api import puts as fabric_puts
from fabric import colors


def puts(msg, type='info'):
    messages_by_type = {
        'info': colors.blue(msg),
        'success': colors.green(msg),
        'warn': colors.yellow(msg),
        'error': colors.red(msg)
    }

    fabric_puts(messages_by_type[type])


def install_packages(packages):
    with settings(warn_only=True):
        sudo("aptitude -y install %s" % (' '.join(packages),))


def server_upgrade():
    puts('updating server')
    with settings(warn_only=True):
        sudo("aptitude -y update")
        sudo("aptitude -y upgrade")


def restart_service(service):
    sudo("service %s stop" % (service,))
    sudo("service %s start" % (service,))


def create_directories(path, user, permission, group=None):
    group = group or user

    sudo("mkdir -p %s" % path)
    sudo("chown %s:%s %s" % (user, group, path))
    sudo("chmod %s %s" % (permission, path))
