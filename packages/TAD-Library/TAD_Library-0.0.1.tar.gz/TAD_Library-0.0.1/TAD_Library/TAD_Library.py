import socket

global client_socket

def Connect_TAD_B():
    global client_socket

    HOST = "127.0.0.1"
    PORT = 111
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

def SendCmd(cmd):
    global  client_socket

    client_socket.send(cmd)

def send_text(str):
    data = bytearray([])
    data.append(0x01)  # Set
    data.append(0x11)  # Text
    byte_str = bytearray(str.encode())

    for bStr in byte_str:
        data.append(bStr)

    data.append(0xFF) #End of text
    SendCmd(data)


