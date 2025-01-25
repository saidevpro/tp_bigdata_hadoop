from pyspark.sql import SparkSession
from pyspark.sql.functions import sum as _sum, to_date, col


spark = SparkSession.builder \
  .appName("Hive to DataMart") \
  .config("spark.sql.catalogImplementation", "hive") \
  .config("hive.metastore.uris", "thrift://hive-metastore:9083") \
  .enableHiveSupport() \
  .getOrCreate()
  

tdf = spark.sql(f"SELECT * FROM default.turnstiles")
sdf = spark.sql(f"SELECT * FROM default.stations")

tdf = tdf.withColumn("date", to_date(col("timestamp"))) \
  .groupBy("station", "date") \
  .agg( _sum("entries").alias("entries"), _sum("exits").alias("exits") )
    
postgres_url = "jdbc:postgresql://postgres-db:5432/datamart"
postgres_properties = {
  "user": "psg",
  "password": "psg",
  "driver": "org.postgresql.Driver"
}

tdf.write.jdbc(url=postgres_url, table="journal_stations", mode="overwrite", properties=postgres_properties)
sdf.write.jdbc(url=postgres_url, table="stations", mode="overwrite", properties=postgres_properties)

spark.stop()



