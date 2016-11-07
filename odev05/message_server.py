import socket
import threading
import time
from multiprocessing import Queue

class LoggerThread (threading.Thread):
    def __init__(self, name, logQueue, logFileName):
        threading.Thread.__init__(self)
        self.name = name
        self.lQueue = logQueue
        # dosyayi appendable olarak ac    
        self.fid =open(logFileName, "a")
    def log(self,message):
        # gelen mesaji zamanla beraber bastir
        t = time.ctime()
        self.fid.write(t + ":"+ message+ "\n")
        self.fid.flush()
    def run(self):
        self.log("Starting " + self.name)
        while True:
            if not self.lQueue.empty():
                # lQueue'da yeni mesaj varsa
                # self.log() metodunu cagir
                to_be_logged = self.lQueue.get()
                self.log(to_be_logged)
        self.log("Exiting" + self.name)
        self.fid.close()
        
class ReadThread (threading.Thread):
    def __init__(self, name, csoc, address, threadQueue, logQueue):
        threading.Thread.__init__(self)
        self.name = name
        self.csoc = csoc
        self.address = address
        self.lQueue = logQueue
        self.fihrist = fihrist
        self.tQueue = threadQueue
    def parser(self):
        data =""
        data = data.strip()
        # henuz login olmadiysa
        if not self.nickname and not data[0:3] == "USR":
            response = "ERL"
            self.tQueue.put(None, None, response)
            self.csoc.send(response)         

        if data[0:3] == "USR":
            nickname = data[4:]
            if nickname not in self.fihrist.keys():
                # kullanici yoksa kabul et
                # fihristi guncelle ??
                self.fihrist[nickname].put()
                # yeni kullanici kabul edildiyse logla
                self.lQueue.put(nickname + "has joined")
                return 0
            else:
                # kullanici reddedilecek
                response = "REJ " + nickname
                self.tQueue.put(None, None, response)
                self.csoc.send(response)
                # baglantiyi kapat
                self.csoc.close()
                return 1
        elif data[0:3] == "QUI":
            response = "BYE " + self.nickname
            # fihristten sil
            del self.fihrist[self.nickname]
            # log gonder
            self.lQueue.put(self.nickname + "has left")
            self.tQueue.put(None, None, response)
            # baglantiyi kapat
            self.csoc.close()
            
        elif data[0:3] == "LSQ":
            for key in self.fihrist.keys():
                kullanici= key + ":"
            users= kullanici[:-1]
            response = "LSA " + users
            self.tQueue.put(None, None, response)            
            self.csoc.send(response)


        elif data[0:3] == "TIC":
            response = "TOK"
            self.tQueue.put(None, None, response)
            self.csoc.send(response)

            
        elif data[0:3] == "SAY":
            response = "SOK"
            self.tQueue.put(None, None, response)
            self.csoc.send(response)

            
        elif data[0:3] == "MSG":
            title, header = data.split() #title->MSG header-> ali:merhaba olur
            to_nickname, message= header.split(':') #to_nickname->ali message->merhaba
            if not to_nickname in self.fihrist.keys():
                response = "MNO"
                self.tQueue.put(None, None, response)
            else:
                queue_message = (to_nickname, self.nickname, message)
                # gonderilecek threadQueueyu fihristten alip icine yaz ?????
                self.fihrist[to_nickname].put(queue_message)
                response = "MOK"
                self.tQueue.put(to_nickname, self.nickname, response)
            self.csoc.send(response)
        else:
            # bir seye uymadiysa protokol hatasi verilecek
            response = "ERR"
            self.tQueue.put(None, None, response)
            self.csoc.send(response)


    def run(self):
        #pek anlayamadım bu kısmı hocam
        self.lQueue.put("Starting " + self.name)
        while True:
            l=threading.Lock()
            l.acquire()
            # burasi blocking bir recv halinde duracak
            # gelen protokol komutlari parserdan gecirilip
            # ilgili hareketler yapilacak
            incoming_data= self.csoc.recv(1024)
            queue_message = self.parser(incoming_data)
            # istemciye cevap hazirla.??
            response= queue_message
            # cevap veya cevaplari gondermek uzere
            # threadQueue'ya yaz
            self.tQueue.put(None, None, response)
            # lock mekanizmasini unutma
            l.release()

class WriteThread (threading.Thread):
    def __init__(self, name, csoc, address, threadQueue, logQueue ):
        threading.Thread.__init__(self)
        self.name = name
        self.csoc = csoc
        self.address = address
        self.lQueue = logQueue
        self.tQueue = threadQueue
    def run(self):
        self.lQueue.put("Starting " + self.name)
        while True:
            if not self.tQueue.empty():
                # burasi kuyrukta sirasi gelen mesajlari
                # gondermek icin kullanilacak
                queue_message = self.threadQueue.get()
                # buraya gelen mesaj (<to>, <from>, <msg>) seklinde olacak
                # ayristirmak gerekiyor
                # gonderilen ozel mesajsa
                if queue_message[0] and queue_message[1]:
                    message_to_send = "MSG " + queue_message[1] + ":" + queue_message[2]
                # genel mesajsa
                elif queue_message[1] and not queue_message[0]:
                    message_to_send = "SAY " + queue_message[1] + ":" + queue_message[2]
                    # hicbiri degilse sistem mesajidir
                else:
                    message_to_send = "SYS " + queue_message[2]
                self.csoc.send(message_to_send)
        self.lQueue.put("Exiting " + self.name)
        self.csoc.close()
        

#main kısmı
logQueue= Queue()
threadQueue= Queue()
fihrist={}
threadCounter=1

logthread= LoggerThread("LoggerThread", logQueue, "log.txt")
logthread.start()

s = socket.socket()
host = "localhost"
port = 12345
s.bind((host, port))
s.listen(5)
while True:
    logQueue.put("Waiting for connection")
    print "Waiting for connection"
    c, addr = s.accept()
    print 'Got a connection from ', addr
    logQueue.put("Got a connection from"+ str(addr))
    threadQueue= Queue()
    #içlerini doldur idil
    readthread= ReadThread("ReadThread"+ threadCounter, c, addr, threadQueue, logQueue)
    writethread= WriteThread("WriteThread"+ threadCounter, c, addr, threadQueue, logQueue)
    threadCounter += 1
    readthread.start()
    writethread.start()

    