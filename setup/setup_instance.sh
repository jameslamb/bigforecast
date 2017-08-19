#!/bin/bash

# Break immediately if anything fails
set -e

# Create a `/bin` dir at home
if [ ! -d "$HOME/bin" ]; then
  mkdir $HOME/bin
fi

######################################
## Mount the attached storage drive ##
######################################
    
    # Softlayer handles mounting the first big drive we attached
    # at "/", so we don't need to do anything special.
    # Creating the "/data" dir here, as we'll reuse that in application
    # configs e.g. to redirect logs.
    # If you want to check what is mounted where, you can run:
    # 
    # fdisk -l
    # findmnt
    sudo mkdir /data

    # References:
    # [1] https://docs.oracle.com/cloud/latest/computecs_common/OCSUG/GUID-7393768A-A147-444D-9D91-A56550604EE5.htm#OCSUG196

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
    git checkout dev && \
    cd $HOME
    echo "Completed fetching application code from GitHub."


#############################
## Misc. system components ##
#############################

    echo "Installing gcc, openssl, and libffi-devel..."
    sudo yum install -y \
        bzip2 \
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
    cd $HOME/bin && \
    wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-${ES_VERSION}.rpm && \
    sudo rpm --install elasticsearch-${ES_VERSION}.rpm && \
    cd $HOME
    echo "Completed installation of Elasticsearch."

    # Configure system to ES starts automatically on boot (useful if we have to restart)
    echo "Registering Elasticsearch so it will start on boot..."
    sudo systemctl daemon-reload
    sudo systemctl enable elasticsearch.service
    echo "Done registering Elasticseacrh."

    # Copy over config
    echo "Replacing default configurations with our own..."
    cp -f $HOME/bigforecast/elasticsearch/elasticsearch.yml /etc/elasticsearch/elasticsearch.yml
    cp -f $HOME/bigforecast/elasticsearch/jvm.options /etc/elasticsearch/jvm.options
    sudo systemctl daemon-reload
    echo "Done configuring Elasticsearch."

    # Create directories for ES to write data to (shouold be consistent with elasticsearch.yml)
    sudo mkdir -p /data/elasticsearch/data
    sudo mkdir -p /data/elasticsearch/logs

    # References:
    # [1] https://www.elastic.co/guide/en/elasticsearch/reference/current/rpm.html#install-rpm
    # [2] https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-elasticsearch-on-centos-7
    # [3] https://www.elastic.co/guide/en/elasticsearch/reference/current/heap-size.html

######################
## conda + Python 3 ##
######################

if ! type "conda" &> /dev/null; then

    echo "Installing conda..."

    # grab lein install source
    export CONDA_SCRIPT="https://repo.continuum.io/archive/Anaconda3-4.3.1-Linux-x86_64.sh"
    curl ${CONDA_SCRIPT} > $HOME/install_conda.sh

    # Make it executable
    chmod a+rwx $HOME/install_conda.sh && \
    cd $HOME && \
    ./install_conda.sh -b -p $HOME/bin/anaconda3 && \
    rm $HOME/install_conda.sh

    # Install python proper
    sudo yum install -y python-devel

    # References:
    echo "Completed installation of Python and conda."
fi

######################
### Jupyter Server ###
######################

# Create Directory
if [ ! -d "~/.jupyter"]; then
    mkdir ~/.jupyter
fi

# Move files
echo "Setting up Jupyter Notebook web connections"
cd $HOME/bigforecast/setup &&  \
    mv jupyter/mycert.pem ~/.jupyter/mycert.pem &&   \
    mv jupyter/jupyter_notebook_config.py ~/.jupyter/jupyter_notebook_config.py &&  \
    cd $HOME

echo "Completed Setting up Jupyter Notebook web connections"

# References
# [1] https://chrisalbon.com/jupyter/run_project_jupyter_on_amazon_ec2.html


####################
#### leiningren ####
####################

# NOTE: This is needed for Storm    
if ! type "lein" &> /dev/null; then

    echo "Installing leiningren..."

    # grab lein install source
    export LEIN_URL="https://raw.githubusercontent.com/technomancy/leiningen/stable/bin/lein"
    cd $HOME && \
    curl ${LEIN_URL} > $HOME/bin/lein

    # Bypass warning about running lein as root
    echo "LEIN_ROOT=TRUE" >> /etc/profile
    source /etc/profile
    export LEIN_ROOT=TRUE

    # Make it executable and install it
    cd $HOME/bin && \
    chmod a+rwx lein && \
    ./lein && \
    cd $HOME

    # References:
    # [1] https://leiningen.org/#install
    # [2] https://stackoverflow.com/questions/41517353/where-to-set-lein-root
    echo "Completed installation of leiningren."
fi

###################
#### Zookeeper ####
###################

if ! type "zookeeper" &> /dev/null; then

    echo "Installing zookeeper..."

    # Add Cloudera yum library
    sudo yum install -y https://archive.cloudera.com/cdh5/one-click-install/redhat/7/x86_64/cloudera-cdh-5-0.x86_64.rpm
    sudo yum install -y \
        zookeeper \
        zookeeper-server

    # References
    # [1] https://stackoverflow.com/questions/41611275/how-to-install-zookeeper-as-service-on-centos-7
    # [2] https://www.cloudera.com/documentation/enterprise/5-9-x/topics/cdh_ig_cdh5_install.html
fi


######################
#### Apache Storm ####
######################

if ! type "storm" &> /dev/null; then

    echo "Installing Apache Storm...."

    # Download storm
    export STORMZIP="http://www-us.apache.org/dist/storm/apache-storm-1.1.0/apache-storm-1.1.0.tar.gz"
    cd $HOME/bin && \
    wget $STORMZIP -O apache-storm-1.1.0.tar.gz && \
    tar -zxf apache-storm-1.1.0.tar.gz && \
    mkdir $HOME/bin/apache-storm-1.1.0/data && \
    rm -rf apache-storm-1.1.0.tar.gz

    # Add directories for Storm data and logs
    sudo mkdir -p /data/storm/data
    sudo mkdir -p /data/storm/logs

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
    export KAFKAZIP="http://www-eu.apache.org/dist/kafka/0.10.1.1/kafka_2.10-0.10.1.1.tgz"
    cd $HOME/bin && \
    wget ${KAFKAZIP} -O kafka_2.10-0.10.1.1.tgz && \
    tar -zxf kafka_2.10-0.10.1.1.tgz && \
    rm -rf kafka_2.10-0.10.1.1.tgz

    # Create KAFKA_HOME variable
    echo "export KAFKA_HOME=$HOME/bin/kafka_2.10-0.10.1.1" >> ~/.bashrc

    # Add directories for Kafka data and logs
    sudo mkdir -p /data/kafka/data
    sudo mkdir -p /data/kafka/logs

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
    export CONDA_BIN="${HOME}/bin/anaconda3/bin"
    export ACTIVATE_ALIAS="${CONDA_BIN}/activate"
    export DEACTIVATE_ALIAS="${CONDA_BIN}/deactivate"
    export CONDA_ENV_ALIAS="${CONDA_BIN}/conda-env"

    # If you dont't do this, system Python (which is 2.7) will get used
    export CONDA_PYTHON="${CONDA_BIN}/python"

    # Create bigforecast conda environment
    cd $HOME/bigforecast/python && \
    $CONDA_ENV_ALIAS create -n bigforecast -f bigforecast.yml && \
    sudo $CONDA_PYTHON setup.py install
    
    # Install bigforecast python package into that environment
    cd $HOME/bigforecast/python && \
    source $ACTIVATE_ALIAS bigforecast && \
    sudo $CONDA_PYTHON setup.py install && \
    source $DEACTIVATE_ALIAS

    # Add bigforecast package to PYTHONPATH to be super sure
    echo "export PYTHONPATH=$HOME/bigforecast/python:$PYTHONPATH" >> ~/.bashrc


##############
## InfluxDB ##
##############
    
    # Install influxDB
    sudo yum install -y influxdb

    # Overwrite the default configs
    cp -f $HOME/bigforecast/influxdb/influxdb.repo /etc/yum.repos.d/influxdb.repo && \
    cp -f $HOME/bigforecast/influxdb/influxdb.conf /etc/influxdb/influxdb.conf

    # Configure Influx for automatic startup
    sudo systemctl daemon-reload
    sudo systemctl enable influxdb.service

    # setup that config path
    echo "export INFLUXDB_CONFIG_PATH=/etc/influxdb/influxdb.conf" >> ~/.bashrc
    source ~/.bashrc

    # Add directories for InfluxDB data and logs
    sudo mkdir -p /data/influx/data
    sudo mkdir -p /data/influx/logs

    # References
    # [1] https://docs.influxdata.com/influxdb/v1.3/introduction/installation


###########################
## Environment variables ##
###########################

# Setup path
echo "export PATH=$HOME/bin/anaconda3/bin:$PATH:$HOME/bin:$HOME/bin/apache-storm-1.1.0/bin:$HOME/bin/kafka_2.10-0.10.1.1.tgz/bin" >> ~/.bashrc

# Set bigforecast home directory
if [[ ! -d "$BIGFORECAST_HOME" ]]; then
    export BIGFORECAST_HOME="$HOME/bigforecast"
    echo 'export BIGFORECAST_HOME="$HOME/bigforecast"' >> ~/.bashrc
fi

######################
## Other references ##
######################

# [1] https://stackoverflow.com/questions/1158091/defining-a-variable-with-or-without-export

