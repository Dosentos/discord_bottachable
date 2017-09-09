# Discord-Bottachable

Discord bot that gathers all links shared in the specified channel and posts them to website

## Instructions for setting up development environment

- Install python 3.6.2 (anywhere u like)
- Create a folder for the project
- Go inside the folder you just made
- Run `virtualenv venv` (With virtualenv you can do clean environment and not pollute your entire pc)
- Run `source venv/Scripts/activate` or `venv\Scripts\activate.bat` if you're on Windows
  - Note that this only works on cmd, not for example in git bash
  - In your CL you should now have `(venv) λ` prefix
- Clone the repository from github
- Run `cd discord-bottachable`
- Run `pip install -r requirements.txt`
- To start local development use `heroku local web` or `heroku local web -f Procfile.windows` if you're on Windows


If you want to run the bot locally which is recommended, you should run 
- TO BE CONTINUED
TODO: install clean working environment locally. (NGROK?)

# Heroku starter Template

An utterly fantastic project starter template for Django 1.11.

## Features

- Production-ready configuration for Static Files, Database Settings, Gunicorn, etc.
- Enhancements to Django's static file serving functionality via WhiteNoise.
- Latest Python 3.6 runtime environment. 

## How to Use

To use this project, follow these steps:

1. Create your working environment.
2. Install Django (`$ pip install django`)
3. Create a new project using this template

## Creating Your Project

Using this template to create a new Django app is easy::

    $ django-admin.py startproject --template=https://github.com/heroku/heroku-django-template/archive/master.zip --name=Procfile helloworld

(If this doesn't work on windows, replace `django-admin.py` with `django-admin`)

You can replace ``helloworld`` with your desired project name.

## Deployment to Heroku

    $ git init
    $ git add -A
    $ git commit -m "Initial commit"

    $ heroku create
    $ git push heroku master

    $ heroku run python manage.py migrate

See also, a [ready-made application](https://github.com/heroku/python-getting-started), ready to deploy.

## Using Python 2.7?

Just update `runtime.txt` to `python-2.7.13` (no trailing spaces or newlines!).


## License: MIT

## Further Reading

- [Gunicorn](https://warehouse.python.org/project/gunicorn/)
- [WhiteNoise](https://warehouse.python.org/project/whitenoise/)
- [dj-database-url](https://warehouse.python.org/project/dj-database-url/)
