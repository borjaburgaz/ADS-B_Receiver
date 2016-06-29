'''
Created on 13/2/2015

@author: borjaburgaz
'''

def hex2bin(string):
    scale = 16                  # Equals to hexadecimal
    num_of_bits = (len(string)/2)*8             # Necessary to avoid elimination of 0 at beginning of binary string
    out = bin(int(string, scale))[2:].zfill(num_of_bits)
    return out

def bin2dec(string):
    scale = 2
    return int(string, 2)

def typecode(TC,display):

    table = {0: 'No position information',
             1: 'Identification (Category Set D)',
             2: 'Identification (Category Set C)',
             3: 'Identification (Category Set B)',
             4: 'Identification (Category Set A)',
             5: 'Surface position',
             6: 'Surface position',
             7: 'Surface position',
             8: 'Surface position',
             9: 'Airborne position',
             10: 'Airborne position',
             11: 'Airborne position',
             12: 'Airborne position',
             13: 'Airborne position',
             14: 'Airborne position',
             15: 'Airborne position',
             16: 'Airborne position',
             17: 'Airborne position',
             18: 'Airborne position',
             19: 'Airborne velocity',
             20: 'Airborne position',
             21: 'Airborne position',
             22: 'Airborne position',
             23: 'Reserved for test purposes',
             24: 'Reserved for surface system status',
             25: 'Reserved',
             26: 'Reserved',
             27: 'Reserved',
             28: 'Extended squitter aircraft emergency priority status',
             29: 'Reserved',
             30: 'Reserved',
             31: 'Aircraft operational status'}

    status = TC[5:]
    TC_dec = bin2dec(TC[0:5])
    if display:
        print("Type Code Format: %s (%s)" % (table[int(TC_dec)],int(TC_dec)))
    return int(TC_dec)