"""
class for handling client functions
"""
from fimiwal import models, db, app
from shutil import move
import os
import datetime
import subprocess

GITOLITE_DIR = "/home/git/.gitolite/"


def update_gitolite():
    subprocess.call(["gitolite", "compile"])
    subprocess.call(["gitolite", "trigger POST_COMPILE"])

    return True


class ClientClass:
    def __init__(self, client):
        self.client = client

    def add_client(self):
        client = self.client
        app.logger.info("Adding client to gitolite: " + str(client.ident))
        # Add the client's keys to the keydir
        keydir = open(GITOLITE_DIR + "keydir/" + client.ident + ".pub", 'w+')
        keydir.write(client.ssh)

        # Add permissions to the gitolite.conf
        with open(GITOLITE_DIR + "conf/gitolite.conf", "a") as conf:
            conf.write(
                "\nrepo " + client.ident + "\n    RW+    =    " + client.ident)

    def repo_write(self):
        client = self.client
        app.logger.info("Changing perms to write for: " + str(client.ident))
        # Parse the file, change the perms
        with open(GITOLITE_DIR + "conf/gitolite.conf") as oldconf, open(
            GITOLITE_DIR + "conf/gitolite.new.conf", 'w') as newconf:
            for line in oldconf:
                if not client.ident in line:
                    newconf.write(line)
            newconf.write(
                "repo " + client.ident + "\n    RW+    =    " + client.ident)
        move(GITOLITE_DIR + "conf/gitolite.new.conf",
             GITOLITE_DIR + "conf/gitolite.conf")
        update_gitolite()

    def repo_read(self):
        client = self.client
        app.logger.info("Changing perms to read for: " + str(client.ident))
        # Parse the file, change the perms
        with open(GITOLITE_DIR + "conf/gitolite.conf") as oldconf, open(
            GITOLITE_DIR + "conf/gitolite.new.conf", 'w') as newconf:
            for line in oldconf:
                if not client.ident in line:
                    newconf.write(line)
            newconf.write(
                "repo " + client.ident + "\n    R    =    " + client.ident)
        move(GITOLITE_DIR + "conf/gitolite.new.conf",
             GITOLITE_DIR + "conf/gitolite.conf")
        update_gitolite()

    def delete_client(self):
        client = self.client
        # Parse file for client data
        with open(GITOLITE_DIR + "conf/gitolite.conf") as oldconf, open(
            GITOLITE_DIR + "conf/gitolite.new.conf", 'w') as newconf:
            for line in oldconf:
                if not client.ident in line:
                    newconf.write(line)
        move(GITOLITE_DIR + "conf/gitolite.new.conf",
             GITOLITE_DIR + "conf/gitolite.conf")

        # Delete SSH key
        os.remove(GITOLITE_DIR + "keydir/" + client.ident + ".pub")

        update_gitolite()

        app.logger.info("Deleting: " + str(client.id))
        # Delete scans and set client inactive
        scans = models.Scans.query.filter_by(client_id=self.client.id)
        for scan in scans:
            db.session.delete(scan)

        self.client.active = False
        client.date_rm = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.session.add(client)
        db.session.commit()
        app.logger.info("Deleted client: " + str(client.id))

        return True
