import socket
import sys


HOST = "localhost"
PORT = 8080


def run_client(host, port):

    for specifications in socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
        family, socket_type, proto, host_name, sockaddr = specifications
        try:
            s = socket.socket(family, socket_type, proto)
        except OSError as err:
            print(f"Couldn't open a socket: {err}")
            sys.exit(1)

        try:
            s.connect(sockaddr)
        except OSError as err:
            s.close()
            print(f"Something went wrong: {err}")
            sys.exit(1)
        break

    with s:
        msg = input("Write your message here: ")
        s.send(msg.encode())
        response = s.recv(1024)
        if response:
            print(f"Received :{response.decode()}")
        else:
            print("Something went wrong - the server doesn't respond.")


if __name__ == '__main__':
    run_client(HOST, PORT)
