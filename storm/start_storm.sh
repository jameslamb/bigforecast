#!/bin/sh

# Copy over config
cp -f $HOME/bigforecast/storm/storm.yaml $HOME/bin/apache-storm-1.1.0/conf/storm.yaml

# Submit the GDELT ingestion topology
cd $HOME/bigforecast/storm && \
    sparse submit --environment prod --name gdelt_ingestion

# References:
# [1] storm.apache.org/releases/1.0.3/Setting-up-a-Storm-cluster.html
# [2] www.michael-noll.com/tutorials/running-multi-node-storm-cluster