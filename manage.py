'''Management commands.'''

import os
from flask.ext.script import Manager
from fimiwal import app, db, models
from flask.ext.migrate import Migrate, MigrateCommand

manager = Manager(app)
app.config.from_object('config.BaseConfiguration')

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def install():
    '''Installs all required packages.'''
    os.system('pip install -U -r requirements.txt')


@manager.command
def createdb():
    '''Runs the db init, db migrate, db upgrade commands automatically'''
    os.system('python manage.py db init')
    os.system('python manage.py db migrate')
    os.system('python manage.py db upgrade')
    # Default creds, admin:fimiwal
    user = models.Users(
        'admin', '$2a$12$OtKZDr9Ax5cPh0ZAKXHbgOLJSxGOLh27BqtBAzD3Yg577NNi2XbSe',
        'admin@example.com')
    db.session.add(user)
    db.session.commit()


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, models=models)


@manager.command
def test():
    '''Runs the tests.'''
    command = 'nosetests --verbosity=2 --nocapture'
    os.system(command)


@manager.command
def lint():
    '''Lints the codebase'''
    command = 'flake8 --ignore E127,E221,F401 --max-line-length=220 --exclude=db_repository,tests,env,migrations .'
    os.system(command)


@manager.command
def clean():
    '''Cleans the codebase'''
    commands = ["find . -name '*.pyc' -exec rm -f {} \;",
                "find . -name '*.pyo' -exec rm -f {} \;",
                "find . -name '*~' -exec rm -f {} \;",
                "find . -name '__pycache__' -exec rmdir {} \;", "rm -f app.db",
                "rm -rf migrations", "rm -f fimiwal.log"]
    for command in commands:
        os.system(command)


if __name__ == "__main__":
    manager.run()
