"""Socket handlers

Will return local and remote socket objects
"""

import socket
import sys
#from typing import Dict


def get_ip():
    """
    OS-free way of getting the IP address of the host machine.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 1))
    except IOError:
        sys.exit('Network error. Check your network settings.')

    return s.getsockname()[0]


def return_split(val):
    return val.split(':')


def return_sockobj(val):
    if val in ['udp', 'UDP']:
        return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    elif val in ['tcp', 'TCP']:
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    else:
        raise Exception("Socket communication can be either TCP or UDP!! Socket type not supported!!")


def create_sockets(connections):
    r"""
    This function will accept a tuple with multiple dict that contains
    the path for each bi-directional UDP/TCP socket connections.

    Arguments:
    :param connections:
    :return local_sock:
    :return rem_sock:
    """
    if not connections or len(connections) == 0:
        raise Exception("Missing a tuple with at least one dict object \n with 'local' and 'remote' keys required")
    local_sock, rem_sock = {}, {}  # type: Dict[str, socket]
    for i in range(len(connections)):
        # for each path
        if type(connections) != dict:
            sock_det = return_split(connections[i]['local'])  # connections[i]['local'].split(':')
            rem_det = return_split(connections[i]['remote'])  # connections[i]['remote'].split(':')
            temp = return_sockobj(connections[i]['socket'])
        else:
            sock_det = return_split(connections['local'])
            rem_det = return_split(connections['remote'])
            temp = return_sockobj(connections['socket'])

        temp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        temp.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 0)
        rem_det[1] = int(rem_det[1])
        rem_det = tuple(rem_det)
        if '*' in sock_det:
            ip = get_ip()
        else:
            ip = sock_det[0]
        port = int(sock_det[1])

        try:
            temp.bind((ip, port))
        except socket.error as msg:
            sys.exit("[Socket error]: %s. Check your connection configuration." % msg)
        local_sock['sock' + str(i)] = temp
        rem_sock['sock' + str(i)] = rem_det
        if type(connections) == dict:
            break
    return local_sock, rem_sock


'''
# test variable
connect = (
    # source to destination communication sockets
    {
        'remote': '141.221.118.200:18000',
        'local': '*:19000',
        'socket': 'udp'
    }
)  # type: Dict[str, str]

loc, rem = create_sockets(connect)  # type: (Dict[str, socket], Dict[str, socket])
print(loc, rem)
'''
