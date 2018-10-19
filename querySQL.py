#Import packages
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2

# Define a database name
# Set your postgres username
dbname = 'postgres'
username = '' # change this to your username


## 'engine' is a connection to a database
## Here, we're using postgres, but sqlalchemy can connect to other things too.
engine = create_engine('postgres://%s@localhost/%s'%(username,dbname))
print(engine.url)


# Connect to make queries using psycopg2
con = None
con = psycopg2.connect(database = dbname, user = username)

# query:
sql_query = """
SELECT * FROM import.ladataset201678 WHERE issueyear='2018'
LIMIT 100000;
"""

tickets_table_from_sql = pd.read_sql_query(sql_query,con)
tickets_table_from_sql
tickets_table_from_sql.dtypes

tickets_table_from_sql['newlat'] = pd.to_numeric(tickets_table_from_sql['newlat'])
tickets_table_from_sql['newlong'] = pd.to_numeric(tickets_table_from_sql['newlong'])
tickets_table_from_sql['dt_issuednew'] = pd.to_datetime(tickets_table_from_sql['dt_issuednew'])
tickets_table_from_sql.dtypes


tickets_table_from_sql = tickets_table_from_sql[~tickets_table_from_sql['newlat'].isnull()] 
tickets_table_from_sql[['newlong','newlat']].isnull().sum()

df=tickets_table_from_sql
df.columns
