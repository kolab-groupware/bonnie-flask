Bonnie Web Service
==================

This is the web service giving access to the Bonnie elasticsearch
backend with logged data from Kolab Groupware activities.

The site is based on [Flask](http://http://flask.pocoo.org/).


Install and Run
---------------

Install Flask and some of the used modules:
```
$ pip install flask flask-bootstrap flask-httpauth flask-sqlalchemy flask-login flask-script flask-wtf flask-babel flask-httpauth itsdangerous
```

or on a CentOS/RHEL Kolab development box:
```
$ yum -y install python-flask python-flask-sqlalchemy python-pip python-argparse
$ pip install flask-bootstrap flask-login flask-script flask-wtf flask-babel flask-httpauth itsdangerous
$ pip install --upgrade sqlalchemy
```

If using the [Riak](http://basho.com/riak/) storage backend, also install the Riak Python client library:
```
$ yum -y install python-devel libffi-devel
$ pip install riak
```

Get the app:
```
$ git clone git@github.com:kolab-groupware/bonnie-flask.git
$ cd bonnie-flask
$ export PYTHONPATH=/usr/lib64/python2.6/site-packages:/usr/lib/python2.6/site-packages:.
```

Initialize the database and create users for API access and administration:
```
$ python run.py shell
>>> db.create_all()
>>> admin = User(username='admin', permissions=Permission.WEB_ACCESS|Permission.ADMINISTRATOR, password='Welcome2KolabSystems', secret='none')
>>> webclient = User(username='webclient', permissions=Permission.API_ACCESS, password='Welcome2KolabSystems', secret='8431f19170e7f90d4107bf4b169baf')
>>> db.session.add(admin)
>>> db.session.add(webclient)
>>> db.session.commit()
```

Start the web server on port 8080:
```
$ python run.py runserver --host '0.0.0.0' --port 8080
```


Development Hints
-----------------

Update localization files:
```
$ pybabel extract -F config/babel.conf -o po/bonnie-flask.pot .
```
see [Flask-Babel](https://pythonhosted.org/Flask-Babel/) documentation for details.