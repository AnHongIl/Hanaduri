import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 8001))
s.listen(0)
while True:
    client_socket, addr = s.accept()
    data = client_socket.recv(1024)
    print(data.decode('utf-8'))
    client_socket.close()
