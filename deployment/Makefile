PROJECT_ID := howamidoing-backend

SHELL := /bin/bash

# ----------------------------------------------------------------------------
#    DEVELOPMENT     C O M M A N D S
# ----------------------------------------------------------------------------
default: devweb
run: build-devweb permissions devweb migrate collectstatic

build-devweb:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Building in development mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) build devweb

devweb:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running in development mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) up --no-deps -d devweb

permissions:
	# Probably we want something more granular here....
	# Your sudo password will be needed to set the file permissions
	# on logs, media, static and pg dirs
	@if [ ! -d "logs" ]; then mkdir logs; fi
	@if [ ! -d "media" ]; then mkdir media; fi
	@if [ ! -d "static" ]; then mkdir static; fi
	@if [ ! -d "backups" ]; then mkdir backups; fi
	@if [ -d "logs" ]; then sudo chmod -R a+rwx logs; fi
	@if [ -d "media" ]; then sudo chmod -R a+rwx media; fi
	@if [ -d "static" ]; then sudo chmod -R a+rwx static; fi
	@if [ -d "pg" ]; then sudo chmod -R a+rwx pg; fi
	@if [ -d "backups" ]; then sudo chmod -R a+rwx backups; fi

db:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running db in development mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) up -d db

nginx:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running nginx in development mode"
	@echo "Normally you should use this only for testing"
	@echo "In a development environment you will typically use nginx running"
	@echo "on the host rather if you have a multi-site host."
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) up -d nginx
	@echo "Site should now be available at http://localhost"

migrate:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running migrate static in development mode"
	@echo "------------------------------------------------------------------"
	@#http://stackoverflow.com/questions/29689365/auth-user-error-with-django-1-8-and-syncdb-migrate
	@#and
	@#http://stackoverflow.com/questions/3143635/how-to-ignore-mv-error
	@# We add the '-' prefix to the next line as the migration may fail
	@# but we want to continue anyway.
	@#We need to migrate accounts first as it has a reference to user model
	@-docker-compose -p $(PROJECT_ID) exec uwsgi python manage.py migrate

collectstatic:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Collecting static in development mode"
	@echo "------------------------------------------------------------------"
	#@docker-compose -p $(PROJECT_ID) run uwsgi python manage.py collectstatic --noinput
	#We need to run collect static in the same context as the running
	# uwsgi container it seems so I use docker exec here
	# no -it flag so we can run over remote shell
	@docker exec $(PROJECT_ID)-uwsgi python manage.py collectstatic --noinput