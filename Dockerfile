FROM kartoza/django-base:3.7
ENV PYTHONUNBUFFERED 1
ENV PORT 8080

# Allows docker to cache installed dependencies between builds
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

# Adds our application code to the image
COPY . code
WORKDIR code

EXPOSE 8080

# Run the production server
CMD newrelic-admin run-program gunicorn --bind 0.0.0.0:8080 --access-logfile - project.wsgi:application