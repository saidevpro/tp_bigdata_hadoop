#!/bin/bash

hdfs dfs -mkdir -p /nyc_subway_data
hdfs dfs -put /data/* /nyc_subway_data

# Keep the container running
tail -f /dev/null