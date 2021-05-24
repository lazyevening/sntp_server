import socket
import time

from ntplib import NTPStats

stats = NTPStats()

with socket.socket() as sock:
    sock.connect(('localhost', 123))
    sock.send('HLO'.encode())
    data = sock.recv(1024)

stats.from_data(data)
print(f'Время полученное пользователем: {time.ctime(stats.tx_time)}')
