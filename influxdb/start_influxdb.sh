#!/bin/sh

# Copy over configuraiton
cp $HOME/bigforecast/influxdb/influxdb.conf $INFLUXDB_CONFIG_PATH
 
# Start it up
sudo systemctl start influxdb