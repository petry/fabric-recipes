# -*- coding: utf-8 -*-
from fabric.colors import red, green
from fabric.context_managers import settings
from fabric.api import sudo
from fabric.api import puts as fabric_puts
from fabric import colors
from fabric.operations import local, run
from fabric.state import env
from fabric.utils import error


def puts(msg, m_type='info'):
    messages_by_type = {
        'info': colors.blue(msg),
        'success': colors.green(msg),
        'warn': colors.yellow(msg),
        'error': colors.red(msg)
    }

    fabric_puts(messages_by_type[m_type])


def install_packages(packages):
    with settings(warn_only=True):
        sudo("apt-get -qqy install %s" % (' '.join(packages),))


def server_upgrade():
    puts('updating server')
    with settings(warn_only=True):
        sudo("apt-get -qqy update")
        # sudo("aptitude -y upgrade")


def restart_service(service):
    sudo("service %s stop" % (service,))
    sudo("service %s start" % (service,))


def create_directories(path, user, permission, group=None):
    group = group or user

    sudo("mkdir -p %s" % path)
    sudo("chown %s:%s %s" % (user, group, path))
    sudo("chmod %s %s" % (permission, path))


def required_envs(env_list):
    missing = []
    for var in env_list:
        if var not in env.keys():
            missing.append(var)
    if missing:
        message = "\nYou forgot to set some variables to deploy:\n"
        for var in missing:
            message += " - {0}\n".format(var)

        error(red(message))


def http_status(host, port="80", name="", run_local=False):
    if run_local:
        url = "{0}:{1}".format(host, port)
        status = local("curl -o /dev/null --silent --head --write-out '%{http_code}' " + url, capture=True)
    else:
        url = "127.0.0.1:{0}".format(port)
        status = run("curl -o /dev/null --silent --head --write-out '%{http_code}' " + url)
    if status == '200':
        print(name + " " + green('OK'))
    else:
        print(name + " " + red('FAIL'))
