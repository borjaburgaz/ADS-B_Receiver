'''
Created on 13/2/2015

@author: borjaburgaz
'''
def bin2dec(string):
    scale = 2
    return int(string, 2)

def downlink_format(DF):

    table = {0:'Short Air to Air ACAS',
             4:'Surveillance (roll call) Altitude',
             5:'Surveillance (roll call) IDENT Reply',
             11:'Mode S Only All-Call Reply (Acq. Squitter if II=0)',
             16:'Long Air to Air ACAS',
             17:'1090ES (ADS-B)',
             18:'1090ES (ADS-B transmitter only)',
             19:'Military Extended Squitter',
             20:'Comm. B Altitude, IDENT Reply',
             21:'Comm. B Altitude, IDENT Reply',
             22:'Military use only',
             24:'Comm. D Extended Length Message (ELM)',}

    DF = bin2dec(DF[0:5])
    #CA = bin2dec(DF[5:])
    print("Downlink Format: %s (%s)" % (table[int(DF)],int(DF)))
    return DF

def df_selector(DF):
    if DF == 17 or DF == 18:
        return True
    else:
        return False


