import socket
import threading
import platform


class Client:
    _username = ""
    _userthread =""
    def __init__(self, socket):
        self._handler = socket
        _userthread = threading.Thread(target=self.listner)
        _userthread.start()

    def username(self):
        return self._username
    def parseData(self,sdata):
        data = bytearray(sdata)
        if len(data)<7: return 0
        if (data[0] != 0xAF or data[1]!=0xAA or data[2]!=0xAF):
            print('not')
            return 0
        mIndex = len(data)-1
        if (data[mIndex-1] != 0xFF or data[mIndex] != 0x00):
            print('not')
            return 0
        type = data[3]
        subtype = data[4]
        data.remove(data[0])
        data.remove(data[0])
        data.remove(data[0])
        data.remove(data[0])
        data.remove(data[0])
        if len(data)==2:return 0
        id = data[0]
        size = data[1]
        data.remove(data[0])
        data.remove(data[0])
        mIndex = len(data)-1
        if size!=0:
            data.remove(data[mIndex])
            data.remove(data[mIndex-1])

        return data



    def listner(self):
        while 1:
            try:
                proxydata = self._handler.recv(1024)
                data = self.parseData(proxydata)
                # print(addres[0], addres[1])
                self.handle_command(data.decode('utf-8'))
                print("active listener")
            except Exception as p:
                print("fail listener",p)
                server.endclient(self)
                return

    def end(self,client):
        try:
            self._handler.close()
            try:
                self._userthread.abort()
            except:
                print("")
        except Exception as e:
            print("Error With the end: {0}.", e)

    def handle_command(self, data):
        if "#setname" in data:
            self._username = data.split('&', 1)
            self.updatechat()
            return
        if "#newmsg" in data:
            msg = data.split('&', 1)
            #db =MySQLdb.connect("localhost","root","93154000lR","chat")
            #cursor = db.cursor()
            #sql ="INSERT INTO log(text, username,date)\
            #values('%s','%s',current_timestamp)"%\
            #     (msg[1],self._username[1])
            #try:
             #   cursor.execute(sql)
            #    db.commit()
            #except Exception as e:
             #   db.rollback()
            #    print('here',e)
            #db.close()
            chatc.addmessage(self._username[1], msg[1])
            return

    #Def updatechat(self):
     #   self.send(chatc.getchat())

    def send(self, command):
        try:
            bytesent = self._handler.send(command.encode('utf-8'))
            if bytesent > 0:
                print("Success")
        except Exception as e:
            print("Error with Send Command: {0}.", e)
            server.endclient(self)


class Server:
    clients = []

    def __init__(self):
        self.clients = []

    def newclient(self, handle):
        try:
            newclient = Client(handle)
            self.clients.append(newclient)
            # may be problem
            # data, addres = handle.recvfrom(1024)
            print("New Client Connected: {0}")  # addres
        except Exception as e:
            print("Error with adding new client: {0}.", e)

    def endclient(self, client):
        try:
            client.end(client)
            self.clients.remove(client)
            print("User {0} has been disconnected", client.username())
        except Exception as e:
            print("Error with end client: {0}.", e)

    #def updatallchats(self):
     #   try:
      #      for key in self.clients:
     #           key.updatechat()
     #   except Exception as e:
      #      print("Error with update all chats: {0}.", e)


class ServerController:
    log =[]
    _maxlog =1000
    def __init__(self):
        self._maxmessage = 1000
        self.chat = []

   # def addmessage(self, username, msg):
      #  try:
         #   if not username or not msg:
         #       return
         #   countmessages = len(self.chat)
         #   if countmessages > self._maxmessage: self.clearchat()
         #   newmessage = message(username, msg)
        #    self.chat.append(newmessage)
         #   print("New message from {0}.", username)
         #   server.updatallchats()
       # except Exception as e:
         #   print("Error with adding message: {0}.", e)

    def clearlog(self):
        self.chat.clear()

    def getlog(self):
        try:
            data = "#updatechat&"
            countmessage = len(self.chat)
            if countmessage <= 0: return ""
            for key in self.chat:
                data += "{0}~{1}|".format(key.returnname(), key.returnmessage())
            return data
            print("getchat success")
        except Exception as e:
            print("Error with get chat: {0}.", e)


class message:
    def __init__(self, name, msg):
        self.usrname = name
        self.data = msg

    def returnmessage(self):
        return self.data

    def returnname(self):
        return self.usrname


# def handlercommand():
def startserver():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("", 9933))
    sock.listen(1000)
    print("Server has been started")
    while 1:
        try:
            user,addr = sock.accept()
            connections.add(user)
            server.newclient(user)
        except Exception as e:
            print("Error: {0}", e)
def shutdown_socket(s):
    if OS_NAME == 'Linux':
        s.shutdown(socket.SHUT_RDWR)
    s.close()
def console():
    while 1:
        command = input()
        if command == 'exit':
            break
    print("exiting")
    for s in connections:
        shutdown_socket(s)
        #shutdown_socket(server)


OS_NAME= platform.system()
connections = set()
server = Server()
chatc = ServerController()
_serverthread = threading.Thread(target=startserver)
_controllerthread = threading.Thread(target=console)
_controllerthread.start()
_serverthread.start()