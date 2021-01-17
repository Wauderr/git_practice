import sqlite3
import pandas as pd
db = sqlite3.connect('hubway.db')


def run_query(query):
    return pd.read_sql_query(query, db)


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('max_colwidth', None)

cur = db.cursor()

# What are the 10 longest trips? How long is the longest Trips?
query1 = '''
SELECT duration FROM trips
ORDER BY duration desc
LIMIT 10;
'''

# What is the total number of trips by registered users?
query2 = '''
SELECT COUNT(*) AS 'Total trips by registered users' FROM trips
WHERE sub_type = "Registered";
'''

# What is the average duration of trips per user type (Registered/casual)?
query3 = '''
SELECT sub_type, AVG(duration) AS 'Average Duration' FROM trips
GROUP BY sub_type;
'''

# Which bike has been used for the most trips?
query4 = '''
SELECT bike_number AS 'Bike number', COUNT(*) as 'Total number of trips'
FROM trips
GROUP BY bike_number
ORDER BY COUNT(*) DESC
LIMIT 1
'''

# What is the average duration of trips by registered user over 30?
query5 = '''
SELECT sub_type, AVG(duration) AS 'Average duration' FROM trips
WHERE (2021 - birth_date) > 30 and sub_type = 'Registered';
'''

# What are the columns in the stations table?
query6 = '''
SELECT * FROM stations
LIMIT 10
'''

# Which station is the most frequent starting point?
query7 = '''
SELECT stations.station AS 'Station', COUNT(*) AS 'Count'
FROM trips INNER JOIN stations
ON trips.start_station = stations.id
GROUP BY stations.station
ORDER BY COUNT(*) DESC
LIMIT 5
'''

# Which stations are most frequently used for round trips?
query8 = '''
SELECT stations.station AS 'Station', COUNT(*) AS 'Count'
FROM trips INNER JOIN stations
ON trips.start_station = stations.id
WHERE trips.start_station = trips.end_station
GROUP BY stations.station
ORDER BY COUNT(*) DESC
LIMIT 5
'''

# How many trips start and end in different municipalities?
query9 = '''
SELECT COUNT(trips.id) as 'COUNT'
FROM trips INNER JOIN stations AS start
ON trips.start_station = start.id
INNER JOIN stations AS end
ON trips.end_station = end.id
WHERE start.municipality != end.municipality;
'''

# Additional Quetsions
# How many trips incurred additional fees (longer than 30 minutes)?
query10 = '''
SELECT COUNT(*) AS 'Total number of trips longer than 30 minutes' FROM trips
WHERE duration / 60 > 30;
'''

# Which bike was used for the longest total time?
query11 = '''
SELECT bike_number AS 'Bike Number',
SUM(duration) AS 'Total duration'
FROM trips
GROUP BY bike_number
ORDER BY SUM(duration) DESC
LIMIT 10
'''

# Did registered or casual users take more round trips?
query12 = '''
SELECT trips.sub_type AS 'User type', COUNT(*) AS 'Number of round trips'
FROM trips INNER JOIN stations
ON trips.start_station = stations.id
WHERE trips.start_station = trips.end_station
GROUP BY trips.sub_type
ORDER BY COUNT(*) DESC
LIMIT 1
'''

# Which municipality had the longest average duration?
# Decided that the question would be: in what municipalicity do people take
# the bike and ride the longest? I looked at the start_station and not at the end
# station.
query13 = '''
SELECT stations.municipality AS 'Municipality',
AVG(trips.duration) AS 'Average Duration'
FROM trips INNER JOIN stations
ON trips.start_station = stations.id
GROUP BY stations.municipality
ORDER BY AVG(trips.duration) DESC
'''
print(run_query(query13))
