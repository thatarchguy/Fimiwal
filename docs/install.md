## Install Fimiwal
In-depth tutorial
Requires python2.7, gitolite, and redis


### Server
----
Create an Ubuntu server. VPS, VM, barebones, etc...


#### Prerequisites
```
sudo apt-get update

sudo apt-get install git python-dev python-pip python-virtualenv redis-server

# If it didn't already create a git user
sudo adduser git

# Switch to git user
su - git

# Generate ssh keys
ssh-keygen -t rsa


```

#### Setup Gitolite

Taken from http://gitolite.com/gitolite/gitolite.html#server-side-admin

Run as git user:
```
# Clone gitolite
git clone git://github.com/sitaramc/gitolite

mkdir ~/bin

gitolite/install -ln ~/bin

# Add the gitolite binaries to our path
export PATH=/home/git/bin:$PATH

# Setup gitolite to not use the git repo as configuration
gitolite setup -a dummy
rm -rf ~/repositories/gitolite-admin.git

# delete gitolite admin repo from config
nano ~/.gitolite/conf/gitolite.conf

# Make a new key directory
mkdir ~/.gitolite/keydir

# Save changes to Gitolite
gitolite compile; gitolite trigger POST_COMPILE
```


#### Setup Fimiwal

Run as git user:
```
git clone git://github.com/thatarchguy/fimiwal.git

cd ~/fimiwal

# Make the virtualenv for python
virtualenv -p /usr/bin/python2.7 env
. env/bin/activate

# install fimiwal requirements
pip install -r requirements.txt

# Create database
python manage.py createdb

# Change IP address of server in config.py
nano config.py

# run the server
python manage.py runserver --host=0.0.0.0

# Run a worker process
# Do this in a separate window or tmux or however
# Make sure you activate the virtualenv in this as well
python worker.py

```

### Linux Client
----
Install ssh and git on the client

Create a user called fimiwal
```
adduser fimiwal
```

Copy the ssh key for the git user on the server into the fimiwal user's
authorized_keys file
```
nano /home/fimiwal/.ssh/authorized_keys
```

Create the repository for the files you want to keep track of!
```
git init
git add .
git commit -m "initial commit"
```

Add client to Fimiwal Server and push the repo to it
for baseline
```
git remote add origin git://[fimiwalserver]/[repo]
```


### Windows Client
----
Install git on the client

fimiwal uses winexe to login to the windows client

Save as install.ps1 and run it in powershell
```
#!/windows/system32
#Set services to start automatically
Set-Service LanmanWorkstation -StartupType "automatic"
Set-Service LanmanServer -StartupType "automatic"
#Enable file & printer sharing (port 139)
netsh advfirewall firewall set rule group="File and Printer Sharing" new enable=Yes
#Open browser window to Git install
[System.Diagnostics.Process]::Start("http://git-scm.com/download/win")
```

During git install, Select "Use git form the Windows Command Prompt"

and "Checkout Windows-Style, Commit Unix-style line endings"

Create the repository for the files you want to keep track of!
```
git init
git add .
git commit -m "initial commit"
```

Add client to Fimiwal Server and push the repo to it
for baseline
```
git remote add origin git://[fimiwalserver]/[repo]
```

