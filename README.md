Gets zones affected by loadshedding for the current time.


Eventual aim: get the next loadshedding stage based on your current location. Most likely web-app


i.e.
- get location from device
- find a way to place the user within a zone
    - very likely to need the zone maps as not just a picture
- given the zone number, can just iterate from current time, in 2-hour intervals, until the zone_calculator's return contains the user's zone
