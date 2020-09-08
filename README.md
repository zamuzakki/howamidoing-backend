# howamidoing
App for anyone to register their status, initially during covid-19 lockdown / quarantine


## API Demo
You can see the demo of the API on [https://howamidoing.backend.kartoza.com/](https://howamidoing.backend.kartoza.com/).

If you want to see how this API works after being intergrated with the Frontend, you can check 
[https://howamidoing.kartoza.com/](https://howamidoing.kartoza.com/)


## Quick Installation on local

1.  Clone the repo:

```
$ git clone https://github.com/kartoza/howamidoing-backend.git
```

2. Run this app locally:
```
$ cd howamidoing-backend/deployment
$ make build        # build container from the image
$ make web          # run container
$ make migrate      # migrate database
$ make superuser    # create superuser
```

3. Open your browser and go to [http://localhost:51202](http://localhost:51202).


## API Usage How-to

Please refer to this [doc](https://github.com/kartoza/howamidoing-backend/blob/develop/docs) for endpoints, authentication, and initial KmGrid setup.