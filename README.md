Bonnie Web Service
==================

This is the web service giving access to the Bonnie elasticsearch
backend with logged data from Kolab Groupware activities.

The site is based on [Flask](http://http://flask.pocoo.org/).


Install and Run
---------------

Install Flask and some of the used modules:
```
$ pip install flask flask-bootstrap flask-httpauth flask-sqlalchemy flask-login flask-script
```

Get the app:
```
$ git clone git@github.com:kolab-groupware/bonnie-flask.git
$ cd bonnie-flask
$ export PYTHONPATH=/usr/lib64/python2.6/site-packages:/usr/lib/python2.6/site-packages:.
```

Initialize the database and create a user for API access:
```
$ python run.py shell
>>> db.create_all()
>>> webclient = User(username='webclient', permissions=Permission.API_ACCESS, password='Welcome2KolabSystems')
>>> db.session.add(webclient)
>>> db.session.commit()
```

Start the web server on port 8080:
```
$ python run.py runserver --host '0.0.0.0' --port 8080
```
