# Fabric Recipes

a quick solution to perform deploy a Django app using nginx and gunicorn

## How to Use:

install the app in your enviroment:

```bash
$ pip install git+https://github.com/petry/fabric-recipes.git
```

create a git repository to your project with `manage.py` and `requirements.txt` on root folder download our `fabfile.py`: 

```bash
$ wget https://raw.github.com/petry/fabric-recipes-example/master/fabfile.py
```

If you like, change some fabric variables such as `env.user` and `env.password` on `fabfile.py`

then, run the commands to deploy your app on your server:

```bash
$ fab deploy
```

and this command to check if everything is working

```bash
$ fab status
```

or 

fork [these example project](https://github.com/petry/fabric-recipes-example) with this structure :)

https://github.com/petry/fabric-recipes-example

***


**NOTE** 
```
I tested this script using a virtual machine with ubuntu 10.04, feel free to create a version 
for your distribution of choice :)
```
