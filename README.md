##FIMIWAL [![Build Status](https://travis-ci.org/thatarchguy/Fimiwal.svg)](https://travis-ci.org/thatarchguy/Fimiwal) [![Stories in Ready](https://badge.waffle.io/thatarchguy/Fimiwal.svg?label=ready&title=Ready)](http://waffle.io/thatarchguy/Fimiwal) 

Git content file integrity solution for hosts. 
Runs on python2.7

Currently uses gitolite on the backend for the git repositories.
http://gitolite.com/gitolite/gitolite.html#server-side-admin


## Installation
---
```    
pip install -r requirements.txt
# Create the sqlite database
python manage.py createdb
#OR
python manage.py db init
python manage.py db migrate
python manage.py db upgrade

# Run the program in server mode
python manage.py runserver --host=0.0.0.0

# or

# Run a python shell in the program's context
python manage.py shell
```

Vagrant and Dockerfiles are supplied also.

## Clients
----
### Linux

By default, fimiwal tries to login through ssh as fimiwal. 
In a default setup, the server's user would be the git user for simplicity's sake.

Add the server's user ssh public key to the client's fimiwal user authorized_keys. 
Make sure this user has permissions to the repo.



## Contributing

See the CONTRIBUTING.md page
