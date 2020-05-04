PROJECT_ID := howamidoing-backend

SHELL := /bin/bash

# ----------------------------------------------------------------------------
#    D E V E L O P M E N T     C O M M A N D S
# ----------------------------------------------------------------------------
default: web
run: build web migrate collectstatic superuser

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
	-@docker exec $(PROJECT_ID)-web python manage.py migrate

superuser:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Creating a superuser in development mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) exec web python manage.py createsuperuser

collectstatic:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Collecting static in development mode"
	@echo "------------------------------------------------------------------"
	@docker exec $(PROJECT_ID)-web python manage.py collectstatic --noinput

status:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Show status for all containers"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) ps

kill:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Killing in development mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) kill

rm: kill
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Removing development instance!!! "
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) rm

shell:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Shelling in in development mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) exec web /bin/bash

dbbash:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Bashing in to development database"
	@echo "------------------------------------------------------------------"
	@docker exec -t -i $(PROJECT_ID)-db /bin/bash

dbbash:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Bashing in to development database"
	@echo "------------------------------------------------------------------"
	@docker exec -t -i $(PROJECT_ID)-db /bin/bash

dbshell:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Shelling in in development database"
	@echo "------------------------------------------------------------------"
	@docker exec -t -i $(PROJECT_ID)-db psql -U docker -h localhost gis

flake8:
	@echo "Check flake 8"
	@flake8