FROM kartoza/django-base:3.7
ENV PYTHONUNBUFFERED 1
ENV PORT 8080

# Allows docker to cache installed dependencies between builds
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

# Adds our application code to the image
RUN mkdir /home/web/django_project/project
#COPY .. code
#WORKDIR code

# Configure Docker SSH
RUN apt-get update && apt-get install -y openssh-server sudo
RUN mkdir /var/run/sshd
RUN echo 'root:docker' | chpasswd

# Comment out PermitRootLogin setting
RUN sed -i 's/^PermitRootLogin */#PermitRootLogin /' /etc/ssh/sshd_config
# Write out PermitRootLogin setting at the end
RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile
#CMD /usr/sbin/sshd

# Open port 8080 as we will be running our django dev server on
EXPOSE 8080
# Open port 22 as we will be using a remote interpreter from pycharm
EXPOSE 22

# Run the development server
CMD newrelic-admin run-program gunicorn --bind 0.0.0.0:8080 --access-logfile - project.wsgi:application
