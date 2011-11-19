from fabric.contrib import files
from fabric.operations import run
import os
from fabric.api import env, local, sudo, prompt


env.project_name = "project"
env.project_dir = os.path.realpath(os.path.join(os.path.dirname(env.real_fabfile), ".."))

env.user = "usr_%s" % env.project_name
env.password = env.user
env.host_string = '127.0.0.1:2222'


