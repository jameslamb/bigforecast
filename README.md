# bigforecast

`bigforecast` is a macro/financial forecasting system completed per the requirements of the Summery 2017 session of "W251: Scaling Up! Really Big Data", part of the [UC-Berkeley Masters of Information in Data Science](https://datascience.berkeley.edu/) program.

# Table of contents
1. [Introduction](#introduction)
2. [Architecture](#architecture)
3. [Installation and Configuration](#installation)
    1. [Provisioning Your Cluster](#provisioning)
    2. [Setting up SSH Access](#ssh)
    3. [Installing Dependencies](#deps)
    4. [Configuring and Starting Elasticsearch](#elasticsearch)
    5. [Configuring and Starting InfluxDB](#influx)
4. [Running the App](#running)
    1. [Monitoring Elasticsearch](#monitorelastic)
5. [Data Sources](#datasources)
    1. [GDELT](#gdelt)

## Introduction <a name="introduction"></a>

The goal of this project is to create an automated system which produces near-term forecasts of globally important economic / financial time series. The system will create features from a wide variety of data sources and create forecasts using an ensemble of time series models. We will exploit distributed compute and storage technologies to build a system which is always on, evaluating new potential features and constantly updating the deployed forecasting model. We will begin with the daily spot price of crude oil, but hope to expand to other important series.

## Architecture <a name="architecture"></a>

* `conda` - dependency management
* `Elasticsearch` - Distributed document-store used for full-text search and extracting timeseries features from text.
* `Kafka` - Distributed messaging queue.
* `Python 3` - main orchestration tool. Storm bolts, Kafka producer, other miscellaneous tooling.
* `Storm` - Stream processing framework.
* `InfluxDB` - Time series database, used as a short-term store for the data used by our forecasting model. High-frequency data are written to this database and the modeling / validation code uses aggregation queries to test different windowed features.

![Diagram](bigforecast.png)

## Installation and Configuration <a name="installation"></a>

This application has been tested and developed on [CentOS 7.x](https://wiki.centos.org/Manuals/ReleaseNotes/CentOS7). If you want to use it on other Linux distributions, you should be able to do so by tweaking the scripts in the `setup/` directory.

### Provisioning Your Cluster <a name="provisioning"></a>

To begin, you should provision a cluster of machines. If you are using [IBM Softlayer](http://www.softlayer.com/) and the associated [Python CLI](http://softlayer-python.readthedocs.io/en/latest/cli.html), you can use the commands listed in `setup/provisioning.txt`.

### Setting up SSH access across your cluster <a name="ssh"></a>

Once your machines are provisioned, you'll need to go in and configure secure access between them. You should have a copy of the key you used when running the commands in `setup/provisioning.txt` laying around on your machine. If you called this key "bigforecast", you can log into one of your VMs from your laptop like this:

```
ssh -i root@${INGEST1_IP}
```

where `INGEST1_IP` is the public IP address of the VM you called `ingest1`. You can find this by running the following:

```
slcli vs list
```

You will be prompted for a password for this node. You can find the passwords for all your VMs in the Device Management Console on Softlayer or by running

```
slcli vs credentisl ${VM_ID}
```

where `VM_ID` is the numeric ID (something like "37684921") associated with the VM you want to log into. This is the leftmost column in the result returned by `slcli vs list`.

Once you're into the box, you'll need to update `/etc/hosts` with the information for the other nodes in your cluster. You can see what this looks like in the `setup/network/hosts` file in this repo, although you will have to update this file with the IP addresses assigned to your particular machines.

Run

```
sudo vi /etc/hosts
```

then paste in the information on your particular machines. Exit the file, then run the following to generate SSH keys and copy them to all the other nodes (just hit ENTER through all the prompts):

```
ssh-keygen
for i in ingest1 kafka1 kafka2 kafka3 elasticsearch1 elasticsearch2 elasticsearch3 elasticsearch4 modelbox storm1 storm2 storm3 storm4; do ssh-copy-id $i; done
```

You will be prompted for the root passwords for each host. This process is somewhat manual but will go faster if you put together a small table in a local text file that has the passwords for all the nodes. Don't put that into the repo or even save it, but just have it handy for quick copy-pastes.

Once this is done running, you'll again be able to enter commands. If this worked, you should be able to SSH to other nodes without using a password. Try running `ssh kafka1`, `ssh elasticsearch2`, etc. to see if you can get to all the other nodes.

Repeat this process (updating `/etc/hosts`, creating and copying keys) for each node in the cluster.

### Installing Dependencies <a name="deps"></a>

Now that your machines are provisioned and can talk to each other, it's time to start installing software! Grab a copy of `setup/setup_instance.sh` from this repo and place it on one of your VMs (for this example, let's use `ingest1`). Make it executable, then run it to install all dependencies...that's it! It should take 8-12 minutes to run and should not require you to respond to any prompts.

```
cd ~
chmod a+rwx setup_instance.sh
./setup_instance.sh
```

**NOTE:** The setup script will pull this repo from GitHub into each node it's run on. If you are working on a fork of `jameslamb/bigforecast`, be sure to change the URL inside `setup_instance.sh`.

You will need to run this script for all the other nodes in the cluster. For simplicity and to preserve your sanity, it's strongly recommended that you just install all dependencies on every VM (e.g. don't comment out the Elasticsearch installation on the nodes reserved for the Kafka cluster). You can copy the script to all the other nodes using `scp`:

```
for i in kafka1 kafka2 kafka3 elasticsearch1 elasticsearch2 elasticsearch3 elasticsearch4 modelbox storm1 storm2 storm3 storm4; do scp setup_instance.sh root@$i:/root/; done
```

But that's not all! You can also run commands over `ssh`, so you can install dependencies on each box from the comfort of `ingest1`. Like this:

```
for i in kafka1 kafka2 kafka3 elasticsearch1 elasticsearch2 elasticsearch3 elasticsearch4 modelbox storm1 storm2 storm3 storm4; do ssh root@${i} "bash /root/setup_instance.sh"; done
```

This may make installation a bit slower (since all of the console output from the nodes you're installing deps on will be directed back to `stdout` on `ingest1`) so, alternatively, you could just log into the other machines one at a time and run the installation script.

```
ssh kafka1
./setup_instance.sh

exit

ssh kafka2
./setup_instance.sh

# and so on for all nodes
```

Congratulations! Once this done, every box will have `Elasticsearch`, `Kafka`, `Zookeeper`, `Storm`, `Python 3`, `conda` and a few other things installed! One step closer to the fun stuff.

### Configuring and Starting Elasticsearch <a name="elasticsearch"></a>

As you can see in the architecture diagram above and / or infer from the host names in the provisioning script, this project is designed to use a 4-node [Elasticsearch](https://www.elastic.co/) cluster. This section explains how to get that cluster up and running. It is heavily inspired by [this tutorial for Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-set-up-a-production-elasticsearch-cluster-on-ubuntu-14-04). 

All of the Elasticsearch configuration needed to get up and running is taken care of for you when running `setup_instance.sh`. That script will install Java and Elasticsearch. It will also overwrite the default Elasticsearch configuration files with those tuned to our setup in this project.

To start Elasticsearch and form the cluster, just go into each Elasticsearch node and run the following command:

```
for i in elasticsearch1 elasticsearch2 elasticsearch3 elasticsearch4; do ssh ${i} "sudo systemctl start elasticsearch.service"; done
```

That command will create a cluster and use Elasticsearch's [Discovery](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-discovery.html) tools to connect all 4 nodes to it. Once you've done this on all four Elasticsearch nodes, your cluster should be up! Log in to any of the Elasticsearch nodes and run the following command:

```
curl -XGET curl -XGET 'http://<host_ip>:9200/_cluster/state?pretty'
```

If this worked correctly, you should see 4 nodes in the "nodes" output. It may look something like this:

```
...
  "nodes" : {
    "6fTZGAuyT6OvLq1_AaLzUQ" : {
      "name" : "elasticsearch1",
      "ephemeral_id" : "sDdnlBNHSFaiL43cE9PLGA",
      "transport_address" : "169.53.131.87:9300",
      "attributes" : { }
    },
    "CnElG-S6RbChpHC6lYSZZw" : {
      "name" : "elasticsearch4",
      "ephemeral_id" : "YM5MUyUPTeKVA-ZmLV_A_Q",
      "transport_address" : "169.53.131.86:9300",
      "attributes" : { }
    },
    "bJVY3g1ZSCWnQq04vZznPw" : {
      "name" : "elasticsearch3",
      "ephemeral_id" : "fFB3CzijSxW3hJks6o6oDw",
      "transport_address" : "169.53.131.94:9300",
      "attributes" : { }
    },
    "_F8K-F8RSVKXcgtsmMBxCw" : {
      "name" : "elasticsearch2",
      "ephemeral_id" : "Ov5iLRt9TcCUxOFPUY8fGw",
      "transport_address" : "169.53.131.83:9300",
      "attributes" : { }
    }
  }
...
```

To view logs for Elasticsearch, you can run the following on one of the VMs running Elasticsearch:

```
tail /var/log/elasticsearch/bigforecast.log
tail /var/log/elasticsearch/elasticsearch.log
```

If you ever need to stop Elasticsearch on one of the nodes, you can log in to the box you want to stop and run this command:

```
sudo systemctl stop elasticsearch.service
```

### Configuring and Starting InfluxDB <a name="influx"></a>

This project uses [InfluxDB](https://www.influxdata.com/) as the serving database for model training. Influx is a time-series DB with really slick semantics for pushing windowed aggregations into the query layer. It also offers excellent compression of time series data.

Almost of the installation details for InfluxDB are taken care of in `setup/setup_instance.sh`, inspired in large part by [this tutorial](http://vmkdaily.ghost.io/influxdb-and-grafana-on-centos/).

Therea are two tiny steps you'll have to do manually. Following the solution [here](https://eapyl.github.io/article/InfluxDB-cant-be-started-as-a-service-21-December-2016.html), SSH into the noded you want to run InfluxDB on and open up `influxdb.service`

```
sudo vi /lib/systemd/system/influxdb.service:
```

Comment out the two lines about "User" and "Group". Your `influxdb.service` will now look something like this:

```
[Unit]
Description=InfluxDB is an open-source, distributed, time series database
Documentation=https://docs.influxdata.com/influxdb/
After=network-online.target

[Service]
#User=influxdb
#Group=influxdb
LimitNOFILE=65536
EnvironmentFile=-/etc/default/influxdb
ExecStart=/usr/bin/influxd -config /etc/influxdb/influxdb.conf ${INFLUXD_OPTS}
KillMode=control-group
Restart=on-failure

[Install]
WantedBy=multi-user.target
Alias=influxd.service
```

Next, we need to configure InfluxDB to take HTTP traffic over its public IP. Do do this, we'll edit `influxdb.conf`. Find the `http` section and pass your Influx node's public IP address in the settings.

```
sudo vi /etc/influxdb/influxdb.conf
```

The relevant section may look something like this when you're done:

```
...
[http]
  # Determines whether HTTP endpoint is enabled.
  enabled = true

  # The bind address used by the HTTP service.
  bind-address = "198.11.200.86:8086"
...
```

OK ok enough nonsense, let's start up the DB! To start up InfluxDB, SSH into whichever VM you want (`modelbox`, in this design) and run the following commands. The first command reloads the settings from the configs we just edited. The second one starts up the DB.

```
sudo systemctl daemon-reload
sudo service influxdb start
```

To check if this worked, you can look in the logs:

```
tail /var/log/messages
```

You can also check here:

```
systemctl status influxdb
```

To learn more:

- [How to start the InfluxDB Web UI(http://www.techietown.info/2017/03/enable-influxdb-web-ui/)

## Running the App <a name="running"></a>

### Monitoring Elasticsearch <a name="monitorelastic"></a>

To monitor Elasticsearch while the app is running, we recommend using [elasticsearch-head](https://github.com/mobz/elasticsearch-head). You can install the app [as a Chrome extension](https://chrome.google.com/webstore/detail/elasticsearch-head/ffmkiejjmecolpfloofpjologoblkegm/), enter the relevant hostname and port in the box at the top, and you're on your way!

## Data Sources <a name="datasources"></a>

### GDELT <a name="gdelt">

The [GDELT 2.0 Event Database](https://blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/) serves as our source of global, potentially market-moving news. In this project, we consume the stream of events coming into `GDELT 2.0` and index them into Elasticsearch. We then use ES queries to create time series feature vectors from the news stories. Detail on the fields available in this dataset can be found in the [GDELT 2.0 Event Database Codebook](http://data.gdeltproject.org/documentation/GDELT-Event_Codebook-V2.0.pdf).
