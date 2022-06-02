# Exploratory Data Analysis(EDA) with PySpark on Google Playstore
<p align="center">
<img src="https://github.com/akukudala/Practice_repo/blob/main/PlayStore.png" width="600" height="600"   />
	</p>
	
## Introduction
 This project is a journey of analyzing various apps found on the Google play store with the help of PySpark. 
 Being an everyday phone user, it is interesting  to take the real time application information  and drive the insights on installations.
  
 ## Data Content
 Dataset: Dataset is downloaded from Kaggle
It consists of 28 columns as mentioned below and 450796 rows.

App Name, App Id, Category, Rating, Rating Count, Installs, Minimum Installs,  Free, Price, Currency, Size, Minimum Android, Developer Id, Developer Website  Developer Email, Released, Last update, Privacy Policy, Content Rating, Ad  Supported, In app purchases, Editor Choice, Summary, Reviews, Android version  Text, Developer, Developer Address, Developer Internal ID, Version

## Data Preparation

The data mostly appears to be clean.
	There are some special characters in the data  which needs to be cleaned.
## Goal with EDA
Exploratory Analysis and Visualization
* Top categories in the play store?
* Top apps contains the highest number of installations?
* Ratings structure of the Apps?
* Distribution of App Sizes?
* What % of Apps are updating in a regular basis?
* Free Vs Paid Apps?
* Paid Apps and its top earnings calculated based on installations?

There are around 3 million apps found on Google Play Store. 
With this project, we will analyze various
apps found on the play store with the help of different python libraries.

Initial step is to clean the data. Here I am loading the data into Pyspark Dataframe to perform cleaning.

1. Cleaning the data


```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate() # Creating a Spark Session

df = spark.read.option("wholeFile", True).option("multiline",True).option("header", True).option("inferSchema", "True").csv("Playstore_final_1.csv")
# Reading the data from the csv file by providing options to handle multiline data and to consider the first row as header.

df.printSchema() # Using pyspark.sql.DataFrame.printSchema to print the structure in tree format

df2=df.drop("_c40","_c29","_c30","_c31","_c32","_c33","_c34","_c35","_c36","_c37","_c38","_c39","_c41","_c42","_c43","_c44","_c45","_c46","_c47","_c48","_c49","_c50","_c51","_c52","_c53","_c54","_c55","_c56")
# Dropping the unwanted columns by using drop() function

df2.cache()
df2.persist()
# Using cache() and persist() methods, Spark provides an optimization mechanism to store the intermediate computation of an RDD, DataFrame, and Dataset so they can be reused in subsequent actions(reusing the RDD, Dataframe, and Dataset computation result’s).

```
2. Top Category of Apps along with the count.

```python 

from pyspark.sql import functions as F
dffinal2.select('Category').groupBy('Category').agg(F.count('Category').alias('CategoryCount')).orderBy('CategoryCount', ascending=False).show()

```

References:

https://www.freepnglogos.com/pics/play-store-logo
