#!/bin/bash

spark-submit --master spark://spark-master:7077 /app/transform_stations.py
spark-submit --master spark://spark-master:7077 /app/transform_turnstiles.py
spark-submit --master spark://spark-master:7077 --jars /opt/spark/postgresql-42.7.5.jar /app/turnstiles_fill_datamart.py
spark-submit --master spark://spark-master:7077 --jars /opt/spark/postgresql-42.7.5.jar /app/stations_fill_datamart.py