cd .. exec /bin/bash
cd blog_demo
nohup python manage.py runserver 0.0.0.0:5000 >./django.log 2>&1 &
cd .. exec /bin/bash
nohup python server.py >./server.log 2>&1 &