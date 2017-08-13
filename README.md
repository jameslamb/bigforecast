# bigforecast

## Introduction

The goal of this project is to create an automated system which produces near-term forecasts of globally important economic / financial time series. The system will create features from a wide variety of data sources and create forecasts using an ensemble of time series models. We will exploit distributed compute and storage technologies to build a system which is always on, evaluating new potential features and constantly updating the deployed forecasting model. We will begin with the daily spot price of crude oil, but hope to expand to other important series.

# Table of contents
1. [Architecture](#architecture)
2. [Installation and Configuration](#installation)
3. [Running the App](#running)
4. [References](#nextsteps)

## Architecture <a name="architecture"></a>

* `conda` - dependency management
* `Elasticsearch` - Distributed document-store used for full-text search and extracting timeseries features from text.
* `Kafka` - Distributed messaging queue.
* `Python 3` - main orchestration tool. Storm bolts, Kafka producer, other miscellaneous tooling all.
* `Storm` - Stream processing framework.

## Installation and Configuration <a name="installation"></a>

This application has been tested and developed on [CentOS 7.x](https://wiki.centos.org/Manuals/ReleaseNotes/CentOS7). If you want to use it on other Linnux distributions, you should be able to do so by tweaking the scripts in the `setup/` directory.

## Running the App <a name="running"></a>

## References <a name="references"></a>
