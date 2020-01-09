[![Save Service](https://github.com/jax79sg/artyins-saveservice/raw/master/images/SoftwareArchitectureSaveService.jpg)]()

# Save For artyins deployment architecture
This is a submodule for the artyins deployment architecture. Please refer to [main module](https://github.com/jax79sg/artyins) for full build details.

[![Build Status](https://travis-ci.com/jax79sg/artyins-saveservice.svg?branch=master)](https://travis-ci.com/jax79sg/artyins-saveservice)

Refer to [Trello Task list](https://trello.com/c/x7u3MPQX) for running tasks.

---

## Table of Contents

- [Usage](#Usage)
- [Virtualenv](#Virtualenv)
- [Tests](#Tests)

---

## Usage
The save service can be called by a HTTP POST call. Primarily on http://webserverip:port/save_reports, http://webserverip:port/save_ingests and http://webserverip:port/updateingests. It expects a json of the following formats.

```python
```
### config.py
The configuration file will indicate the save class to use. For testing purposes, the mysql-connector-python library is used. 
```python

```

### Abstract Saver Class
All implementations of savers must implement this abstract class.
savers/save.py
```python

```

### An example on how to implement the Abstract Saver class
```python

```

### Adding your Saver into Web Service
You will need to add your saver function into the Web Service (flask_app.py). Here is an example, you may simply add your functions.
```python

```
---

## Virtualenv
```shell
python3 -m venv venv
source venv/bin/activate
pip install --user -r requirements.txt`
```
---

## Tests 
This repository is linked to [Travis CI/CD](https://travis-ci.com/jax79sg/artyins-saveservice). You are required to write the necessary unit tests if you introduce more Saver classes.
### Unit Tests
```python
```

### Web Service Test
```
#Start gunicorn wsgi server
gunicorn --bind 0.0.0.0:9898 --daemon --workers 10 wsgi:app
```
### Send test POST request
```python
```

---

