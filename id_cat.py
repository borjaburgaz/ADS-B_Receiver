'''
Created on 16/2/2015

@author: borjaburgaz
'''

def hex2bin(string):
    scale = 16                                  # Equals to hexadecimal
    num_of_bits = (len(string)/2)*8             # Necessary to avoid elimination of 0 at beginning of binary string
    out = bin(int(string, scale))[2:].zfill(num_of_bits)
    return out
'''
def bin2dec(string):
    return int(string, 2)
'''
def bin2dec(buf):
    if 0 == len(buf): # Crap input
        return -1
    return int(buf, 2)

def aircraft_cat_lookup(tc,n):

    seta = {0:'No aircraft category information',
            1:'Light(<15500lbs or 7031kg)',
            2:'Medium 1 (15500 to 75000lbs or 7031 to 34019kg)',
            3:'Medium 2 (75000 to 300000lbs or 34019 to 136078kg)',
            4:'High vortex aircraft',
            5:'Heavy (>300000lbs or 136078kg)',
            6:'High performance (>5g acceleration) and high speed (> 400kt)',
            7:'Rotorcraft'}
    setb = {0:'No aircraft category information',
            1:'Glider/sailplane',
            2:'Lighter-than-air',
            3:'Parachutist/skydiver',
            4:'Ultralight/hang-glider/paraglider',
            5:'Reserved',
            6:'Unmanned aerial vehicle',
            7:'Space/transatmospheric vehicle'}
    setc = {0:'No aircraft category information',
            1:'Surface vehicle - emergency vehicle',
            2:'Surface vehicle - service vehicle',
            3:'Fixed ground or tethered obstruction',
            4:'Reserved',
            5:'Reserved',
            6:'Reserved',
            7:'Reserved'}
    setd = {0:'Reserved',
            1:'Reserved',
            2:'Reserved',
            3:'Reserved',
            4:'Reserved',
            5:'Reserved',
            6:'Reserved',
            7:'Reserved'}

    if tc == 4:
        print("Aircraft Vehicle Category: %s" % (seta[n]))
    elif tc == 3:
        print("Aircraft Vehicle Category: %s" % (setb[n]))
    elif tc == 2:
        print("Aircraft Vehicle Category: %s" % (setc[n]))
    else:
        print("Aircraft Vehicle Category: %s" % (setd[n]))

def character_decod(string):
    table = {0:'',
             1:'A',
             2:'B',
             3:'C',
             4:'D',
             5:'E',
             6:'F',
             7:'G',
             8:'H',
             9:'I',
             10:'J',
             11:'K',
             12:'L',
             13:'M',
             14:'N',
             15:'O',
             16:'P',
             17:'Q',
             18:'R',
             19:'S',
             20:'T',
             21:'U',
             22:'V',
             23:'W',
             24:'X',
             25:'Y',
             26:'Z',
             27:'',
             28:'',
             29:'',
             30:'',
             31:'',
             32:' ',
             33:'',
             34:'',
             35:'',
             36:'',
             37:'',
             38:'',
             39:'',
             40:'',
             41:'',
             42:'',
             43:'',
             44:'',
             45:'',
             46:'',
             47:'',
             48:'0',
             49:'1',
             50:'2',
             51:'3',
             52:'4',
             53:'5',
             54:'6',
             55:'7',
             56:'8',
             57:'9',
             58:'',
             59:'',
             60:'',
             61:'',
             62:'',
             63:'',
             64:''}

    n = bin2dec(string)
    return table[n]
'''
raw_message ='8d49529120501431cf1ca04cf016'
bin_message = hex2bin(raw_message)
bin_info = hex2bin(raw_message[8:])
tc = 4

aircraft_cat = bin2dec(bin_info[5:8])
aircraft_cat_lookup(tc,aircraft_cat)

ch1 = character_decod(bin_info[8:14])
ch2 = character_decod(bin_info[14:20])
ch3 = character_decod(bin_info[20:26])
ch4 = character_decod(bin_info[26:32])
ch5 = character_decod(bin_info[32:38])
ch6 = character_decod(bin_info[38:44])
ch7 = character_decod(bin_info[44:50])
ch8 = character_decod(bin_info[50:56])

flight_id = ch1+ch2+ch3+ch4+ch5+ch6+ch7+ch8

print(flight_id)
'''







