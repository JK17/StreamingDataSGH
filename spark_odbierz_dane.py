# spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1,org.mongodb.spark:mongo-spark-connector_2.12:10.1.1 spark_odbierz_dane.py
# spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1 spark_odbierz_dane.py

from pyspark.sql import SparkSession
from pyspark.sql import functions as f
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    FloatType,
)

if __name__ == "__main__":
    
    spark = SparkSession.builder.appName("stream").getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")

    # json message schema
    json_schema = StructType(
        [
            StructField("event_time", StringType()),
            StructField("value", FloatType()),
            StructField("temperature", FloatType()),
            StructField("location", StringType())
        ]
    )
    
    # topic subscription
    raw = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", "broker:9092")
        .option("subscribe", "test2")
        .load()
    )
    
    parsed = raw.select(
        "timestamp", f.from_json(raw.value.cast("string"), json_schema).alias("json")
    ).select(
        f.col("timestamp").alias("proc_time"),
        f.col("json").getField("event_time").alias("event_time"),
        f.col("json").getField("temperature").alias("temperature"),
        f.col("json").getField("location").alias("location"),
    )

    # defining output to csv
    query = parsed.writeStream.outputMode("append")\
        .format("parquet")\
        .option("path", "wyniki")\
        .option("checkpointLocation", "wyniki/_spark_metadata/")\
        .start()
    query.awaitTermination()
    query.stop()

    # defining output
    # query = parsed.writeStream.outputMode("append").format("console").start()
    # query.awaitTermination()
    # query.stop()

    # #tryWithMongo
    # query = parsed.writeStream.outputMode("append").format("mongodb")\
    # .option("checkpointLocation", "/tmp/pyspark/")\
    # .option("forceDeleteTempCheckpointLocation", "true")\
    # .option("spark.mongodb.connection.uri", "mongodb://localhost:27017/")\
    # .option("spark.mongodb.database","jk_test")\
    # .option("spark.mongodb.collection", "data_from_spark").start()

    query.awaitTermination()
    query.stop()