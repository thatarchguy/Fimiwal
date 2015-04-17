"""
Class for handling scanning
"""

from fimiwal import models, db, app
import sys
import datetime
import time
import select
import paramiko


class ScanClass:
    def __init__(self, client):
        self.client = client

    def force_scan_linux(self):
        client = self.client
        app.logger.info("Initiating scan for: " + str(client.ident))
        # Initiate scan
        self.linux_ssh()

    def linux_ssh(self, command="diff"):
        client = self.client
        host = str(client.ip)
        i = 1

        #
        # Try to connect to the host.
        # Retry a few times if it fails.
        #
        while True:
            print "Trying to connect to %s (%i/30)" % (host, i)

            try:
                ssh = paramiko.SSHClient()
                ssh.load_system_host_keys()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(host, username="fimiwal")
                print "Connected to %s" % host
                break
            except paramiko.AuthenticationException:
                print "Authentication failed when connecting to %s" % host
                sys.exit(1)
            except:
                print "Could not SSH to %s, waiting for it to start" % host
                i += 1
                time.sleep(2)

            # If we could not connect within time limit
            if i == 30:
                print "Could not connect to %s. Giving up" % host
                sys.exit(1)

        # Send the command (non-blocking)
        stdin, stdout, stderr = ssh.exec_command(
            "cd " + client.directory + "; git " + command)
        stderr_data = stderr.read()
        if stderr_data:
            print stderr_data
            print "error: not in git repo"
            return "error: not in git repo"
        # Wait for the command to terminate
        self.process(stdout.read())

        #
        # Disconnect from the host
        #
        print "Command done, closing SSH connection"
        ssh.close()

    def process(self, data):
        client = self.client
        if "nothing to commit, working directory clean" in data:
            app.logger.info("Scan results: " + client.ident + " - Clean")
            print "Super duper"
            newScan = models.Scans(
                client_id=client.id,
                date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                status="0",
                data=data)
            db.session.add(newScan)
            db.session.commit()
        elif "diff --git" in data:
            app.logger.info("Scan results: " + client.ident + " - Diff")
            newScan = models.Scans(
                client_id=client.id,
                date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                status="1",
                data=data)
            db.session.add(newScan)
            db.session.commit()
        elif "Untracked files:" in data:
            app.logger.info("Scan results: " + client.ident + " - New File(s)")
            newScan = models.Scans(
                client_id=client.id,
                date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                status="2",
                data=data)
            db.session.add(newScan)
            db.session.commit()
        elif "Changes to be committed" in data:
            app.logger.info("Scan results: " + client.ident + " - Staged")
            newScan = models.Scans(
                client_id=client.id,
                date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                status="3",
                data=data)
            db.session.add(newScan)
            db.session.commit()
        elif len(data) == 0:
            # If diff comes back clean, there may still be new files 
            # added that we need to check for
            print "diff clean, running status"
            self.linux_ssh(command="status")
        else:
            print "idk mang"
            app.logger.info(
                "Scan results: " + client.ident + " - Unknown Error")
