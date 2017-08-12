cd $HOME/bin/kafka_2.10-0.10.1.1
bin/zookeeper-server-start.sh config/zookeeper.properties &
bin/kafka-server-start.sh config/server.properties &

