'''
Author: Kazybek Askarbek
Date: 17.09.20
Description: File uploading client
'''

import socket
import tqdm
import os
import sys


# Global variables
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"


# handle exceptions
try:
    filename = sys.argv[1]
    HOST = sys.argv[2]
    PORT = int(sys.argv[3])

    filesize = os.path.getsize(filename)
except OSError:
    print("File not found")
    sys.exit()
except IndexError:
    print("Not enough arguments passed")
    print("Please provide: filename hostname port")
    sys.exit()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # connect to the server
    s.connect((HOST, PORT))
    # send filename and filesize to the server
    s.send(f'{filename}{SEPARATOR}{filesize}'.encode())

    # initialize progress bar
    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024, leave=False)
    with open(filename, "rb") as f:
        for _ in progress:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # if no bytes read then stop
                break
            # send file to the server
            s.sendall(bytes_read)
            # update progress bar
            progress.update(len(bytes_read))
    # close the socket
    s.close()
