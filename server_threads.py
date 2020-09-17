'''
Author: Kazybek Askarbek
Date: 17.09.20
Description: File receiving server
'''

import socket
import tqdm
import os
from threading import Thread


# Global Variables
HOST = '127.0.0.1'
PORT = 8800
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"


# functions to find available filenames
def get_available_filename(filename):
    new_filename = filename
    # variable to store number of copies
    copy_num = 0
    # get basename and extension of the file
    basename, *extension = filename.split('.')
    # in case file format of compound type join them into one string
    extension = '.'.join(extension)
    while os.path.isfile(new_filename):
        copy_num += 1
        # update filename
        new_filename = f"{basename}_copy{copy_num}.{extension}"

    return new_filename


# Class for Individual Thread Connections with Clients
class ClientListener(Thread):
    def __init__(self, sock: socket.socket):
        super().__init__(daemon=True)
        # assign received socket
        self.sock = sock

    # functions that will run the thread
    def run(self):
        # receive filename and filesize
        received = self.sock.recv(BUFFER_SIZE).decode()
        filename, filesize = received.split(SEPARATOR)
        # strip path from filename
        filename = os.path.basename(filename)
        filesize = int(filesize)

        # initialize progress bar
        progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024, leave=False)

        # get available filename
        new_filename = get_available_filename(filename)

        # receive and write data to a new file
        with open(new_filename, "wb") as f:
            for _ in progress:
                bytes_read = self.sock.recv(BUFFER_SIZE)
                if not bytes_read:
                    break
                f.write(bytes_read)
                progress.update(len(bytes_read))

        print(f"\n[*] File:{filename} Successfully Received\n")
        # close the client socket
        self.sock.close()


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # bind socket with HOST ip number and PORT number
        s.bind((HOST, PORT))
        # listen for connections
        s.listen()
        print(f"[*] Listening as {HOST}:{PORT}")

        while True:
            # if connection established
            conn, addr = s.accept()
            print(f"[*] Connected to {addr}")
            # start thread execution
            ClientListener(conn).start()
