# bigforecast

`bigforecast` is a macro/financial forecasting system completed per the requirements of the Summery 2017 session of "W251: Scaling Up! Really Big Data", part of the [UC-Berkeley Masters of Information in Data Science](https://datascience.berkeley.edu/) program.

# Table of contents
1. [Introduction](#introduction)
2. [Architecture](#architecture)
3. [Installation and Configuration](#installation)
4. [Running the App](#running)
5. [Data Sources](#datasources)
    1. [GDELT](#gdelt)

## Introduction <a name="introduction"></a>

The goal of this project is to create an automated system which produces near-term forecasts of globally important economic / financial time series. The system will create features from a wide variety of data sources and create forecasts using an ensemble of time series models. We will exploit distributed compute and storage technologies to build a system which is always on, evaluating new potential features and constantly updating the deployed forecasting model. We will begin with the daily spot price of crude oil, but hope to expand to other important series.

## Architecture <a name="architecture"></a>

* `conda` - dependency management
* `Elasticsearch` - Distributed document-store used for full-text search and extracting timeseries features from text.
* `Kafka` - Distributed messaging queue.
* `Python 3` - main orchestration tool. Storm bolts, Kafka producer, other miscellaneous tooling all.
* `Storm` - Stream processing framework.
* `InfluxDB` - Time series database, used as a short-term store for the data used by our forecasting model. High-frequency data are written to this database and the modeling / validation code uses aggregation queries to test different windowed features.

![Diagram](bigforecast.png)

## Installation and Configuration <a name="installation"></a>

This application has been tested and developed on [CentOS 7.x](https://wiki.centos.org/Manuals/ReleaseNotes/CentOS7). If you want to use it on other Linnux distributions, you should be able to do so by tweaking the scripts in the `setup/` directory.

## Running the App <a name="running"></a>

## Data Sources <a name="datasources"></a>

### GDELT <a name="gdelt">

The [GDELT 2.0 Event Database](https://blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/) serves as our source of global, potentially market-moving news. In this project, we consume the stream of events coming into `GDELT 2.0` and index them into Elasticsearch. We then use ES queries to create time series feature vectors from the news stories. Detail on the fields available in this dataset can be found in the [GDELT 2.0 Event Database Codebook](http://data.gdeltproject.org/documentation/GDELT-Event_Codebook-V2.0.pdf).
