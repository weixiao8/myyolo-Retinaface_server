@echo off
start python server.py
cd blog_demo
python manage.py runserver 0.0.0.0:10004
exit
