import socket
import tqdm
import os


HOST = '127.0.0.1'
PORT = 8800
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((HOST, PORT))
	s.listen()
	print(f"[*] Listening as {HOST}:{PORT}")
	conn, addr = s.accept()
	with conn:
		print(f"[+] {addr} is connected.")
		received = conn.recv(BUFFER_SIZE).decode()
		filename, filesize = received.split(SEPARATOR)
		filename = os.path.basename(filename)
		filesize = int(filesize)
		
		progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024, leave=False)

		with open(filename, "wb") as f:
		    for _ in progress:
		        # read 1024 bytes from the socket (receive)
		        bytes_read = conn.recv(BUFFER_SIZE)
		        if not bytes_read:    
		            # nothing is received
		            # file transmitting is done
		            break
		        # write to the file the bytes we just received
		        f.write(bytes_read)
		        # update the progress bar
		        progress.update(len(bytes_read))

		# close the client socket
		conn.close()
		# close the server socket
		s.close()						
