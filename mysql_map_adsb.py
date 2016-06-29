import longitude_zones_lookup, typecode_lookup, df_lookup, airborne_velocity, math, id_cat, surf_position
import socket
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib as mpl
import matplotlib.pyplot as plt
import time
import MySQLdb as mdb
import sys
	
def split(message):
    h1 = message[0:2]       # First part of the header: DF+CA
    h2 = message[2:8]       # Second part of the header: ICAO 24bit address
    data = message[8:22]    # Data
    ec = message[22:]       # Redundancy Check (to be ignored)

    return h1, h2, data, ec

def hex2bin(string):
    scale = 16                  # Equals to hexadecimal
    num_of_bits = (len(string)/2)*8             # Necessary to avoid elimination of 0 at beginning of binary string
    out = bin(int(string, scale))[2:].zfill(num_of_bits)
    return out

def bin2dec(string):
    scale = 2
    return int(string, 2)

def floor(number):
    if number < 0:
        return round(number)
    else:
        return int(number)

def mod(x,y):
	res = int(x%y)
	if res < 0:
		res += y
	return res

def altdecod(string):       # Altitude in binary form as input

    if string[7] == 0:
        increment = 100
    else:
        increment = 25

    string_shifted = string[0:7] + string[8:]
    altitude = bin2dec(string_shifted)*increment + 1000

    return altitude

def cpr_airborne(mess0, mess1, fflag):
	Nb = 17
	Nz = 15
	#print("mess1",mess1)

	lat0 = bin2dec(mess0[14:31])
	#print("------",mess1[14:31])
	#print("lat0:",lat0)
	lon0 = bin2dec(mess0[31:])
	#print("lon0:",lon0)
	lat1 = bin2dec(mess1[14:31])
	#print("lat1:",lat1)
	lon1 = bin2dec(mess1[31:])
	#print("lon1:",lon1)
	
	j = floor(((59.0*lat0 - 60.0*lat1)/131072.0)+0.5)
	#print("j =",j)
	Dlat0 = 360.0/60.0
	Dlat1 = 360.0/59.0

	rlat0 = Dlat0*(mod(j,60.0)+lat0/131072.0)
	rlat1 = Dlat1*(mod(j,59.0)+lat1/131072.0)
	
	if (rlat0 >= 270) or (rlat1 >= 270):
		rlat0 = rlat0 - 360.0
		rlat1 = rlat1 - 360.0
	
	NL0 = longitude_zones_lookup.n_lon_zones(rlat0)
	NL1 = longitude_zones_lookup.n_lon_zones(rlat1)
	
	if NL0 != NL1:
		return "Error calculating position"
	
	if fflag:
		ni = NL1 - 1.0
		Dlon1 = 360.0 / ni
		M = np.floor(((lon0*(NL1 - 1.0)- (lon1*NL1))/131072.0) + 0.5)
		lon = Dlon1 * (mod(M,ni)+ lon1 / 131072.0)
		if lon > 180:
			lon = lon - 360
		lat = rlat1
		return (lon, lat)
	else:
		ni = NL0
		Dlon0 = 360.0 / ni
		M = np.floor(((lon0*(NL0 - 1.0)- (lon1*NL0))/131072.0) + 0.5)
		lon = Dlon0 * (mod(M,ni)+ lon0 / 131072.0)
		if lon > 180:
			lon = lon - 360
		lat = rlat0
		return (lon, lat)

running = True
msg_num = 1
dict_cpr = {'AAAAAA':['list0','list1']}


#-------Connect to MySQL Server-------#
con = mdb.connect('localhost','testuser', 'test623', 'testdb');
with con:
	cur = con.cursor()
	cur.execute("DROP TABLE IF EXISTS Positions")
	cur.execute("CREATE TABLE Positions(Icao VARCHAR(25) PRIMARY KEY, Flightid VARCHAR(25), Lon FLOAT(25), Lat FLOAT(25), \
				Altitude FLOAT(25), Airspeed FLOAT(25), Heading FLOAT(25))")


mpl.rcParams['figure.figsize'] = (10,10)

map = Basemap(projection='merc', lat_0 = 40.4372300, lon_0 = -3.8460100,
		resolution = 'h', area_thresh = 10000,
		llcrnrlon=-5, llcrnrlat=39,
		urcrnrlon=-2, urcrnrlat=41,
		epsg = 2062) #5520
	 
map.drawcoastlines()
map.drawcountries()

map.drawmapscale(-7., 35.8, -3.25, 39.5, 500, barstyle='fancy')

map.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 1500, verbose= True)
#map.drawmapboundary(fill_color = 'aqua')
#map.fillcontinents(color='coral', lake_color='aqua', zorder = 0)
#map.drawmeridians(np.arange(0,360,30))
#map.drawparallels(np.arange(-90,90,30))
x1,y1 = map(-3.560833,40.472222)
map.plot(x1,y1,'o')
plot_handle, = map.plot(0,0,'ro')
#label1 = plt.annotate('Barcelona', xy=(0, 0),  xycoords='data',
#											xytext=(2, 2), textcoords='offset points',
#											color='r',
#											arrowprops=dict(arrowstyle="-", color='g')  #arrowstyle defines the type of line
#											)

plt.ion()
plt.show()

while running == True:
	#------Connecting to TCP------#
	TCP_IP = 'localhost'
	TCP_PORT = 30002
	BUFFER_SIZE = 64
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	data = []
	s.connect((TCP_IP,TCP_PORT))
	data = s.recv(BUFFER_SIZE)
	s.close()
	
	msg_num = msg_num + 1
	#print msg_num,"received data:",data
	#print len(data)
	
	if len(data) == 31:
		raw_message = data[1:28]
		binary_mess = hex2bin(raw_message)
		DF = bin2dec(binary_mess[0:5])
		#print("--------->",binary_mess[0:4])
		if DF == 17:
			mess_sep = split(raw_message)
			ICAO =  mess_sep[1]
			TC_bin = binary_mess[32:40]
			information = binary_mess[40:88]
			TC = typecode_lookup.typecode(TC_bin, True)
			
			if 9 <= TC <= 18:		#Airborne Position & Altitude
				flag = int(information[13])
				print('FLAG:',flag,'DATA',raw_message)
				mess_meta = [flag, "timestamp", information]
				
				#Altitude Calculation
				alt_bin = information[0:12]
				altitude = altdecod(alt_bin)
				
				if ICAO in dict_cpr:
					dict_cpr[ICAO][flag] = mess_meta
					print("COMPLETE MESSAGE:",ICAO)
					print(dict_cpr[ICAO])
					if (dict_cpr[ICAO][0][1] == "timestamp") and (dict_cpr[ICAO][1][1] == "timestamp"):
						position = cpr_airborne(dict_cpr[ICAO][0][2], dict_cpr[ICAO][1][2], flag)
						if position:
							lon = position[0]
							lat = position[1]
							print ICAO
							print (lon, lat)
							with con:
								cur = con.cursor()
								cur.execute("INSERT INTO Positions(Icao, Lon, Lat, Altitude) VALUES(%s,%s,%s,%s) \
											On DUPLICATE KEY UPDATE Lon = VALUES(Lon), Lat = VALUES(Lat), Altitude = VALUES(Altitude)", (ICAO, lon, lat, altitude))
				else:
					if flag == 0:
						dict_cpr[ICAO] = [mess_meta,"empty"]
						print(dict_cpr[ICAO])
					elif flag == 1:
						dict_cpr[ICAO] = ["empty",mess_meta]
						print(dict_cpr[ICAO])	
			elif TC == 19:          #Airborne velocity
				bin_info = hex2bin(raw_message[8:])
				subtype = bin2dec(bin_info[5:8])
				airborne_velocity.vel_subtype_lookup(subtype)
		
				if subtype == 1 or subtype == 2:            #Ground Speed
					intent_change_flag = bin_info[8]
					ifr_capability_flag = bin_info[9]
					airborne_velocity.ifr_cap_flag_explanation(ifr_capability_flag)
		
					nuc_r = bin2dec(bin_info[10:13])
					airborne_velocity.nuc_decoder(nuc_r)
		
					dir_vel_ew = int(bin_info[13])
					dir_vel_ns = int(bin_info[24])
		
					ew_velocity_value = bin2dec(bin_info[14:24])
					ew_velocity = float(airborne_velocity.ground_vel_decode(ew_velocity_value,subtype))
		
					ns_velocity_value = bin2dec(bin_info[25:35])
					ns_velocity = float(airborne_velocity.ground_vel_decode(ns_velocity_value,subtype))
		
					abs_velocity = math.sqrt(ew_velocity**2.0+ns_velocity**2.0)
		
					heading = airborne_velocity.airborne_vel_heading(ew_velocity, ns_velocity, dir_vel_ew, dir_vel_ns)
					
					with con:
						cur = con.cursor()
						cur.execute("INSERT INTO Positions(Icao, Airspeed, Heading) VALUES(%s,%s,%s) \
									On DUPLICATE KEY UPDATE Airspeed = VALUES(Airspeed), Heading = VALUES(Heading)", (ICAO, abs_velocity, heading))
						
					vert_rate_source = bin_info[35]
					airborne_velocity.vert_rate_source_exp(vert_rate_source)
					vert_sign = bin_info[36]                                 # 0=Up, 1=Down
					vert_rate_value = bin2dec(bin_info[37:46])
					if vert_rate_value == 0:
						vert_rate = 666
					else:
						vert_rate=airborne_velocity.vert_rate_calc(vert_rate_value,vert_sign)
		
					turn_indicator = bin_info[46:48]
		
					gnss_alt_sign = bin_info[48]
					gnss_alt_diff_value = bin2dec(bin_info[49:56])
		
					if gnss_alt_diff_value == 0:
						gnss_alt_diff = 666
					else:
						gnss_alt_diff = (gnss_alt_diff_value - 1)*25
		
				elif subtype == 3 or subtype == 4:              #Airspeed and Magnetic Heading
					intent_change_flag = bin_info[8]
					ifr_capability_flag = bin_info[9]
					airborne_velocity.ifr_cap_flag_explanation(ifr_capability_flag)
		
					nuc_r = bin2dec(bin_info[10:13])
					airborne_velocity.nuc_decoder(nuc_r)
		
					status_bit = bin_info[13]
					airborne_velocity.status_exp(status_bit)
		
					magnetic_heading_bin = bin_info[14:24]
					magnetic_heading_msb = 360.0/1024.0
					magnetic_heading = airborne_velocity.weighed_binary(magnetic_heading_msb,magnetic_heading_bin)
		
					airspeed_type = bin_info[24]
					airborne_velocity.airspeed_type_exp(airspeed_type)
					airspeed_value = bin2dec(bin_info[25:35])
					if airspeed_value == 0:
						airspeed = 666
					else:
						airspeed = airborne_velocity.airspeed_decode(airspeed_value, subtype)
						
					with con:
						cur = con.cursor()
						cur.execute("INSERT INTO Positions(Icao, Airspeed, Heading) VALUES(%s,%s,%s) \
									On DUPLICATE KEY UPDATE Airspeed = VALUES(Airspeed), Heading = VALUES(Heading)", (ICAO, airspeed, magnetic_heading))

					vert_rate_source = bin_info[35]
					airborne_velocity.vert_rate_source_exp(vert_rate_source)
					vert_sign = bin_info[36]                  # 0=Up, 1=Down
					vert_rate_value = bin2dec(bin_info[37:46])
					vert_rate=airborne_velocity.vert_rate_calc(vert_rate_value,vert_sign)
		
					turn_indicator = bin_info[46:48]
		
					gnss_alt_sign = bin_info[48]
					gnss_alt_diff_value = bin2dec(bin_info[49:56])
					if gnss_alt_diff_value == 0:
						gnss_alt_diff = 666
					else:
						gnss_alt_diff = (gnss_alt_diff_value - 1)*25
			elif 1 <= TC <= 4:		#Flight ID
				bin_info = hex2bin(raw_message[8:22])
				aircraft_cat = bin2dec(bin_info[5:8])
				
				ch1 = id_cat.character_decod(bin_info[8:14])
				ch2 = id_cat.character_decod(bin_info[14:20])
				ch3 = id_cat.character_decod(bin_info[20:26])
				ch4 = id_cat.character_decod(bin_info[26:32])
				ch5 = id_cat.character_decod(bin_info[32:38])
				ch6 = id_cat.character_decod(bin_info[38:44])
				ch7 = id_cat.character_decod(bin_info[44:50])
				ch8 = id_cat.character_decod(bin_info[50:56])
		
				flight_id = ch1+ch2+ch3+ch4+ch5+ch6+ch7+ch8
				
				with con:
					cur = con.cursor()
					cur.execute("INSERT INTO Positions(Icao, Flightid) VALUES(%s,%s) \
								On DUPLICATE KEY UPDATE Flightid = VALUES(Flightid)", (ICAO, flight_id))
			
			#------Begin Map Treatment------#
			with con:
				cur = con.cursor()
				cur.execute("SELECT * FROM Positions")
				rows = cur.fetchall()
				
				first_pass = True
				if cur.rowcount != 0:
					for i in range(cur.rowcount):
						if rows[0][2] != None and rows[i][3] != None and first_pass:
							lon = [rows[i][2]]
							lat = [rows[i][3]]
							first_pass = False
						elif rows[i][2] != None and rows[i][3] != None and first_pass == False:
							lon = lon + [rows[i][2]]
							lat = lat + [rows[i][3]]
				if 'lon' and 'lat' in locals():
					print lon
					print lat
					x,y = map(lon,lat)
					#label1.remove()
					
					#x2, y2 = (-90, 10)

					#label1 = plt.annotate('Barcelona', xy=(x, y),  xycoords='data',
					#						xytext=(x2, x2), textcoords='offset points',
					#						color='r',
					#						arrowprops=dict(arrowstyle="-", color='g')  #arrowstyle defines the type of line
					#						)
					
					plot_handle.set_ydata(y)
					plot_handle.set_xdata(x)
					plt.draw()
				
					
				
