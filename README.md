Bonnie Web Service
==================

This is the web service giving access to the Bonnie elasticsearch
backend with logged data from Kolab Groupware activities.

The site is based on [Flask](http://http://flask.pocoo.org/)


Install and Run
---------------

Install Flask and some of the used modules:
```
$ pip install flask
$ pip install flask-bootstrap
$ pip install flask-httpauth
```

Get the app and start the web server:
```
(tg2env)$ git clone git@github.com:kolab-groupware/bonnie-flask.git
(tg2env)$ cd bonnie-flask
(tg2env)$ export PYTHONPATH=/usr/lib64/python2.6/site-packages:/usr/lib/python2.6/site-packages:.
(tg2env)$ python run.py
```
