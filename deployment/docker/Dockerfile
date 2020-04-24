FROM kartoza/django-base:3.7


ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN pip install uwsgi

# Open port 8080 as we will be running our app on that
EXPOSE 8080

WORKDIR /home/web/django_project
CMD ["uwsgi", "--ini", "/uwsgi.conf"]