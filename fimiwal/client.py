"""
class for handling client functions
"""
from fimiwal import models, db
from shutil import move

GITOLITE_DIR = "/home/git/.gitolite/"


class ClientClass:
    def __init__(self, client):
        self.client = client


    def add_client(self):
        client = self.client
        # Add the client's keys to the keydir
        keydir = open(GITOLITE_DIR + "keydir/" + client.ident + ".pub", 'w+')
        keydir.write(client.ssh)

        # Add permissions to the gitolite.conf
        with open(GITOLITE_DIR + "conf/gitolite.conf", "a") as conf:
            conf.write("repo " + client.ident + "\n    RW+    =    " + client.ident)


    def repo_write(self):
        client = self.client
        # Parse the file, change the perms
        with open(GITOLITE_DIR + "conf/gitolite.conf") as oldconf, open(GITOLITE_DIR + "conf/gitolite.new.conf", 'w') as newconf:
            for line in oldconf:
                if not client.ident in line:
                    newconf.write(line)
            newconf.write("repo " + client.ident + "\n    RW+    =    " + client.ident)
        move(GITOLITE_DIR + "conf/gitolite.new.conf", GITOLITE_DIR + "conf/gitolite.conf")
        

    def repo_read(self):
        client = self.client
        # Parse the file, change the perms
        with open(GITOLITE_DIR + "conf/gitolite.conf") as oldconf, open(GITOLITE_DIR + "conf/gitolite.new.conf", 'w') as newconf:
            for line in oldconf:
                if not client.ident in line:
                    newconf.write(line)
            newconf.write("repo " + client.ident + "\n    R    =    " + client.ident)
        move(GITOLITE_DIR + "conf/gitolite.new.conf", GITOLITE_DIR + "conf/gitolite.conf")
