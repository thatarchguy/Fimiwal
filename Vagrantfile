# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = "vtemian/trusty64-python"

   # Application provision
  config.vm.provision :shell, :inline => "cd /vagrant && pip install -r requirements.txt && python run.py"

   # networking
  config.vm.network :forwarded_port, host: 5000, guest: 5000
end
