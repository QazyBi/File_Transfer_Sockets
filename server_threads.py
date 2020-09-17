import socket
import tqdm
import os
from threading import Thread


HOST = '127.0.0.1'
PORT = 8800
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

clients = []


def get_available_filename(filename):
    new_filename = filename
    copy_num = 0
    basename, *extension = filename.split('.')
    extension = '.'.join(extension)
    while os.path.isfile(new_filename):
        copy_num += 1
        new_filename = f"{basename}_copy{copy_num}.{extension}"

    return new_filename


class ClientListener(Thread):
    def __init__(self, sock: socket.socket):
        super().__init__(daemon=True)
        self.sock = sock

    def run(self):
        # print(f"[+] {addr} is connected.")
        received = self.sock.recv(BUFFER_SIZE).decode()
        filename, filesize = received.split(SEPARATOR)
        filename = os.path.basename(filename)
        filesize = int(filesize)

        progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024, leave=False)

        new_filename = get_available_filename(filename)

        with open(new_filename, "wb") as f:
            for _ in progress:
                # read 1024 bytes from the socket (receive)
                bytes_read = self.sock.recv(BUFFER_SIZE)
                if not bytes_read:
                    # nothing is received
                    # file transmitting is done
                    break
                # write to the file the bytes we just received
                f.write(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))

        print(f"\n[*] File:{filename} Successfully Received\n")
        # close the client socket
        self.sock.close()


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[*] Listening as {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            print(f"[*] Connected to {addr}")
            clients.append(conn)
            ClientListener(conn).start()
