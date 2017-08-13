#!/bin/bash

# Break immediately if anything fails
set -e

# Create a `/bin` dir at home
if [ ! -d "$HOME/bin" ]; then
  mkdir $HOME/bin
fi


#########
## Git ##
#########

if ! type "git" &> /dev/null; then
    
    echo "Installing Git..."

    # Install Git
    sudo yum install -y git-all

    # References:
    # [1] https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
    echo "Completed installation of Git"
fi


#########################
## Project source code ##
#########################

    # Get the source code
    echo "Fetching application code from GitHub..."
    cd $HOME && \
    git clone https://github.com/jameslamb/bigforecast && \
    cd bigforecast && \
    git fetch origin dev && \
    git checkout dev
    echo "Completed fetching application code from GitHub."


#############################
## Misc. system components ##
#############################

    echo "Installing gcc, openssl, and libffi-devel..."
    sudo yum install -y \
        bzip2
        gcc-c++ \
        libffi-devel \
        openssl-devel \
        
    echo "Completed installation of miscellanous system components."


###################
## Java (for ES) ##
###################

    echo "Installing Java...."
    sudo yum install -y \
        java-1.8.0-openjdk.x86_64

    echo "Completed installation of Java."


###################
## Elasticsearch ##
###################

    echo "Installing Elasticsearch..."

    # Download ES 
    export ES_VERSION=5.5.1
    cd $HOME/bin
    curl -L -O https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-${ES_VERSION}.tar.gz
    tar -xvf elasticsearch-${ES_VERSION}.tar.gz


######################
## conda + Python 3 ##
######################

if ! type "conda" &> /dev/null; then

    echo "Installing conda..."

    # grab lein install source
    CONDA_SCRIPT="https://repo.continuum.io/archive/Anaconda3-4.3.1-Linux-x86_64.sh"
    curl $CONDA_SCRIPT > $HOME/install_conda.sh

    # Make it executable
    chmod a+rwx $HOME/install_conda.sh
    cd $HOME
    ./install_conda.sh

    # References:
    # [1] https://leiningen.org/#install
    echo "Completed installation of conda."
fi


####################
#### leiningren ####
####################

# NOTE: This is needed for Storm    
if ! type "lein" &> /dev/null; then

    echo "Installing leiningren..."

    # grab lein install source
    curl https://raw.githubusercontent.com/technomancy/leiningen/stable/bin/lein > $HOME/bin/lein

    # Make it executable
    chmod a+rwx $HOME/bin/lein
    cd $HOME/bin
    ./lein

    # References:
    # [1] https://leiningen.org/#install
    echo "Completed installation of leiningren."
fi


######################
#### Apache Storm ####
######################

if ! type "storm" &> /dev/null; then

    echo "Installing Apache Storm...."

    # Download storm
    cd $HOME/bin
    STORMZIP="http://www-us.apache.org/dist/storm/apache-storm-1.1.0/apache-storm-1.1.0.tar.gz"
    wget $STORMZIP -O apache-storm-1.1.0.tar.gz
    tar -zxf apache-storm-1.1.0.tar.gz
    mkdir $HOME/bin/apache-storm-1.1.0/data

    # Replace the storm config file with our custom config
    echo "Replacing the Storm config with custom version..."
    cp $HOME/bigforecast/setup/storm.yaml $HOME/bin/apache-storm-1.1.0/conf/storm.yaml

    # References:
    # [1] https://www.tutorialspoint.com/apache_storm/apache_storm_installation.html
    # [2] http://www.apache.org/dyn/closer.lua/storm/apache-storm-1.1.0/apache-storm-1.1.0.tar.gz
    echo "Completed installation of Apache Storm."

fi


##################
## Apache Kafka ##
##################

if [ -z ${KAFKA_HOME+x} ]; then
    echo "Installing Apache Kafka..."

    # Download Kafka
    cd $HOME/bin
    KAFKAZIP="http://www-eu.apache.org/dist/kafka/0.10.1.1/kafka_2.10-0.10.1.1.tgz"
    wget $KAFKAZIP -O kafka_2.10-0.10.1.1.tgz
    tar -zxf kafka_2.10-0.10.1.1.tgz

    # Create KAFKA_HOME variable
    echo "export KAFKA_HOME=$HOME/bin/kafka_2.10-0.10.1.1" >> ~/.bashrc

    # References:
    # [1] http://stackoverflow.com/questions/3601515/how-to-check-if-a-variable-is-set-in-
    # [2] https://www.tutorialspoint.com/apache_kafka/apache_kafka_installation_steps.htm
    echo "Completed installation of Apache Kafka."
else 
    echo "Apache Kafka is already installed! KAFKA_HOME is set to '$KAFKA_HOME'";
fi


#######################################
## project Python package, conda env ##
#######################################

    # Set up variables (since Anaconda isn't on our path yet)
    CONDA_BIN="$HOME/anaconda3/bin"
    ACTIVATE_ALIAS="$CONDA_BIN/activate"
    DEACTIVATE_ALIAS="$CONDA_BIN/deactivate"
    CONDA_ENV_ALIAS="$CONDA_BIN/conda-env"

    # Create bigforecast conda environment
    cd $HOME/bigforecast/python && \
    $CONDA_ENV_ALIAS create -n bigforecast -f bigforecast.yml && \
    sudo python setup.py install
    
    # Install bigforecast python package into that environment
    cd $HOME/bigforecast/python && \
    source $ACTIVATE_ALIAS bigforecast && \
    sudo python setup.py install && \
    source $DEACTIVATE_ALIAS bigforecast

    # Add bigforecast package to PYTHONPATH to be super sure
    echo "export PYTHONPATH=$HOME/bigforecast/python:$PYTHONPATH" >> ~/.bashrc


##############
## InfluxDB ##
##############

    # Download and install influxDB
    export INFLUX_VERSION=1.3.1
    wget https://dl.influxdata.com/influxdb/releases/influxdb_${INFLUX_VERSION}_amd64.deb
    sudo dpkg -i influxdb_${INFLUX_VERSION}_amd64.deb

    # setup that config path
    echo "export INFLUXDB_CONFIG_PATH=/etc/influxdb/influxdb.conf" >> ~/.bashrc
    source ~/.bashrc

    ## TODO (jaylamb20@gmail.com)
    # Fix the http part of the config to allow all members of the cluster
    # to write here


###########################
## Environment variables ##
###########################

# Setup path
echo "export PATH=$HOME/anaconda3/bin:$PATH:$HOME/bin:$HOME/bin/apache-storm-1.1.0/bin:$HOME/bin/kafka_2.10-0.10.1.1.tgz/bin" >> ~/.bashrc

# Set bigforecast home directory
if [[ ! -d "$BIGFORECAST_HOME" ]]; then
    export BIGFORECAST_HOME="$HOME/bigforecast"
    echo 'export BIGFORECAST_HOME="$HOME/bigforecast"' >> ~/.bashrc
fi
