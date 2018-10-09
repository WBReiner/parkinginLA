#do the thing, gets cluster num
import pandas as pd
import numpy as np
import hdbscan
from numpy import arccos, arcsin, around, cos, pi, radians, sin


def cluster_id(lat,long):
    #user_input_coords 
    u_lat=str(lat)
    u_lon=str(long)
    app_user_query = "SELECT * FROM parking_db WHERE lat_max >= '"+ u_lat +"'AND lat_min <='"+ u_lat +"'AND long_min <='"+ u_lon +"' AND long_max >='" + u_lon +"';"
    user_SUBSET = pd.read_sql_query(app_user_query,con)
    return user_SUBSET

cluster_id
