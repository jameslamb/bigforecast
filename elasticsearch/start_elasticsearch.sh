#!/bin/sh

# Copy over config
cp -f $HOME/bigforecast/elasticsearch/elasticsearch.yml $HOME/bin/elasticsearch-5.5.1/config/

# TODO (jaylamb20@gmail.com):
# parameterize the version number to be read
# off environment variables
cd $HOME/bin/elasticsearch-5.5.1/bin && \
    ./elasticsearch