# eda_spark.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import to_timestamp, col
import matplotlib.pyplot as plt

spark = SparkSession.builder \
    .appName("GridSupplyEDA") \
    .master("local[*]") \
    .getOrCreate()

# Directly reference one of your CSVs at the project root:
csv_path = r"./bishops-wood_wmids.csv"  

df_spark = spark.read.csv(csv_path, header=True, inferSchema=True)

print("===== Spark DataFrame Schema =====")
df_spark.printSchema()
print("\n===== First 5 rows =====")
df_spark.show(5, truncate=False)

df_spark = df_spark.withColumn("ts", to_timestamp(col("Timestamp"), "yyyy-MM-dd HH:mm:ss"))
sample_pdf = df_spark.select("ts", "Import").orderBy("ts").limit(5000).toPandas()

sample_pdf.set_index("ts")['Import'].resample('1H').mean().plot(figsize=(12, 6))
plt.title("Spark‐Pandas: Hourly Average of 'Import'")
plt.xlabel("Timestamp")
plt.ylabel("Import")
plt.tight_layout()
plt.show()

spark.stop()