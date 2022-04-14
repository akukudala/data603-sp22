import time
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()
stream_df = (spark.readStream.format('socket')
                             .option('host', 'localhost')
                             .option('port', 22223)
                             .load())

json_df = stream_df.selectExpr("CAST(value AS STRING) AS payload")

writer = (
    json_df.writeStream
           .queryName('iss')
           .format('memory')
           .outputMode('append')
)

streamer = writer.start()


for _ in range(5):
    df = spark.sql("""
    SELECT CAST(get_json_object(payload, '$.iss_position.latitude') AS FLOAT) AS latitude,
           CAST(get_json_object(payload, '$.iss_position.longitude') AS FLOAT) AS longitude 
    FROM iss
    """)
    
    df.show(10)
    
    print(df)
    time.sleep(5)
    
streamer.awaitTermination(timeout=10)
print('streaming done!')

# df = pd.read_csv('latlon.csv')
lat_list=[]
lon_list=[]
for lati,long in zip(df.select('latitude').collect(), df.select('longitude').collect()):
    lat_list.append(lati[0])
    lon_list.append(long[0])
 dfmap = pd.DataFrame(list(zip(lat_list, lon_list)),
               columns =['Latitude', 'Longitude'])
   
    
gdf = geopandas.GeoDataFrame(
    dfmap, geometry=geopandas.points_from_xy(dfmap.Longitude, dfmap.Latitude))
    
world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))


# We can now plot our ``GeoDataFrame``.
gdf.plot(ax=world.plot(
    color='white', edgecolor='black'), color='red')
plt.savefig('hw06_map.jpg')
plt.show()
fig=px.scatter_geo(dfmap, lat="Longitude", lon="Latitude")
fig.update_layout(title='4/13/2022 3:12:52 PM TO 4/13/2022 4:12:52 PM',title_x=0.5)
fig.show()