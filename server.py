import struct

import ntplib
import socket
import time

TIME1970 = 2208988800  # UNIX time - NTP time

fake_time_shift = 0
try:
    with open('conf.txt') as conf_file:
        fake_time_shift = int(conf_file.readline())
except Exception as e:
    print(f'Произошла ошибка: {e}')
finally:
    print(f'Установленное время сдвига: {fake_time_shift} сек.')

ntp = ntplib.NTPClient()

sock = socket.socket()
sock.bind(('', 123))
sock.listen(1)



while True:
    conn, addr = sock.accept()
    print('connected:', addr)
    data = conn.recv(1024)

    if not data:
        break
    request = ntp.request('time.windows.com')

    true_time = request.tx_time
    data = request.to_data()
    data_bytes = bytearray(data)

    new_time_data = struct.pack('!1I', TIME1970 + int(true_time) + fake_time_shift)
    new_time_data_bytes = bytearray(new_time_data)
    print(new_time_data_bytes)
    data_bytes[40:43] = new_time_data_bytes
    request.from_data(data_bytes)

    print(f'Время: {time.ctime(true_time)}')
    print(f'Время с установленным сдвигом: {time.ctime(request.tx_time)}')

    conn.send(data_bytes)


