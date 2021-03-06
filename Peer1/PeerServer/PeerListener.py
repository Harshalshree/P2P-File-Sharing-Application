import os
import pickle
import threading
from socket import *
from threading import Semaphore

PORT = int(5555)
HOST = 'localhost'
REGISTER = '1'
SEARCH = '2'
DOWNLOAD = '3'
LIST_ALL = '4'
EXIT = '5'


class PeerListener(threading.Thread):
    def __init__(self, port, host, max_connection):
        threading.Thread.__init__(self)
        self.host = host
        self.semaphore = Semaphore(max_connection)  # For Handling threads synchronization
        self.port = port  # this port it will listen to
        self.sock = socket()
        self.sock.bind((self.host, self.port))  # bind socket to address
        self.sock.listen(max_connection)

    def run(self):
        print("And This Peer is Ready For Sharing his File\n")
        while True:
            conn, addr = self.sock.accept()
            print("Got Connection From ", addr[0], " : ", addr[1])
            request = pickle.loads(conn.recv(1024))
            if request[0] == DOWNLOAD:  # Organizing the path of file that will be shared
                file_path = os.path.join(os.getcwd(), '..')
                file_path = os.path.join(file_path, 'SharingFiles')
                file_path = os.path.join(file_path, "Uploads")
                file_name = request[1]
                Full_path = os.path.join(file_path, file_name)
                self.semaphore.acquire()

                with open(Full_path, "rb") as myfile:       # Start Transfer File to Other Peer
                    while True:
                        l = myfile.read(2014)
                        while (l):
                            conn.send(l)
                            l = myfile.read(1024)
                        if not l:
                            myfile.close()
                            conn.close()
                            break
                self.semaphore.release()
                print('File Sent')
            else:
                continue


def Start_PeerListener(port, host):
    peer = PeerListener(port, host, 5)  # Start Thread listen to peer_id to share the files with others Peers
    peer.start()
