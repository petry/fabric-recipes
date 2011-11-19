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

def new_user(admin_username, admin_password, group):
    # Create the admin group and add it to the sudoers file
    admin_group = group
    try:
        sudo('addgroup {group}'.format(group=admin_group))
        sudo('echo "%{group} ALL=(ALL) ALL" >> /etc/sudoers'.format(group=admin_group))
    except:
        pass

    # Create the new admin user (default group=username); add to admin group
    sudo('adduser {username} --disabled-password --gecos ""'.format(
        username=admin_username))
    sudo('adduser {username} {group}'.format(
        username=admin_username,
        group=admin_group))

    # Set the password for the new admin user
    sudo('echo "{username}:{password}" | chpasswd'.format(
        username=admin_username,
        password=admin_password))


def create_directories(path, user, permission, group=None):
    group = group or user

    sudo("mkdir -p %s" % path)
    sudo("chown %s:%s %s" % (user, group, path))
    sudo("chmod %s %s" % (permission, path))
    