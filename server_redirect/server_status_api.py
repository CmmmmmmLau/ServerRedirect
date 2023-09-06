import socket
import struct


def readVarInt(sock: socket.socket):
    result = 0
    for i in range(5):
        byteVarInt = ord(sock.recv(1))
        result |= (byteVarInt & 0x7F) << 7 * i
        if not byteVarInt & 0x80:
            break

    return result


def writeVarInt(num: int):
    result = bytearray()

    while True:
        byteVarInt = num & 0x7F
        num >>= 7

        result.append((byteVarInt | 0x80) if num else byteVarInt)
        if not num:
            break

    return bytes(result)


def writePort(port: int):
    return struct.pack(">H", port)


def writeHost(host: str):
    hostLength = writeVarInt(len(host))
    host = bytes(host.encode("utf8"))
    return hostLength + host


def writePackage(data):
    packageLength = writeVarInt(len(data))
    return packageLength + data


def requestServerStatus(host='localhost', port=25565):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    dataPackage = b"\x00\x00" + writeHost(host) + writePort(port) + b"\x01"
    sock.send(writePackage(dataPackage))
    sock.send(writePackage(b"\x00"))

    packageLength = readVarInt(sock)
    packageID = readVarInt(sock)
    stringLength = readVarInt(sock)

    jsonString = b""
    while len(jsonString) < stringLength:
        jsonString += sock.recv(1024)

    sock.close()

# TODO
# maybe a class object here for used to access data
