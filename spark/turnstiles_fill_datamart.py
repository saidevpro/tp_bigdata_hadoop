from pyspark.sql import SparkSession
from pyspark.sql.functions import sum as _sum, to_date, col


spark = SparkSession.builder \
  .appName("Hive to DataMart") \
  .config("spark.sql.catalogImplementation", "hive") \
  .config("hive.metastore.uris", "thrift://hive-metastore:9083") \
  .enableHiveSupport() \
  .getOrCreate()
  
  
hive_table = "default.turnstiles"
df = spark.sql(f"SELECT * FROM {hive_table}")

tdf = df.select("c/a", "unit", "scp", "station").distinct()
jdf = df.withColumn("date", to_date(col("timestamp"))) \
  .groupBy("unit", "scp", "station", "date") \
  .agg( _sum("entries").alias("entries"), _sum("exits").alias("exits") )
    

postgres_url = "jdbc:postgresql://postgres-db:5432/datamart"
postgres_properties = {
  "user": "psg",
  "password": "psg",
  "driver": "org.postgresql.Driver"
}

jdf.write.jdbc(url=postgres_url, table="journal_turnstiles", mode="overwrite", properties=postgres_properties)
tdf.write.jdbc(url=postgres_url, table="turnstiles", mode="overwrite", properties=postgres_properties)

spark.stop()



