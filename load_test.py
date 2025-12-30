#!/usr/bin/env python3
import socket
import time
import threading

def send_requests():
    for i in range(100):
        try:
            s = socket.socket()
            s.connect(('localhost', 9000))
            s.sendall(b'X' * 1024)
            s.recv(1024)
            s.close()
        except:
            pass
        time.sleep(0.1)

# Crear múltiples threads
threads = []
for i in range(5):
    t = threading.Thread(target=send_requests)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("Carga completada")