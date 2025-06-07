# test_pyspark.py
from pyspark.sql import SparkSession

print("Attempting to create a SparkSession…")
spark = SparkSession.builder.master("local[*]").appName("TestPySparkImport").getOrCreate()
print("✅ Successfully created SparkSession!")
spark.stop()