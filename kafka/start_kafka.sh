#!/bin/sh

#
# Start Zookeeper and Kafka Server
# Expects KAFKA_HOME to be passed in the environment
#

if [ "$KAFKA_HOME" = "" ]
then
    echo "Please set KAFKA_HOME"
    exit 1
fi

echo "Running kafka from $KAFKA_HOME"
cd $KAFKA_HOME

#
# Start Zookeeper
#
if [ -f "bin/zookeeper-server-start.sh" ]
then
    ./bin/zookeeper-server-start.sh config/zookeeper.properties &
    sleep 5
fi

if [ -f "bin/kafka-server-start.sh" ]
then
    ./bin/kafka-server-start.sh config/server.properties &
fi
