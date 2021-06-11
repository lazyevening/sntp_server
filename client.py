import socket
import time

from ntplib import NTPStats

stats = NTPStats()

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.connect(('127.0.0.1', 123))
    sock.send('.'.encode())
    data = sock.recv(1024)

stats.from_data(data)
print(f'Время полученное пользователем: {time.ctime(stats.tx_time)}')
