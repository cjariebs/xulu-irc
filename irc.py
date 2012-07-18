"IRC Module for handling IRC stuff. Yay."

import socket

# [?] Initialize socket dictionary for corresponding hostnames with sockets
socks = {}

# [?] Init. receiving buf dict. for corresponding buffers to their sockets
buf = {}

def connect(host, port=6667):
	"Connect to a host on a port (defaults to 6667). Returns True on success."
	try:
		sock = socket.socket()
		sock.connect((host, port))

		global socks, buf
		socks[host] = sock
		buf[host] = ""
	# [?] Connection failed. Send the exception up
	except:
		raise
    
	return True

def host_lookup(host):
	"Look up a host in the socket dictionary. Returns None if not found"
	global socks
	return socks.get(host)

def send(host, data):
	"Send data to a host."
	sock = host_lookup(host)
	if sock == None:
		return None

	sock.setblocking(False)

	data = bytes(data + "\r\n", "utf-8")
	length = len(data)
	total = 0
	while True:
		sent = sock.send(data)
		total += sent
		data = data[sent:]
		if total >= length:
			break

	return data.decode()

def recv(host):
	"Receive data from a host."
	sock = host_lookup(host)
	if sock == None:
		return None
	# [?] Receive, decode, and put the data in its buf.
	global buf
	try:
	    sock.setblocking(False)
	    buf[host] += sock.recv(4096).decode()
	except UnicodeDecodeError:
		pass
	except socket.error:
	    return None
	# [?] The last part of the data is probably still being received.
	data = buf[host].split("\r\n")
	buf[host] = "".join(data[1:])

	# [?] Handle each line individually
	for i in data:
		i = i.strip()
		i = i.split(" ")

		# [?] Handle ping/pong automatically
		if i[0] == "PING":
			send(host, "PONG " + i[1])
			return None

		try:
			# [?] Check numeric commands
			int(i[0])
		except ValueError:
			# [?] Not a numeric
			hostmask = i[0]
			nick = hostmask[1:hostmask.find("!")]
			hostmask = hostmask[1+len(nick)+1:]

			command = i[1]
			to = i[2]
			payload = " ".join(i[3:])

			return (nick, hostmask, to, command, payload)
		else:
			# [?] Numeric
			n = i[1]

			# [?] Welcome! Connected successfully.
			if n == "001":
				return "<IRC_CONNECTED>"
			# [?] NAMES
			if n == "353":
				return "<IRC_NAMES> " + " ".join(i[5:])
			# [?] End of NAMES
			if n == "366":
				return "<IRC_ENDOFNAMES>"
