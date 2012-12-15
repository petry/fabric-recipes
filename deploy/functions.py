from fabric.contrib import files
from fabric.operations import run
from fabric.api import env, local, sudo
from fabutils import install_packages, restart_service, create_directories, puts


def nginx_server_base_configuration(project_dir):
    puts('adding HTTP Server config files for project')
    files.upload_template("%s/deploy/nginx/server.conf" % project_dir,
                          "/etc/nginx/nginx.conf",
                          use_sudo=True)
    restart_service('nginx')


def nginx_setup(project_dir):
    puts('installing NGINX')
    install_packages([
        'nginx',
    ])
    nginx_server_base_configuration(project_dir)


def nginx_server_project_configuration(project_dir, project_name):
    puts('adding HTTP Server config files')

    sudo("rm -f /etc/nginx/sites-enabled/default")
    sudo("rm -f /etc/nginx/sites-enabled/%s" % project_name)

    files.upload_template("%s/deploy/nginx/site.conf" % project_dir,
                          "/etc/nginx/sites-enabled/%s.conf" % project_name,
                          context=env,
                          use_sudo=True)
    restart_service('nginx')


def gunicorn_setup(project_dir):
    puts('Add Gunicorn init script')
    files.upload_template("%s/deploy/gunicorn/gunicorn_django_server" % project_dir,
                          "/etc/init.d/gunicorn_django",
                          use_sudo=True)
    sudo('chmod +x /etc/init.d/gunicorn_django')


def install_pip_dependancies(project_dir, enviroment_dir):
    puts('install pip dependaecies')
    requirements = open('%s/requirements.txt' % project_dir, 'r')
    for module in requirements.readlines():
        run('%sbin/pip install %s' % (enviroment_dir, module))


def upload_project(project_name):
    git_url = local('git config --get remote.origin.url', capture=True)

    puts('cloning repository')
    local('rm -rf /tmp/git_repository')
    local('git clone %s /tmp/git_repository' % git_url)

    puts('uploading project files')
    local('cd /tmp/git_repository && tar -zcvf /tmp/%(project_name)s.tar %(project_name)s' % env)
    files.upload_template("/tmp/%s.tar" % project_name,
                          "%(server_project_dir)s%(project_name)s.tar" % env)
    run('tar -zxvf %(server_project_dir)s%(project_name)s.tar -C %(server_project_dir)s' % env)


def python_install_virtualenv(server_project_dir, server_user, enviroment_dir):
    install_packages(
        [
            'python-virtualenv'
        ]
    )
    create_directories(server_project_dir, server_user, '0750')
    if not files.exists("%sbin/activate" % enviroment_dir):
        run("virtualenv --distribute --no-site-packages %s" % enviroment_dir)


def python_enviroment(project_dir, server_project_dir, server_user, enviroment_dir):
    puts('base python libs for system')
    python_install_virtualenv(
        server_project_dir=server_project_dir,
        server_user=server_user,
        enviroment_dir=enviroment_dir)

    install_pip_dependancies(project_dir=project_dir)


def gunicorn_deploy(project_dir, project_name):
    puts('transferring gunicorn configurarion and restart')
    files.upload_template("%s/deploy/gunicorn/gunicorn_django_site" % project_dir,
                          "/etc/default/gunicorn_django-%s" % project_name,
                          context=env,
                          use_sudo=True)

    sudo('/etc/init.d/gunicorn_django restart %s' % project_name, pty=False)
