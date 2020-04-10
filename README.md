# howamidoing
App for anyone to register their status, initially during covid-19 lockdown / quarantine


## First-time setup

1.  Make sure Python 3.6x, Pip, and Virtualenv are already installed. 
See [here](https://robbinespu.gitlab.io/blog/2019/07/23/Python-36-with-VirtualEnv/) and 
[here](https://linuxize.com/post/how-to-install-pip-on-ubuntu-18.04/) for help.

2. Make sure PostGIS (and PostgreSQL) is already installed 
([See here](https://computingforgeeks.com/how-to-install-postgis-on-ubuntu-debian/)). You can also use Kartoza PostGIS
docker. [See here](https://hub.docker.com/r/kartoza/postgis/)

3. Because we want to run Django with PostgreSQL, we need to install required prerequisites.
```
$ sudo apt install libpq-dev python3-dev python3.6-dev
```

4.  Clone the repo and configure the virtual environment:

```
$ git clone https://github.com/kartoza/howamidoing-backend.git
$ cd howamidoing-backend
$ virtualenv --python=/usr/bin/python3.6 venv
$ source /venv/bin/activate
(venv) $ pip install -r requirements.txt
```

5. Configure environment variables using `.env` file. Check `.env_example`
[here](https://github.com/kartoza/howamidoing-backend/blob/dev-zakki/.env_example).

6.  Migrate the models to database.

```
(venv) $ python manage.py migrate
```

7.  Create a superuser:

```
(venv) $ python manage.py createsuperuser
```

8.  Run test.

```
(venv) $ python manage.py test
```

9.  Confirm everything is working:

```
(venv) $ python manage.py runserver
```

10. Load the site at [http://localhost:8000](http://localhost:8000).