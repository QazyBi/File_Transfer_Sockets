import socket
import tqdm
import os
import sys


HOST = sys.argv[2]
PORT = int(sys.argv[3])
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

try:
    filename = sys.argv[1]
    filesize = os.path.getsize(filename)
except OSError:
    print("File not found")
    sys.exit()
except IndexError:
    print("No filename provided")
    sys.exit()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.send(f'{filename}{SEPARATOR}{filesize}'.encode())

    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024, leave=False)
    with open(filename, "rb") as f:
        for _ in progress:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            # we use sendall to assure transimission in
            # busy networks
            s.sendall(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))
    # close the socket
    s.close()
