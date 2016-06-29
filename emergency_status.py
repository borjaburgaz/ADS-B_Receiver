'''
Created on 22/2/2015

@author: borjaburgaz
'''
def hex2bin(string):
    scale = 16                                  # Equals to hexadecimal
    num_of_bits = (len(string)/2)*8             # Necessary to avoid elimination of 0 at beginning of binary string
    out = bin(int(string, scale))[2:].zfill(num_of_bits)
    return out

def bin2dec(string):
    return int(string, 2)

raw_message = '9911118998580f1f9a9e'   #input data only + CRC
bin_info = hex2bin(raw_message)

subtype = bin2dec(bin_info[5:8])
emergency_state = bin2dec(bin_info[8:11])

def emergency_state_lookup(n):
    table = {0:'No Emergency',
             1:'General Emergency',
             2:'Lifeguard/Medical',
             3:'Minimum Fuel',
             4:'No Communications',
             5:'Unlawful Interference',
             6:'Reserved',
             7:'Reserved'}

    print("Emergency State: %s" % (table[n]))

