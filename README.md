# bigforecast

`bigforecast` is a macro/financial forecasting system completed per the requirements of the Summery 2017 session of "W251: Scaling Up! Really Big Data", part of the [UC-Berkeley Masters of Information in Data Science](https://datascience.berkeley.edu/) program.

# Table of contents
1. [Introduction](#introduction)
2. [Architecture](#architecture)
3. [Installation and Configuration](#installation)
    1. [Provisioning Your Cluster](#provisioning)
    2. [Setting up SSH Access](#ssh)
    3. [Installing Dependencies](#deps)
4. [Running the App](#running)
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

You will need to do this for all the other nodes in the cluster. For simplicity and to preserve your sanity, it's strongly recommended that you just install all dependencies on every VM (e.g. don't comment out the Elasticsearch installation on the nodes reserved for the Kafka cluster). You can copy the script to all the other nodes using `scp`:

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

## Running the App <a name="running"></a>

## Data Sources <a name="datasources"></a>

### GDELT <a name="gdelt">

The [GDELT 2.0 Event Database](https://blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/) serves as our source of global, potentially market-moving news. In this project, we consume the stream of events coming into `GDELT 2.0` and index them into Elasticsearch. We then use ES queries to create time series feature vectors from the news stories. Detail on the fields available in this dataset can be found in the [GDELT 2.0 Event Database Codebook](http://data.gdeltproject.org/documentation/GDELT-Event_Codebook-V2.0.pdf).
