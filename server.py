import socket
import threading
import platform
import urllib.request
import datetime
import mysql.connector
from MySQLdb._mysql import Error

from xml.dom import minidom

import tensorflow
from tensorflow.keras.models import Sequential
from tensorflow.keras import utils
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LeakyReLU

import numpy as np
from tensorflow.python.keras.models import load_model


class Client:
    _username = ""
    _userthread = ""

    def __init__(self, socket):
        self._handler = socket
        _userthread = threading.Thread(target=self.listner)
        _userthread.start()

    def username(self):
        return self._username

    def parseData(self, sdata):
        data = bytearray(sdata)
        if len(data) < 7: return 0
        if (data[0] != 0xAF or data[1] != 0xAA or data[2] != 0xAF):
            print('not')
            return 0
        mIndex = len(data) - 1
        if (data[mIndex - 1] != 0xFF or data[mIndex] != 0x00):
            print('not')
            return 0
        type = data[3]
        subtype = data[4]
        data.remove(data[0])
        data.remove(data[0])
        data.remove(data[0])
        data.remove(data[0])
        data.remove(data[0])
        if len(data) == 2: return 0
        id = data[0]
        size = data[1]
        data.remove(data[0])
        data.remove(data[0])
        mIndex = len(data) - 1
        if size != 0:
            data.remove(data[mIndex])
            data.remove(data[mIndex - 1])

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
                print("fail listener", p)
                server.endclient(self)
                return

    def end(self, client):
        try:
            self._handler.close()
            try:
                self._userthread.abort()
            except:
                print("")
        except Exception as e:
            print("Error With the end: {0}.", e)

    def handle_command(self, data):
        # if "#setname" in data:
        # self._username = data.split('&', 1)
        # self.updatechat()
        # return
        if "#newmsg" in data:
            msg = data.split('&', 1).pop(1)
            datapr = "".join(msg).split('%')
            datapr[0] = int(datapr[0])
            datapr[1] = int(datapr[1])
            datapr[2] = int(datapr[2])
            datapr[3] = int(datapr[3])
            datapr[4] = int(datapr[4])
            datapr[5] = int(datapr[5])
            dataIn = np.array(datapr).reshape(1, 6)
            # db =MySQLdb.connect("localhost","root","93154000lR","chat")
            # cursor = db.cursor()
            # sql ="INSERT INTO log(text, username,date)\
            # values('%s','%s',current_timestamp)"%\
            #     (msg[1],self._username[1])
            # try:
            #   cursor.execute(sql)
            #    db.commit()
            # except Exception as e:
            #   db.rollback()
            #    print('here',e)
            # db.close()
            # chatc.addmessage(self._username[1], msg[1])
            try:
                # print("#newresponse&" + neural.makePredict(dataIn))
                self.send("#newresponse&" + neural.makePredict())
            except Exception as e:
                print("Wrong data structure: {0}.", e)

            return

    def updatelog(self):
        self.send(chatc.getlog())

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

    # def updatallchats(self):
    #   try:
    #      for key in self.clients:
    #           key.updatechat()
    #   except Exception as e:
    #      print("Error with update all chats: {0}.", e)


class NeuralNetwork:
    model = []
    income_model = []
    std = []
    mean = []
    vallet_inputs = []

    def __init__(self):
        self.income_model = load_model('valletTestClass.h5',
                                       custom_objects={'LeakyReLU': tensorflow.keras.layers.LeakyReLU})
        self.income_model.summary()
        # f = open('mean_std_metadata2.txt', 'r')
        # self.std = f.readline()
        # self.std = np.asarray(self.std.split('%'))
        # self.mean = f.readline()
        # self.mean = np.asarray(self.mean.split('%'))
        # self.std = np.delete(self.std, 7)
        # self.mean = np.delete(self.mean, 7)
        # self.mean = np.asfarray(self.mean, float)
        # 3self.std = np.asfarray(self.std, float)

        # f.close()

    def saverequest(self, inputs, prediction):

        conn = ''
        day14 = float(inputs[0])
        day13 = float(inputs[1])
        day12 = float(inputs[2])
        day11 = float(inputs[3])
        day10 = float(inputs[4])
        day9 = float(inputs[5])
        day8 = float(inputs[6])
        day7 = float(inputs[7])
        day6 = float(inputs[8])
        day5 = float(inputs[9])
        day4 = float(inputs[10])
        day3 = float(inputs[11])
        day2 = float(inputs[12])
        day1 = float(inputs[13])
        day0 = float(inputs[14])
        today = datetime.datetime.today()
        today = today.strftime("%d") + "/" + today.strftime(
            "%m") + "/" + today.strftime("%Y")
        query = "INSERT INTO cources(day,input_1,input_2,input_3,input_4,input_5,input_6,input_7,input_8,input_9,input_10,input_11,input_12,input_13,input_14,input_15,prediction,checked) " + "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        args = (today, day14, day13, day12, day11, day10, day9, day8, day7, day6, day5, day4, day3, day2, day1, day0,
                int(prediction), int(0))
        try:
            conn = mysql.connector.connect(host='localhost',
                                           database='bank',
                                           user='root',
                                           password='93154000lR')
            if conn.is_connected():
                print('Connected to MySQL database')
            cursor = conn.cursor(buffered=True)
            cursor_m = conn.cursor(prepared=True)
            cursor_2 = conn.cursor(buffered=True)
            cursor.execute('SELECT COUNT(*) FROM cources')
            (is_null,) = cursor.fetchone()
            if (is_null is not None):
                today_date = datetime.datetime.today()
                cursor_2.execute('SELECT day FROM cources ORDER BY req_id DESC LIMIT 1')
                (is_today,) = cursor_2.fetchone()
                if (is_today != (today_date.strftime(
                        "%d") + "/" + today_date.strftime(
                    "%m") + "/" + today_date.strftime("%Y"))):
                    cursor_m.execute(query, args)
                    if cursor_m.lastrowid:
                        print('last insert id', cursor_m.lastrowid)
                    else:
                        print('last insert id not found')
            else:
                cursor_m.execute(query, args)
                if cursor_m.lastrowid:
                    print('last insert id', cursor_m.lastrowid)
                else:
                    print('last insert id not found')

            conn.commit()
            cursor.close()
            cursor_2.close()
            cursor_m.close()
            conn.close()
        except Error as error:
            print(error)

    def parceCourse(self):
        print("here")
        self.vallet_inputs = []
        now = datetime.datetime.today()
        i = 0
        while (i < 15):
            url = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + now.strftime("%d") + "/" + now.strftime(
                "%m") + "/" + now.strftime("%Y") + ""
            webFile = urllib.request.urlopen(url)
            data = webFile.read()
            # UrlSplit = url.split("/")[-1]
            # ExtSplit = UrlSplit.split(".")[1]
            FileName = "vallet.xml"
            with open(FileName, "wb") as localFile:
                localFile.write(data)
            webFile.close()
            doc = minidom.parse(FileName)
            # root = doc.getElementsByTagName("ValCurs")[0]
            currency = doc.getElementsByTagName("Valute")
            for rate in currency:
                charcode = rate.getElementsByTagName("CharCode")[0].firstChild.data
                value = rate.getElementsByTagName("Value")[0].firstChild.data
                if charcode == 'USD':
                    self.vallet_inputs = self.vallet_inputs + [float(value.replace(",", "."))]
            i = i + 1
            now = now - datetime.timedelta(days=1)
        self.vallet_inputs = np.array(self.vallet_inputs[::-1]).reshape(1, 15)

    def makePredict(self):
        self.parceCourse()
        income = self.income_model.predict(self.vallet_inputs)[0]
        if (income[0] > income[1]):
            income = 0
        else:
            income = 1
        self.saverequest(self.vallet_inputs[0], income)
        return str(income)


class ServerController:
    log = []
    _maxlog = 1000

    def __init__(self):
        self._maxmessage = 1000
        self.log = []

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
            data = "#updatelog&"
            countmessage = len(self.log)
            if countmessage <= 0: return ""
            for key in self.chat:
                data += "{0}~{1}|".format(key.returnname(), key.returnmessage())
            return data
            print("getlog success")
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
            user, addr = sock.accept()
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
        # shutdown_socket(server)


OS_NAME = platform.system()
connections = set()
server = Server()
chatc = ServerController()
neural = NeuralNetwork()
_serverthread = threading.Thread(target=startserver)
_controllerthread = threading.Thread(target=console)
_controllerthread.start()
_serverthread.start()
