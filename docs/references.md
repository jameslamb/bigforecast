
# References

This page is a dumping ground for links we found helpful throughout this process. Loosely organized by technology.

# Table of contents
1. [Elasticsearch](#introduction)
2. [InfluxDB](#influxdb)
3. [Kafka](#kafka)
4. [CentOS/Linux](#centos)
5. [Other](#other)
6. [Python/Jupyter/Conda](#python)
7. [Storm](#storm)
8. [Zookeeper](#zookeeper)

## Elasticsearch <a name="elasticsearch"></a>

1. [rpm installation of Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/rpm.html#install-rpm)
2. [How to Install and Configure Elasticsearch on CentOS 7](https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-elasticsearch-on-centos-7)
3. [Heap Size in Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/heap-size.html)
4. [Important Config Changes](https://www.elastic.co/guide/en/elasticsearch/guide/1.x/_important_configuration_changes.html)
5. [elasticsearch-head UI](https://github.com/mobz/elasticsearch-head)
6. [The 'date' datatype in Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/date.html)
7. [All  the different datetype formats in ES](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-date-format.html)

## InfluxDB <a name="influxdb"></a>

1. [Installing InfluxDB on CentOS 7](http://vmkdaily.ghost.io/influxdb-and-grafana-on-centos/)
2. [influxdb-python documentation](https://github.com/influxdata/influxdb-python)
3. [(forum) Starting InfluxDB on CentOS 7](https://community.influxdata.com/t/start-influxdb-service-in-centos-7/961)
4. [Fixing InfluxDB restart errors](https://eapyl.github.io/article/InfluxDB-cant-be-started-as-a-service-21-December-2016.html)
5. [Installing InfluxDB v1.3](https://docs.influxdata.com/influxdb/v1.3/introduction/installation)
6. [How timestamps work in InfluxDB](https://docs.influxdata.com/influxdb/v0.9/guides/writing_data/)
7. [Multi-Series Aggregate Queries](https://github.com/grafana/grafana/issues/3028)

## Kafka <a name="kafka"></a>

1. [Kafka installation](https://www.tutorialspoint.com/apache_kafka/apache_kafka_installation_steps.htm)
2. [Kafka Python package](https://github.com/dpkp/kafka-python)
3. [Blog post with a decent Kafka setup walkthrough](http://armourbear.blogspot.com/2015/03/setting-up-multinode-kafka-cluster.html)
4. [Kafka configuration explained](http://kafka.apache.org/090/documentation.html)
5. [Kafka-manager, a web UI for Kafka](https://github.com/yahoo/kafka-manager)
6. [Kafka in a nutshell](https://sookocheff.com/post/kafka/kafka-in-a-nutshell/)

## CentOS/Linux <a name="centos"></a>

1. [rpm installation](http://ftp.rpm.org/max-rpm/s1-rpm-install-additional-options.html)
2. [Mounting Drives at Specific Locations in a Filesystem](https://docs.oracle.com/cloud/latest/computecs_common/OCSUG/GUID-7393768A-A147-444D-9D91-A56550604EE5.htm#OCSUG196)
3. [Installing Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
4. [(forum) How to check if a variable is set in bash](http://stackoverflow.com/questions/3601515/how-to-check-if-a-variable-is-set-in-)
5. [(forum) Difference between defining variables with and without "export"](https://stackoverflow.com/questions/1158091/defining-a-variable-with-or-without-export)
6. [(forum) Avoiding output buffering using nohup and python](https://stackoverflow.com/questions/12919980/nohup-is-not-writing-log-to-output-file)

## Other <a name="other"></a>

1. [Stock Market Status API (check if a given market is open)](https://www.stockmarketclock.com/stock-market-api)
2. [Unix Epoch Convert (web calculator)](https://www.epochconverter.com/)
3. [The Currencies Most Affected by Falling Oil Prices](http://www.investopedia.com/articles/investing/102015/currencies-most-affected-falling-oil-prices.asp)
4. [In currency trading, what are the Commodity Pairs?](http://www.investopedia.com/ask/answers/09/commodity-pair.asp)
5. [The most-traded currency pairs](http://theessentialsoftrading.com/Blog/2011/07/27/most-traded-currency-pairs/)

## Python/Jupyter/Conda <a name="python"></a>

1. [Running Jupyter Server from a Cloud VM](https://chrisalbon.com/jupyter/run_project_jupyter_on_amazon_ec2.html)
2. [Getting Current Time in UTC](https://stackoverflow.com/questions/4548684/how-to-get-the-seconds-since-epoch-from-the-time-date-output-of-gmtime-in-py)
3. [yahoo-finance module](https://github.com/lukaszbanasiak/yahoo-finance)
4. [Dropping NAs in Pandas](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.dropna.html)
5. [About the Jupyter Project](http://jupyter.org/about.html)
6. [A curated list of insanely awesome libraries, packages and resources for Quants (Quantitative Finance)](https://github.com/wilsonfreitas/awesome-quant)
7. [Interpolating and Upsampling Timeseries Data with Pandas](http://machinelearningmastery.com/resample-interpolate-time-series-data-python/)
8. [Pandas docs on resample() method for time series](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.resample.html)
9. [(forum) Yahoo Finance Module - discontinued support for historical data](https://stackoverflow.com/questions/44753963/yahoo-finance-module-doesnt-work-anymore)
10. [(forum) How to get around the issues with Yahoo Finance historical data](https://stackoverflow.com/a/44445027)
11. [(forum) How to read a CSV string into a pandas DataFrame](https://stackoverflow.com/questions/22604564/how-to-create-a-pandas-dataframe-from-string)
12. [Pandas read_csv docs](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html)
13. [(forum) Dropping Pandas rows with duplicate index values in](https://stackoverflow.com/questions/13035764/remove-rows-with-duplicate-indices-pandas-dataframe-and-timeseries)
14. [How to coerce a Pandas series to numeric, NaN-ing the non-numeric stuff](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.to_numeric.html)

## Storm <a name="storm"></a>

1. [Apache Storm Installation Tutorial](https://www.tutorialspoint.com/apache_storm/apache_storm_installation.html)
2. [Download Mirror for Storm](http://www.apache.org/dyn/closer.lua/storm/apache-storm-1.1.0/apache-storm-1.1.0.tar.gz)
3. [Installing leiningren for Storm](https://leiningen.org/#install)
4. [Setting LEIN_ROOT so it installs without interaction](https://stackoverflow.com/questions/41517353/where-to-set-lein-root)
5. [Timeout and Bolt Heartbeat Issues](https://www.linkedin.com/pulse/heartbeat-issue-apache-storm-chandan-prakash)
6. [Storm REST API](http://storm.apache.org/releases/0.9.6/STORM-UI-REST-API.html)
7. [Running a multi-node Storm cluster](http://www.michael-noll.com/tutorials/running-multi-node-storm-cluster/)
8. [Explaining the Storm Architecture](https://www.tutorialspoint.com/apache_storm/apache_storm_cluster_architecture.htm)

## Zookeeper <a name="zookeeper"></a>

1. [Installing Zookeeper as a Service on CentOS 7](https://stackoverflow.com/questions/41611275/how-to-install-zookeeper-as-service-on-centos-7)
2. [Installing Zookeper from Cloudera](https://www.cloudera.com/documentation/enterprise/5-9-x/topics/cdh_ig_cdh5_install.html)
