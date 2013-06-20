# Echo server program
import socket

HOST = ''                 # Symbolic name meaning the local host
PORT = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print 'Connected by', addr

while 1:
	#if not data:
	try:
		data = conn.recv(1024)
	except Exception:
		print "Client left"
		conn, addr = s.accept()
	#conn.send(data)
	print data	

conn.close()
