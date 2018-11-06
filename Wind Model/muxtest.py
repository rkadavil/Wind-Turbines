# Pi-145
import sys
import struct

from connections import create_sockets

# Define connection dict
connect = (
    # pi145 to inl-villas bidirectional socket
    {
        'remote': '141.221.118.93:12160',
        'local': '*:5000',
        'socket': 'udp'
    }
)

# Create connection
loc, rem = create_sockets(connect)

while True:
    # Receive data
    #rtds_dat, _ = loc['sock0'].recvfrom(80)
    #value = struct.unpack(">ffffffffffffffffffff", rtds_dat)
    rtds_dat, _ = loc['sock0'].recvfrom(16)
    value = struct.unpack(">ffff", rtds_dat)
    print(value[0:2])
    loc['sock0'].sendto(bytearray(struct.pack(">ff", *(15.0,16.0))), rem['sock0'])
