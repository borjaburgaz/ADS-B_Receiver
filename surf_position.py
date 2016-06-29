'''
Created on 21/2/2015

@author: borjaburgaz
'''
import airborne_velocity, longitude_zones_lookup

def hex2bin(string):
    scale = 16                                  # Equals to hexadecimal
    num_of_bits = (len(string)/2)*8             # Necessary to avoid elimination of 0 at beginning of binary string
    out = bin(int(string, scale))[2:].zfill(num_of_bits)
    return out

def bin2dec(string):
    return int(string, 2)

def floor(number):
    if number < 0:
        return round(number)
    else:
        return int(number)

def mod(x,y):
    if y == 0:
        print('Error in mod, y=0, cannot have this value.')
    else:
        return x-y*floor(x/y)

def movement_decode(value):
    if value == 0:
        out = 'n/a'
    elif value == 1:
        out = 0
    elif 2 <= value <= 8:
        out = 0.125*(value-2)+0.125             #Ground Speed is given in knots.
    elif 9 <= value <= 12:
        out = 0.25*(value-9)+1
    elif 13 <= value <= 38:
        out = 0.5*(value-13)+2
    elif 39 <= value <= 93:
        out = 1*(value-39)+15
    elif 94 <= value <= 108:
        out = 2*(value-94)+70
    elif 109 <= value <= 123:
        out = 5*(value-109)+100
    elif value == 124:
        out = 175
    else:
        out = 'Reserved'

    return out

def surf_lonlatcalc(lat_bin,lon_bin,lat_s,lon_s,flag):
    YZ = int(lat_bin)
    XZ = int(lon_bin)
    Nb = len(lat_bin)
    NZ = 15.0

    Dlat = 90.0/(4.0*NZ-flag)
    j = floor(lat_s/Dlat) + floor(0.5 + (mod(lat_s,Dlat)/Dlat)-(YZ/2.0**Nb))
    Rlat = Dlat*(j+(YZ/2.0**Nb))

    NL = longitude_zones_lookup.n_lon_zones(Rlat)
    if (NL-flag) > 0:
        Dlon = 90.0/(NL-flag)
    else:
        Dlon = 90.0
    m = floor(lon_s/Dlon) + floor(0.5 + (mod(lon_s,Dlon)/Dlon)-(XZ/2.0**Nb))
    Rlon = Dlon*(m+(XZ/2.0**Nb))
    return [Rlat, Rlon]

raw_message = '9911118998580f1f9a9e'   #input data only + CRC
bin_info = hex2bin(raw_message)

movement_value = bin2dec(bin_info[5:12])

ground_speed = movement_decode(movement_value)
ground_track_status = int(bin_info[12])

ground_track_bin = bin_info[13:21]
ground_track_lsb = 360.0/128.0

if ground_track_status == 1:
    ground_track = airborne_velocity.weighed_binary(ground_track_lsb,ground_track_bin)
else:
    ground_track = 'n/a'

utc_sync_bin = bin_info[20]

flag = int(bin_info[21])

lat_bin = bin_info[22:39]
lon_bin = bin_info[39:56]
lat_s = 40.4372
lon_s = 3.8465

position = surf_lonlatcalc(lat_bin,lon_bin,lat_s,lon_s,flag) + [0]
