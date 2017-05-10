from twisted.internet.protocol import ClientFactory,Protocol, Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor, task
import time
from collections import deque
import pygame

pygame.init()

class chatClient(LineReceiver):

'''The protocol for the client side'''

    def __init__(self):
        self.message=None

    def connectionMade(self):
        print ("connected to server")

    def lineReceived(self,data):
        print (data)
        self.sendData()

    def sendData(self):     # send data (i.e. chat message) to the server
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

'''The factory for the client side'''

    def __init__(self):
        self.message=None
    def buildProtocol(self, addr):
        return chatClient()

class chatServerProtocol(LineReceiver):

'''The protocol for the serve side'''

    def __init__(self, users):
        self.users = users
        self.name = None
        self.state = "GETNAME"      # stores whether we're getting a player number, or chat message

    def connectionMade(self):       # Asks the player what number (1-4) they are
        self.sendLine(str("What player number are you?").encode('utf-8'))

    def connectionLost(self,reason):
        print ("Connection Lost")

    def lineReceived(self, line):       # Calls appropriate function to handle message
        if(self.state== "GETNAME"):
            self.handle_GETNAME(line)
        else:
            self.handle_CHAT(line)

    def handle_GETNAME(self,line):      # function to get player number from client
        if line in self.users:          # check what player numbers are still available
            self.sendLine("Player taken. Please choose a different player number")
            return
        message = str("Welcome Player %s"%(line,))
        self.sendLine(message.encode('utf-8'))
        self.name = line
        self.users[line]=self
        self.state="CHAT"
        print(message)

    def handle_CHAT(self,message):      # function to get chat messages from client
        message = str("Player %s %s %s"%(self.name," : ",message,))
        for name, protocol in self.users.items():
            if protocol !=self:
                protocol.sendLine(message.encode('utf-8'))
        print (message)

class chatServerFactory(Factory):

'''Factory for the server side'''

    def __init__(self):
        self.users = {}

    def buildProtocol(self, addr):
        return chatServerProtocol(self.users)
