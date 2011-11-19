from fabric.contrib import files
from fabric.operations import run
import os
from fabric.api import env, local, sudo, prompt
from fabutils import install_packages, restart_service, new_user, \
    server_upgrade, create_directories, puts


env.project_name = "project"
env.project_dir = os.path.realpath(os.path.join(os.path.dirname(env.real_fabfile), ".."))

env.user = "usr_%s" % env.project_name
env.password = env.user
env.host_string = '127.0.0.1:2222'

env.server_user = env.user
env.server_project_dir = '/srv/%s/' % env.project_name
env.server_home_dir = '/home/%s/' % env.server_user
env.enviroment_dir = '%senviroment/' % env.server_home_dir

env.gunicorn_port = '8081'


def nginx_server_base_configuration():
    puts('adding HTTP Server config files for project')
    files.upload_template("%s/deploy/nginx/server.conf" % env.project_dir,
                          "/etc/nginx/nginx.conf",
                          use_sudo=True)
    restart_service('nginx')

def nginx_setup():
    puts('installing NGINX')
    install_packages([
        'nginx',
    ])
    nginx_server_base_configuration()

def nginx_server_project_configuration():
    puts('adding HTTP Server config files')

    sudo("rm -f /etc/nginx/sites-enabled/default")
    sudo("rm -f /etc/nginx/sites-enabled/%s" % env.project_name)

    files.upload_template("%s/deploy/nginx/site.conf" % env.project_dir,
                          "/etc/nginx/sites-enabled/%s.conf" % env.project_name,
                          context=env,
                          use_sudo=True)
    restart_service('nginx')

def gunicorn_setup():
    puts('Add Gunicorn init script')
    files.upload_template("%s/deploy/gunicorn/gunicorn_django_server" % env.project_dir,
                          "/etc/init.d/gunicorn_django",
                          use_sudo=True)
    sudo('chmod +x /etc/init.d/gunicorn_django')

def install_pip_dependancies():
    puts('install pip dependaecies')
    requirements = open('%s/requirements.txt' % env.project_dir, 'r')
    for module in requirements.readlines():
        run('%sbin/pip install %s' % (env.enviroment_dir, module))

def upload_project():
    git_url = local('git config --get remote.origin.url', capture=True)

    puts('cloning repository')
    local('rm -rf /tmp/git_repository')
    local('git clone %s /tmp/git_repository' % git_url)

    puts('uploading project files')
    local('cd /tmp/git_repository && tar -zcvf /tmp/%(project_name)s.tar %(project_name)s' % env)
    files.upload_template("/tmp/%s.tar" % env.project_name,
                          "%(server_project_dir)s%(project_name)s.tar" % env)
    run('tar -zxvf %(server_project_dir)s%(project_name)s.tar -C %(server_project_dir)s' % env)

def python_install_virtualenv():
    install_packages([
        'python-virtualenv',
        ])
    create_directories(env.server_project_dir, env.server_user, '0750')
    if not files.exists("%sbin/activate" % env.enviroment_dir):
        run("virtualenv --distribute --no-site-packages %s" % env.enviroment_dir)

def python_enviroment():
    puts('base python libs for system')
    python_install_virtualenv()

    install_pip_dependancies()

def gunicorn_deploy():
    puts('transferring gunicorn configurarion and restart')
    files.upload_template("%s/deploy/gunicorn/gunicorn_django_site" % env.project_dir,
                          "/etc/default/gunicorn_django-%s" % env.project_name,
                          context=env,
                          use_sudo=True)

    sudo('/etc/init.d/gunicorn_django restart %s' % env.project_name, pty=False)

def deploy():
    puts("Deploying Project...")
    nginx_server_project_configuration()

    python_enviroment()
    upload_project()
    gunicorn_deploy()

def setup():
    server_upgrade()
    nginx_setup()
    gunicorn_setup()
    deploy()
