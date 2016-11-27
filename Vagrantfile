# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|

  config.vm.box = "hashicorp/precise64"
  config.vm.synced_folder ".", "/vagrant", disabled: true


  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # config.vm.network "forwarded_port", guest: 80, host: 8080

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  # config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
  #   vb.memory = "1024"
  # end

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.

  config.vm.provision "shell", inline: <<-SHELL
   apt-get update
   apt-get install -y python
   apt-get install -y postgresql
   apt-get install -y postgresql-client
   apt-get install -y postgresql-contrib
   apt-get install -y python-pip
   apt-get install -y python-dev
   apt-get install -y build-essential
   apt-get install -y libpq-dev
   apt-get install -y git
   pip install psycopg2
   pip install flask
   pip install Flask-AutoIndex
   pip install flask-wtf
   mkdir /usr/novus-convert
   cd /usr/novus-convert
   git clone https://github.com/krubottom/novus-convert
  SHELL
end
