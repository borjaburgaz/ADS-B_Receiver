# adsb_decoder

ADS-B Receiver: Treats the signal, decodes the messages and extracts all information and subsequently plots it and stores in a MySQL database. The real-time mapping application allows the visualization of the received positions of the aircraft.

The system runs mostly on Python although it has some dependencies based on C. The system was developed on Ubuntu 16.04 LTS however it should run perfectly on UNIX based operating system.

Installation:
  The system has a number of dependencies that are required for it to function correctly:
      
      1. Python 2.7
      
      2. Dump1090 (all signal treatment is done with this and then messages are passed through a TCP tunnel (port 30002) (https://github.com/antirez/dump1090)
      
      3. Basemap (an extension to the popular Matplotlib python package) (http://matplotlib.org/basemap/)
      
      4. MySQL

Launch:
  1. Connect SDR dongle (preferably RTL2832U, although other types should work just fine.)
  2. Launch dump1090 with the raw and network profile: ./dump1090 --raw --net
  3. Run mysql_map_adsb.py

Initialization may take a few seconds to load all satellite imagery and create the MySQL database. Two databases are created Adsbdata and Positions, the first includes all of the decoded messages and the second keeps only the last updated data for each aircraft. The mapping properties can be adjusted within mysql_map_adsb.py.
