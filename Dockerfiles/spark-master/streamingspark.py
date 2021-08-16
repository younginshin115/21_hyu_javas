from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark import SparkConf
from pyspark import SparkContext
from pyspark.sql import SparkSession

conf = SparkConf()
conf.setMaster('spark://spark-master:7077')
conf.setAppName('spark-basic')
sc = SparkContext(conf=conf)

spark = SparkSession \
.builder \
.appName("kafka-to-spark") \
.config("spark.some.config.option", "some-value") \
.getOrCreate()

sc.addFile("/spark/abuse_model_v1.py")
import abuse_model_v1 as abuse

sc.addFile("/spark/sentiment_model_v2.py")
import sentiment_model_v2 as sentiment

df_raw = spark \
.readStream \
.format('kafka') \
.option('kafka.bootstrap.servers', 'kafka:9092') \
.option("startingOffsets", "earliest") \
.option('subscribe', 'inchat') \
.load()

df1 = df_raw.selectExpr('CAST(value AS STRING) as value')

emotion_udf = udf(lambda x: sentiment.sentiment_model(x), StringType())
abuse_udf = udf(lambda x: abuse.slang_predict(x), StringType())

schema = StructType([ \
StructField("video_id",StringType(),True), \
StructField("user_name",StringType(),True), \
StructField("chat_id",StringType(),True), \
StructField("chat_text",StringType(),True), \
StructField("noun_token",ArrayType(StringType()),True), \
StructField("chat_time", TimestampType(),True)
])

df2 = df1.select(from_json("value",schema).alias("data")).select("data.*")

df3 = df2 \
.withColumn("emotion", emotion_udf(col('chat_text'))) \
.withColumn("abuse", abuse_udf(col('chat_text'))).alias('data')

df3 \
.selectExpr("CAST('data' AS STRING) AS key", "to_json(struct(*)) AS value") \
.writeStream    \
.format('kafka') \
.option('kafka.bootstrap.servers', 'kafka:9092') \
.option('topic', 'outchat') \
.option("truncate", False).option("checkpointLocation", "/tmp/dtn/checkpoint") \
.start().awaitTermination()
