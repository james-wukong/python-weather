import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder.master("local[*]") \
                        .appName('Weather API') \
                        .getOrCreate()

# Create DataFrame
# df = spark.createDataFrame(
#     [("Scala", 25000), ("Spark", 35000), ("PHP", 21000)])
# df.show()

# # Spark SQL
# df.createOrReplaceTempView("sample_table")
# df2 = spark.sql("SELECT _1,_2 FROM sample_table")
# df2.show()

# # Create Hive table & query it.  
# spark.table("sample_table").write.saveAsTable("sample_hive_table")
# df3 = spark.sql("SELECT _1,_2 FROM sample_hive_table")
# df3.show()

# Get metadata from the Catalog
# List databases
dbs = spark.catalog.listDatabases()
print(dbs)

# List Tables
tbls = spark.catalog.listTables()
print(tbls)