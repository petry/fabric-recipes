Django fabric is a quick solution to perform deploy a Django app using nginx and gunicorn

How to Use:
-----------
First, change the Variables env.user env.password on deploy/fabfile.py deploy,
 (for obvious reasons, this user must have sudo permission).

Just run

    fab setup

Fab setup will update the system, install nginx, python dependencies of the project,
and the application that is in repository.

Any change in application, just run the command

    fab deploy


