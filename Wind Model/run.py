import sys
import struct
import signal
from connections import create_sockets
import turbine_power as WP
import air_density as aird
from regulation import droop_ctrl
from helpers import *

def sigint_handler(signum, frame):
    sys.exit('Exiting Script, Goodbye!')

# Define connection dict
connect = (
    # pi10 to villasNode bidirectional socket
    {
        'remote': '192.168.0.10:12160',
        'local': '*:5000',
        'socket': 'udp'
    }
)

# Define variables
ref_f = 60.0
timestep = 9e-4
wind_rate_lim = 5.0
droop_rate_lim = 4.0
old_wind_val = 0.0
old_droopOut = 0.0

# Create connection
loc, rem = create_sockets(connect)

# Clean exit script
signal.signal(signal.SIGINT, sigint_handler)
print("Wind Turbine active:pi10")
print('Press Ctrl+C to Quit')


# Run frequency regulation
while True:
    # Receive data
    rtds_dat, _ = loc['sock0'].recvfrom(40)
    # value[0]: out0sysfreq, value[1]: out1windspeed, value[2]: out2airtmpdegc,
    # value[3]: out3humidity, value[4]: out4airpressmb, value[5]: out5droop
    # value[6]: out6droopact, value[7]: out7rotordia, value[8]: out8cp, value[9]: out9WTScale => 10 x 4 = 40bytes
    value = struct.unpack(">ffffffffff", rtds_dat)

    # Air pressure:
    ad = aird.calc(value[2], value[4], value[3])
    
    # Computer Wind Power Output
    wgen = WP.calc(value[7], ad, value[8], value[1], 'MW')

    # Perform Droop
    droopOut = droop_ctrl(ref_f, value[0], value[5], value[6])

    Pdg1 = ((0.9*wgen) + (0.1*droopOut))*value[9]
    Pdg1max = wgen*value[9]
    
    print(Pdg1,Pdg1max)
    # Send data
    loc['sock0'].sendto(bytearray(struct.pack(">ff", *(Pdg1,Pdg1max))), rem['sock0'])

