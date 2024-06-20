import socket
import struct
import time
import random

SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345
TIMEOUT = 0.1  # 100ms


def create_packet(seq_no, ver, data):
    return struct.pack('!H B 200s', seq_no, ver, data.encode())


def parse_response(data):
    seq_no, ver, response_data = struct.unpack('!H B 200s', data)
    response_data = response_data.decode().strip('\x00')
    return seq_no, ver, response_data


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(TIMEOUT)

    seq_no = 1
    ver = 2
    rtts = []
    responses = 0
    sent_packets = 0
    start_time = time.time()

    for i in range(12):
        data = 'request' + str(seq_no).zfill(194)
        packet = create_packet(seq_no, ver, data)

        for _ in range(3):  # Maximum of 3 attempts
            try:
                start = time.time()
                client_socket.sendto(packet, (SERVER_IP, SERVER_PORT))
                sent_packets += 1  # 每次发送包后将 sent_packets 加 1
                response, _ = client_socket.recvfrom(2048)
                end = time.time()

                rtt = (end - start) * 1000  # RTT in milliseconds
                seq_no_resp, ver_resp, server_time = parse_response(response)
                print(
                    f"Seq No: {seq_no_resp}, Server IP: {SERVER_IP}:{SERVER_PORT}, RTT: {rtt:.2f}ms, Server Time: {server_time}")
                rtts.append(rtt)
                responses += 1
                break
            except socket.timeout:
                print(f"Seq No: {seq_no}, request timeout")
                continue
        else:
            print(f"Seq No: {seq_no}, failed after 3 attempts")

        seq_no += 1

    client_socket.close()
    end_time = time.time()

    # Summary information
    received_packets = responses
    lost_packets = sent_packets - received_packets
    loss_rate = (lost_packets / sent_packets) * 100
    max_rtt = max(rtts, default=0)
    min_rtt = min(rtts, default=0)
    avg_rtt = sum(rtts) / len(rtts) if rtts else 0
    rtt_std_dev = (sum((x - avg_rtt) ** 2 for x in rtts) / len(rtts)) ** 0.5 if rtts else 0
    total_response_time = end_time - start_time

    print("\nSummary:")
    print(f"Sent packets: {sent_packets}")
    print(f"Received packets: {received_packets}")
    print(f"Loss rate: {loss_rate:.2f}%")
    print(f"Max RTT: {max_rtt:.2f}ms")
    print(f"Min RTT: {min_rtt:.2f}ms")
    print(f"Avg RTT: {avg_rtt:.2f}ms")
    print(f"RTT Standard Deviation: {rtt_std_dev:.2f}ms")
    print(f"Total response time: {total_response_time:.2f}s")


if __name__ == "__main__":
    main()
