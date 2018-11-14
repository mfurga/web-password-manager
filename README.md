# Web Password Manager 
> Simple web password manager implemented using [Django Web Framework](https://www.djangoproject.com/).

[![Build Status](https://travis-ci.org/mfurga/chip8.svg?branch=master)](https://travis-ci.org/mfurga/web-password-manager)
[![Python3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/django-2.1.3-green.svg)](https://www.djangoproject.com/)
[![License MIT](https://img.shields.io/badge/license-MIT-%237900CA.svg)](https://github.com/mfurga/web-password-manager/blob/master/LICENSE)

Demo: https://web-password-manager.herokuapp.com/

## Overview
Simple web-based password manager written using Django Web Framework & pycrypto library. Allows to create a new entry, edit the entry, delete the entry and share the entry using a special URL, which is valid only for 5 minutes. It also uses the AES algorithm to deal with passwords storage in the database.

![Manager Image](https://raw.githubusercontent.com/mfurga/web-password-manager/master/demo.png)

## User credentials
**NOTE:** There is only one account that you can log in using the following credentials:
* **login**: root
* **password**: qwerty123

## Installation / Requirements

- [Django 2.1.3](https://www.djangoproject.com/)
- [Python 3.7](https://www.python.org/downloads/)
- [Pycrypto 2.6.x](https://pypi.org/project/pycrypto/)

You can also easly install the require packages using the following command:
```
pip install -r requirements.txt
```
Then run the server:
```
export SECRET_KEY="<secret here>"  # use `set` command for Windows
python manage.py runserver 0.0.0.0:8000
```

Done! 😊

## License
MIT © Mateusz Furga