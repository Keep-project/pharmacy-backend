
from math import radians, cos, sin, asin, sqrt

#☺ Python 3 program to calculate Distance Between Two Points on Earth

def distance(lat1, lat2, lon1, lon2):
     
    # The math module contains a function named
    # radians which converts from degrees to radians.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
      
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
 
    c = 2 * asin(sqrt(a))
    
    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371
      
    # calculate the result
    return(c * r)
     
     
# driver code
lat1 =  4.05 # Douala latitude
lat2 =  3.866667 # Yaoundé latitude
lon1 = 9.7 # Douala longitude
lon2 = 11.516667 # Yaoundé longitude
print(distance(lat1, lat2, lon1, lon2), "K.M")