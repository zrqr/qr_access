# Useful django commands
## How to create a django project (No need to run this)
django-admin startproject <django project name>

## To create a new app 
python manage.py startapp <AppName>
## To start Server
python manage.py runserver 172.17.0.2:8000
<br>Ctrl+C to stop

## when updating data model
python manage.py makemigrations
<br>python manage.py migrate

## Install vscode extention
Thunder Client
<br> to test the API

## API endpoints can be found in 
backend/django_project/qr_manager/urls.py