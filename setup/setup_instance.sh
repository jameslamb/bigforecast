#!/bin/bash

# Break immediately if anything fails
set -e

# Create a `/bin` dir at home
if [ ! -d "$HOME/bin" ]; then
  mkdir $HOME/bin
fi

#### Install Git ####
if ! type "git" &> /dev/null; then
    
    echo "Installing Git..."

    # Install Git
    sudo yum install -y git-all

    # References:
    # [1] https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
    echo "Completed installation of Git"
fi

#### Get project source code ####

    # Get the source code
    echo "Fetching application code from GitHub..."
    cd $HOME && \
    git clone https://github.com/jameslamb/bigforecast && \
    cd bigforecast && \
    git fetch origin dev && \
    git checkout dev
    echo "Completed fetching application code from GitHub."

#### Install misc. system components ####

    echo "Installing gcc, openssl, and libffi-devel..."
    sudo yum install -y gcc-c++
    sudo yum install -y openssl-devel
    sudo yum install -y libffi-devel
    sudo yum install -y bzip2
    echo "Completed installation of miscellanous system components."

#### Install conda + Anaconda Python 2.7 ####

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

#### Install lein ####

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

#### Install Apache Storm ####

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

#### Install kafka ####

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

#### Install python package and conda env ####

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

# Setup path
echo "export PATH=$HOME/anaconda3/bin:$PATH:$HOME/bin:$HOME/bin/apache-storm-1.1.0/bin:$HOME/bin/kafka_2.10-0.10.1.1.tgz/bin" >> ~/.bashrc


# Set bigforecast home directory
if [[ ! -d "$BIGFORECAST_HOME" ]]; then
    export BIGFORECAST_HOME="$HOME/bigforecast"
    echo 'export BIGFORECAST_HOME="$HOME/bigforecast"' >> ~/.bashrc
fi
