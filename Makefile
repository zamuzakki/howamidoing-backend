PROJECT_ID := howamidoing-backend

SHELL := /bin/bash

# ----------------------------------------------------------------------------
#    D E V E L O P M E N T     C O M M A N D S
# ----------------------------------------------------------------------------
default: web
run: build web migrate collectstatic

build:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Building in development mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) build web

web:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running in development mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) up -d web

migrate:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running migrate static in development mode"
	@echo "------------------------------------------------------------------"
	@# We add the '-' prefix to the next line as the migration may fail
	@# but we want to continue anyway.
	@#We need to migrate accounts first as it has a reference to user model
	-@docker-compose -p $(PROJECT_ID) exec build python manage.py migrate

collectstatic:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Collecting static in development mode"
	@echo "------------------------------------------------------------------"
	@docker exec $(PROJECT_ID)-build python manage.py collectstatic --noinput