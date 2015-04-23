############################################################
# Dockerfile to build grrmanager
# Based on Ubuntu
############################################################

# Set the base image to Ubuntu
FROM ubuntu

# File Author / Maintainer
MAINTAINER Kevin Law

# Update the sources list
RUN apt-get update

# Install basic applications
RUN apt-get install -y build-essential net-tools git vim curl wget tar

# Install Python and Basic Python Tools
RUN apt-get install -y python python-dev python-distribute python-pip

# Copy the application folder inside the container
ADD . /Fimiwal

# Get pip to download and install requirements:
RUN pip install -r Fimiwal/requirements.txt

# Expose ports
EXPOSE 5000

# Set the default directory where CMD will execute
WORKDIR /Fimiwal

# Set the default command to execute    
# when creating a new container
# i.e. using CherryPy to serve the application
CMD python manage.py createdb && python manage.py runserver -h 0.0.0.0


