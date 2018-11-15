import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('', 8001))
data = u"안녕하세요2323".encode("UTF-8")
sock.send(data)
