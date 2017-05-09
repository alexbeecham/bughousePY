from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
import time
from collections import deque
class DataProtocol(Protocol): # protocol that reads the player's sent data
    def __init__(self,queue,players,moves):
        self.queue = queue
        self.players=players
        self.moves=moves
    def connectionMade(self):
        if(len(self.players>0)): # if players have not joined the game yet
            print("Players 1 and 2 are a team. Players 3 and 4 are a team. Players 1 and 4 will play against each other. Players 2 and 3 will play against each other. Please pick from the available players: "+self.players)
        else: # otherwise, data sent is a move
            self.transport.write(queue[moveCount])
    def dataReceived(self, data):
        if(data!=""):
            self.queue.append(data)
            moves+=1
        time.sleep(.5)
        reactor.stop()



class Server(Factory): # factory that reads and sends players information
    def __init__(self,queue,players,moves):
        self.queue = queue
        self.players = players
        self.moveCount = moves
    def buildProtocol(self):
        return DataProtocol(self.queue,self.players, self.moveCount)

if __name__=="__main__":
    dataQueue = deque()
    players = [1,2,3,4]
    while(len(players)>0): #while waiting for players to join      
        factory = Server(dataQueue,players,0)
        reactor.listenTCP(8000, factory) #listen for player to enter their number
        reactor.run()
        for elem in dataQueue:
            players.remove(int(elem))
    dataQueue = deque()
    moveCount=0
    while(1): # runs the game passing moves from player to player and from board to board
        factory = Server(dataQueue,players,moveCount)
        reactor.listenTCP(8000, factory)
        reactor.run()
        
        

        
