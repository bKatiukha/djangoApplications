 lsof -nti:8000 | xargs kill -9 
 python manage.py runserver 8000