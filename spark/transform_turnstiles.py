from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, concat, to_timestamp, date_format, to_date, lag
from pyspark.sql.window import Window

spark = SparkSession.builder \
    .appName("Turnstile Data Transformation") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:9000") \
    .config("spark.sql.catalogImplementation", "hive") \
    .config("hive.metastore.uris", "thrift://hive-metastore:9083") \
    .enableHiveSupport() \
    .getOrCreate()
    
    
hdfs_input_path = "hdfs://namenode:9000/nyc_subway_data/turnstile"
df = spark.read.csv(hdfs_input_path, header=True, inferSchema=True)
df = df.toDF(*[*df.columns[:-1], 'EXITS'])

df = df.withColumn("TIMESTAMP",  concat(to_date(df["DATE"], "MM/dd/yyyy"), lit(" "), date_format(df["TIME"], "HH:mm:ss"))) \
  .withColumn("TIMESTAMP", to_timestamp("TIMESTAMP")) \
  .withColumn("DATE", to_date(df["DATE"], "MM/dd/yyyy")) \
  .withColumn("ENTRIES", col("ENTRIES").cast("int")) \
  .withColumn("EXITS", col("EXITS").cast("int")) \
  .withColumnRenamed("C/\A","CA") \
  .drop("TIME", "DATE")
  
winspec = Window.partitionBy("SCP", "STATION", "DIVISION").orderBy("TIMESTAMP")

df = df.withColumn("ENTRIES", col("ENTRIES") - lag("ENTRIES", 1).over(winspec)) \
  .withColumn("EXITS", col("EXITS") - lag("EXITS", 1).over(winspec))
  
df = df.filter(df["ENTRIES"] >= 0).filter(df["EXITS"] >= 0) \
  .orderBy("SCP", "STATION", "DIVISION")

# RENAME ALL COLUMNS TO LOWERCASE
df = df.select([col(c).alias(c.lower()) for c in df.columns])
  
df.write.mode("overwrite").format("parquet").saveAsTable("default.turnstiles")
  
spark.stop()


