#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_fimiwal
----------------------------------

Tests for `fimiwal` module.
"""

from urllib.request import urlopen
import datetime
from flask import Flask
from flask.ext.testing import LiveServerTestCase
from fimiwal import app, db, models
import config


class Testfimiwal(LiveServerTestCase):

    TESTING = app.config['TESTING']

    def create_app(self):
        app.config.from_object('config.TestConfiguration')
        SQLALCHEMY_DATABASE_URI = app.config['SQLALCHEMY_DATABASE_URI']
        print(SQLALCHEMY_DATABASE_URI)

        return app

    def setUp(self):
        print("CREATING DB")
        db.create_all()
        db.session.commit()

    def tearDown(self):
        print("TEARING DOWN!")
        db.session.remove()
        db.drop_all()

    def test_server_is_up_and_running(self):
        #u = models.Clients(name="testClient", date_added=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        #db.session.add(u)
        #db.session.commit()
        print("DATA ADDED!")

        print("QUERYING DATABASE")
        #clientID = models.Clients.query.filter_by(name="testClient").one().id
        #print clientID

        response = urlopen(self.get_server_url() + "/login")
        self.assertEqual(response.code, 200)
