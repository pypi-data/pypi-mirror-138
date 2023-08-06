import socket
import re


def get_server_status(ip, port):
    port = int(port)
    ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ss.settimeout(10)
    ss.connect((ip, port))
    ss.send(b'\xFF\xFF\xFF\xFFgetstatus')
    dd = ss.recv(1000)
    i = 0
    status = {}
    for e in dd.replace(b'\n', b'').split(b'\\')[1:]:
        e = e.decode('utf-8')
        if i % 2 == 0:
            k = e
        else:
            status[k] = e
        i += 1
    ss.close()
    return status


def get_list_of_players(ip, port):
    dit = get_server_status(ip, port)
    raw = dit['server_freezetag']
    listOfPlayers = re.findall(r"\"(.*?)\"", raw)
    return listOfPlayers
