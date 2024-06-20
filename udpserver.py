import socket
import struct
import time
import random

SERVER_IP = '0.0.0.0'
SERVER_PORT = 12345
DROP_RATE = 0.3  # 30% drop rate

def create_response(seq_no, ver):
    server_time = time.strftime('%H-%M-%S', time.localtime())
    return struct.pack('!H B 200s', seq_no, ver, server_time.encode())

def parse_request(data):
    seq_no, ver, request_data = struct.unpack('!H B 200s', data)
    request_data = request_data.decode().strip('\x00')
    return seq_no, ver, request_data

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))

    print(f"Server listening on {SERVER_IP}:{SERVER_PORT}")

    while True:
        request, client_address = server_socket.recvfrom(2048)
        seq_no, ver, request_data = parse_request(request)

        # Simulate packet drop
        if random.random() > DROP_RATE:
            response = create_response(seq_no, ver)
            server_socket.sendto(response, client_address)
            print(f"Received Seq No: {seq_no}, responding to {client_address}")
        else:
            print(f"Dropped packet with Seq No: {seq_no}")

if __name__ == "__main__":
    main()
