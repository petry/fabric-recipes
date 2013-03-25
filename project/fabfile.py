import os
from fabric.decorators import task
from fabric.api import env
from fabricdeploy.functions import gunicorn_setup, nginx_setup, gunicorn_deploy, upload_project, python_enviroment, nginx_server_project_configuration
from fabutils import server_upgrade, puts

env.project_name = "project"
env.project_dir = os.path.realpath(os.path.join(os.path.dirname(env.real_fabfile), ".."))

env.user = "usr_%s" % env.project_name
env.password = env.user
env.host_string = '127.0.0.1:2222'

env.server_user = env.user
env.server_project_dir = '/srv/%s/' % env.project_name
env.server_home_dir = '/home/%s/' % env.server_user
env.enviroment_dir = '%senviroment/' % env.server_home_dir


@task
def deploy():
    puts("Deploying Project...")
    nginx_server_project_configuration(
        project_dir=env.project_dir,
        project_name=env.project_name)

    python_enviroment(project_dir=env.project_dir)
    upload_project(project_name=env.project_name)
    gunicorn_deploy(project_dir=env.project_dir, project_name=env.project_name)


@task
def setup():
    server_upgrade()
    nginx_setup(project_dir=env.project_dir)
    gunicorn_setup(project_dir=env.project_dir)
    deploy()
