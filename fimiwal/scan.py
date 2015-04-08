"""
Class for handling scanning
"""

from fimiwal import models, db
import sys
import time
import select
import paramiko


def process(data):
    if "diff" in data:
        print "ALERT ALERT THERE'S DIFF"
    elif len(data) == 0:
       print "clean" 
    else:
        print "idk mang"

def linux_ssh(client):
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
            ssh.connect(host)
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
    stdin, stdout, stderr = ssh.exec_command("git diff")
    stderr_data = stderr.read()
    if stderr_data:
        print stderr_data
        print "error: not in git repo"
        return "error: not in git repo"
    # Wait for the command to terminate
    process(stdout.read())

    #
    # Disconnect from the host
    #
    print "Command done, closing SSH connection"
    ssh.close()



class ScanClass:

    def __init__(self, client):
        self.client = client


    def force_scan_linux(self):
        client = self.client
        # Initiate scan
        linux_ssh(client)
