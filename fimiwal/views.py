from flask import render_template, request, flash, redirect, url_for
from flask.ext.login import login_user, logout_user, current_user, login_required
from fimiwal import app, db, models, login_manager, bcrypt
from .forms import SettingsPass, SettingsGeneral, AddClient
from dateutil.relativedelta import relativedelta
import os
import datetime
import time
import subprocess
import re
import json
import socket


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login?next=' + request.path)


@login_manager.user_loader
def load_user(id):
    return models.Users.query.get(int(id))


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.route('/')
@app.route('/index')
@app.route('/index.html')
@login_required
def index_view():
    clientCount = models.Clients.query.filter_by(active=True).count()
    return render_template('index.html',
                           title="Dashboard",
                           clientCount=clientCount)


@app.route('/login', methods=['GET', 'POST'])
def login_view():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form['username']
    password = request.form['password']
    remember_me = False
    if 'remember_me' in request.form:
        remember_me = True
    registered_user = models.Users.query.filter_by(username=username).first()
    if registered_user and bcrypt.check_password_hash(registered_user.password,
                                                      password):
        login_user(registered_user, remember=remember_me)
        flash('%s logged in successfully' % username)
        return redirect(request.args.get('next') or url_for('index_view'))
    flash('Username or Password is invalid', 'error')
    return redirect(url_for('login_view'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_view'))


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings_view():
    error = None
    user = current_user
    GeneralForm = SettingsGeneral(email=user.email)
    ChangePassForm = SettingsPass()
    if GeneralForm.validate_on_submit():
        email = request.form['email']
        user.email = email
        db.session.add(user)
        db.session.commit()
        app.logger.info("Changed email for: " + user.username)
        flash('Email successfully changed')
        return redirect('/settings')
    if ChangePassForm.validate_on_submit():
        currentPass = request.form['currentPass']
        if bcrypt.check_password_hash(user.password, currentPass):
            newPass = bcrypt.generate_password_hash(request.form['newPass'])
            user.password = newPass
            db.session.add(user)
            db.session.commit()
            app.logger.info("Changed password for: " + user.username)
            flash('Password successfully changed')
            return redirect('/settings')
        else:
            error = "Current password was incorrect"
    return render_template('settings.html',
                           title="Settings",
                           ChangePassForm=ChangePassForm,
                           GeneralForm=GeneralForm,
                           error=error)


@app.route('/clients')
@login_required
def clients_view():
    clients = models.Clients.query.filter_by(active=True).all()
    return render_template('clients.html', title="Clients", entries=clients)


@app.route('/clients/add', methods=['POST', 'GET'])
@login_required
def client_add():
    error = None
    AddClientForm = AddClient()

    if AddClientForm.validate_on_submit():
        if models.Clients.query.filter_by(
            email=AddClientForm.email.data).first() is None:
            newClient = models.Clients(email=AddClientForm.email.data,
                                       date_added=datetime.datetime.now(
                                       ).strftime("%Y-%m-%d %H:%M:%S"),
                                       ident=AddClientForm.ident.data,
                                       os=AddClientForm.os.data,
                                       ip=AddClientForm.ip.data,
                                       directory=AddClientForm.directory.data)
            db.session.add(newClient)
            db.session.commit()

            # Task to create git repo and add to gitolite

            return redirect(url_for('client_admin', client_id=newClient.id))
        else:
            error = "Client Name is already in use"

    return render_template('addclient.html',
                           title='Add Client',
                           AddClientForm=AddClientForm,
                           error=error)


@app.route('/client/<int:client_id>/admin/')
@login_required
def client_admin(client_id):
    client = models.Clients.query.get(client_id)
    return render_template('clientadmin.html',
                           title=client.ident,
                           client=client)
