from twisted.internet.protocol import ClientFactory,Protocol, Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor, task
import time
from collections import deque
import pygame

pygame.init()

class chatClient(LineReceiver):
    def __init__(self):
        self.message=None

    def connectionMade(self):
        print ("connected to server")

    def lineReceived(self,data):
        print (data)
        self.sendData()

    def sendData(self):
        data=input(">")
        if data is not None:
            data+='\r\n'
            self.transport.write(data.encode('utf-8'))
            #self.transport.loseConnection()
        #else:
        #    self.transport.loseConnection()

    def connectionLost(self, reason):
        print (reason)


class chatFactory(ClientFactory):
    def __init__(self):
        self.message=None
    def buildProtocol(self, addr):
        return chatClient()

class chatServerProtocol(LineReceiver):
    def __init__(self, users):
        self.users = users
        self.name = None
        self.state = "GETNAME"

    def connectionMade(self):
        self.sendLine(str("What player number are you?").encode('utf-8'))

    def connectionLost(self,reason):
        print ("Connection Lost")
    
    def lineReceived(self, line):
        if(self.state== "GETNAME"):
            self.handle_GETNAME(line)
        else:
            self.handle_CHAT(line)

    def handle_GETNAME(self,line):
        if line in self.users:
            self.sendLine("Player taken. Please choose a different player number")
            return
        message = str("Welcome Player %s"%(line,))
        self.sendLine(message.encode('utf-8'))
        self.name = line
        self.users[line]=self
        self.state="CHAT"
        print(message)

    def handle_CHAT(self,message):
        message = str("Player %s %s %s"%(self.name," : ",message,))
        for name, protocol in self.users.items():
            if protocol !=self:
                protocol.sendLine(message.encode('utf-8'))
        print (message)

class chatServerFactory(Factory):
    def __init__(self):
        self.users = {}

    def buildProtocol(self, addr):
        return chatServerProtocol(self.users)
