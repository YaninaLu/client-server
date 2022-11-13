import socket
import sys
from concurrent.futures import ThreadPoolExecutor

HOST = "localhost"
PORT = 8080


def handle_request(connection: socket.socket):
    with connection:
        while True:
            data = connection.recv(1024)
            if not data:
                break
            connection.send(b"OK")

def run_server(host, port):
    for specifications in socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
        family, socket_type, proto, host_name, sockaddr = specifications
        try:
            s = socket.socket(family, socket_type, proto)
        except OSError as err:
            print(f"Couldn't open a socket{err}")
            sys.exit(1)

        try:
            s.bind(sockaddr)
            s.listen(2)
        except OSError as err:
            s.close()
            print(f"Something went wrong: {err}")
            sys.exit(1)
        break

    with ThreadPoolExecutor(2) as client_pool:
        try:
            while True:
                connection, addr = s.accept()
                client_pool.submit(handle_request, connection)
        except KeyboardInterrupt:
            print("Server is closed")
        finally:
            s.close()


if __name__ == '__main__':
    run_server(HOST, PORT)
