import socket
import threading

class readThread (threading.Thread):
#kullanıcıdan giriş bekleyip sunucuya gönder
    def __init__(self, threadID, clientSocket, msg):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.clientSocket = clientSocket
        self.msg = msg
    def run(self):
            self.clientSocket.send(msg)
                  
class writeThread (threading.Thread):
#gelen mesajlları bastır
    def __init__(self, threadID, clientSocket):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.clientSocket = clientSocket
    def run(self):
        print self.clientSocket.recv(1024)

s = socket.socket()
host = "127.0.0.1"
port = 12345
s.connect((host, port))

wThread = writeThread(2,s)
wThread.start()

msg=''
msg=raw_input()
if msg:
    while("END" not in msg): 
        rThread = readThread(1,s, msg)
        rThread.start()
    s.close()
    rThread.join()
    wThread.join()

