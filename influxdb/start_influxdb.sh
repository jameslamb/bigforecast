#!/bin/sh

# Copy over configuraiton
cp -f $HOME/bigforecast/influxdb/influxdb.conf $INFLUXDB_CONFIG_PATH
 
# Start it up
sudo systemctl start influxdb