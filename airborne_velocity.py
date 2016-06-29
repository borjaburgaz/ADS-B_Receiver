'''
Created on 14/2/2015

@author: borjaburgaz
'''
import math

def hex2bin(string):
    scale = 16                                  # Equals to hexadecimal
    num_of_bits = (len(string)/2)*8             # Necessary to avoid elimination of 0 at beginning of binary string
    out = bin(int(string, scale))[2:].zfill(num_of_bits)
    return out

def bin2dec(string):
    return int(string, 2)

def no_info_detect(string):
    num_bits = len(string)
    i = 1
    zeros = '0'
    while i < num_bits:
        zeros = zeros+'0'
        i = i+1
    if string == zeros:
        return True
    else:
        return False

def vel_subtype_lookup(subtype):

    table = {0:'Reserved',
             1:'Normal Ground Speed',
             2:'Supersonic Ground Speed',
             3:'Normal Airspeed Heading',
             4:'Supersonic Airspeed Heading',
             5:'Reserved',
             6:'Reserved',
             7:'Reserved'}

    print("Velocity Subtype: %s (%s)" % (table[subtype],subtype))

def ifr_cap_flag_explanation(flag):
    if flag == 0:
        print('Transmitting aircraft has no capability for ADS-B- based conflict detection or higher level (class A1 or above) applications')
    else:
        print('Transmitting aircraft has capability for ADS-B- based conflict detection and higher level (class A1 or above) applications.')

def nuc_decoder(nuc):
    hor_error = {0:'Unknown',
                 1:'<10 m/s',
                 2:'<3 m/s',
                 3:'<1 m/s',
                 4:'<0.3 m/s'}
    ver_error = {0:'Unknown',
                 1:'<15.2 m/s (50 fps)',
                 2:'<4.6 m/s (15 fps)',
                 3:'<1.5 m/s (5 fps)',
                 4:'<0.46 m/s (1.5 fps)'}
    print("Horizontal Velocity Error 95pc: %s, Vertical Velocity Error 95pc: %s ." % (hor_error[nuc],ver_error[nuc]))

def ground_vel_decode(value, type):
    if value == 0:
        return 'n/a'
    if type == 1:
        increment = 1         #knt
        if value == 1023:
            return '>1021.5'
        else:
            return (value-1)*increment
    else:
        increment = 4
        if value == 1033:
            return '>4086'
        else:
            return (value-1)*increment

def airspeed_decode(value, type):
    if value == 0:
        return 'n/a'
    if type == 3:
        increment = 1         #knt
        if value == 1023:
            return '>1021.5'
        else:
            return (value-1)*increment
    else:
        increment = 4
        if value == 1033:
            return '>4086'
        else:
            return (value-1)*increment

def vert_rate_source_exp(i):
    if i == 0:
        print('Source for Vertical Rate: GNSS')
    else:
        print('Source for Vertical Rate: Barometer')

def vert_rate_calc(value,sign):
    if value == 0:
        return 'n/a'
    increment = 64              #ft/min
    abs_rate = (value-1)*increment
    if sign==0:
        return abs_rate
    else:
        return -abs_rate

def gnss_alt_sign_exp(i):
    if i == 0:
        print('GNSS altitude above baro. altitude')
    else:
        print('GNSS altitude below baro. altitude')

def status_exp(i):
        if i == 0:
            print('Magnetic heading not available')
        else:
            print('Magnetic heading available')

def weighed_binary(lsb,string):
        n_bits = len(string)
        n = lsb*2.0**n_bits
        out = 0
        i=1
        while i <= n_bits:
            out=out + float((n/2.0**i))*int(string[i])
            i = i + 1
        return out

def airspeed_type_exp(i):
        if i == 0:
            print('Airspeed Type: IAS')
        else:
            print('Airspeed Type: TAS')

def airborne_vel_heading(ew_vel,ns_vel,ew_dir,ns_dir):
    if ew_dir == 0 and ns_dir == 0:
        return 90.0 - (math.atan(ns_vel/ew_vel)*(180.0/math.pi))
    elif ew_dir == 0 and ns_dir == 1:
        return (math.atan(ns_vel/ew_vel)*(180.0/math.pi)) + 90.0
    elif ew_dir == 1 and ns_dir == 1:
        return 270.0 - (math.atan(ns_vel/ew_vel)*(180.0/math.pi))
    else:
        return (math.atan(ns_vel/ew_vel)*(180.0/math.pi)) + 270.0



############################################################################
'''
raw_message = '9911118998580f1f9a9e'   #input data only + CRC
bin_info = hex2bin(raw_message)
print(bin_info)

subtype = bin2dec(bin_info[5:8])
vel_subtype_lookup(subtype)

if subtype == 1 or subtype == 2:
    intent_change_flag = bin_info[8]
    ifr_capability_flag = bin_info[9]
    ifr_cap_flag_explanation(ifr_capability_flag)

    nuc_r = bin2dec(bin_info[10:13])
    nuc_decoder(nuc_r)

    dir_vel_ew = bin_info[13]
    dir_vel_ns = bin_info[24]

    ew_velocity_value = bin2dec(bin_info[14:24])
    ew_velocity = ground_vel_decode(ew_velocity_value,subtype)
    print(ew_velocity)

    ns_velocity_value = bin2dec(bin_info[25:35])
    ns_velocity = ground_vel_decode(ns_velocity_value,subtype)
    print(ns_velocity)

    vert_rate_source = bin_info[35]
    vert_rate_source_exp(vert_rate_source)      # 0=Up, 1=Down
    vert_sign = bin_info[36]
    vert_rate_value = bin2dec(bin_info[37:46])
    if vert_rate_value == 0:
        vert_rate = 'n/a'
    else:
        vert_rate=vert_rate_calc(vert_rate_value,vert_sign)

    turn_indicator = bin_info[46:48]

    gnss_alt_sign = bin_info[48]
    gnss_alt_diff_value = bin2dec(bin_info[49:56])

    if gnss_alt_diff_value == 0:
        gnss_alt_diff = 'n/a'
    else:
        gnss_alt_diff = (gnss_alt_diff_value - 1)*25

    print(gnss_alt_diff)

elif subtype == 3 or subtype == 4:
    intent_change_flag = bin_info[8]
    ifr_capability_flag = bin_info[9]
    ifr_cap_flag_explanation(ifr_capability_flag)

    nuc_r = bin2dec(bin_info[10:13])
    nuc_decoder(nuc_r)

    status_bit = bin_info[13]
    status_exp(status_bit)

    magnetic_heading_bin = bin_info[14:24]
    magnetic_heading_msb = 180
    magnetic_heading = weighed_binary(magnetic_heading_msb,magnetic_heading_bin)

    airspeed_type = bin_info[24]
    airspeed_type_exp(airspeed_type)
    airspeed_value = bin2dec(bin_info[25:35])
    if airspeed_value == 0:
        airspeed = 'n/a'
    else:
        airspeed = airspeed_decode(airspeed_value, subtype)
        print(airspeed)

    vert_rate_source = bin_info[35]
    vert_rate_source_exp(vert_rate_source)
    vert_sign = bin_info[36]                  # 0=Up, 1=Down
    vert_rate_value = bin2dec(bin_info[37:46])
    vert_rate=vert_rate_calc(vert_rate_value,vert_sign)

    turn_indicator = bin_info[46:48]

    gnss_alt_sign = bin_info[48]
    gnss_alt_diff_value = bin2dec(bin_info[49:56])
    if gnss_alt_diff_value == 0:
        gnss_alt_diff = 'n/a'
    else:
        gnss_alt_diff = (gnss_alt_diff_value - 1)*25
    print(gnss_alt_diff)
'''
