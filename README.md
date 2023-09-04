start:

    lsof -nti:8000 | xargs kill -9 
    python manage.py runserver 8000

 

    pip3 install libsass django-compressor django-sass-processor
