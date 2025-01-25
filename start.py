from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, concat, to_timestamp, date_format, to_date, sum as _sum, min as _min, max as _max, lag
from pyspark.sql.window import Window

spark = SparkSession.builder \
  .appName("Test Mod") \
  .config("spark.driver.extraJavaOptions", "-Djava.security.manager=allow") \
  .config("spark.executor.extraJavaOptions", "-Djava.security.manager=allow") \
  .getOrCreate()
  

df = spark.read.csv("data/MTA_Subway_Stations_and_Complexes.csv", header=True, inferSchema=True)

df = df.drop("ADA", "ADA Notes", "Is Complex", "Number Of Stations In Complex", "Constituent Station Names", "Station IDs", "Borough", "CBD") \
  .withColumnRenamed("Complex ID", "complex_id") \
  .withColumnRenamed("Stop Name", "stop_name") \
  .withColumnRenamed("Display Name", "display_name") \
  .withColumnRenamed("GTFS Stop IDs", "unit") \
  .withColumnRenamed("Daytime Routes", "daytime_routes") \
  .withColumnRenamed("Structure Type", "structure_type") \
  .withColumnRenamed("Latitude", "latitude") \
  .withColumnRenamed("Longitude", "longitude") \

df.columns

# spark.stop()



