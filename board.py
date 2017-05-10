import pygame
import sys
from images import *
from player import *
from piece import *
from pygame.locals import*
from twisted.internet.protocol import ClientFactory,Protocol
from twisted.internet.task import LoopingCall
from twisted.internet import reactor
import time
from collections import deque
from chatFactory import *


class GameClient(Protocol): #client that sends moves made to the server
    def __init__(self,message,queue,firstRun):
        self.queue=queue
        self.message=message
        self.firstRun=firstRun
    def connectionMade(self):
        self.transport.write(self.message)
    def dataReceived(self,data):
        self.queue.append(data)
        self.transport.loseConnection()
        time.sleep(.2)
        if(self.firstRun):
            time.sleep(5)
        reactor.stop

class InitialClient(Protocol): # client used to set up the game
    def __init__(self,queue):
        self.queue = queue
        self.message=None
    def connectionMade(self):
        string = ''
        self.transport.write(string.encode('utf-8'))
        print("connection made")
        time.sleep(10)
    def lineReceived(self,line):
        self.queue.append(line)
        time.sleep(10)
        reactor.stop()

class GameFactory(ClientFactory): #factory that connects to the game server
    def __init__(self,message,queue,firstRun):
        self.message = message
        self.queue = queue
        self.firstRun = firstRun
    def buildProtocol(self,addr):
        if(self.firstRun):
            print("on first run")
            return InitialClient(self.queue)
        else:
            return GameClient(self.message,self.queue,self.firstRun)
    def clientConnectionFailed(self,connector, reason):
        print("Connection has failed")
        reactor.stop()
    def clientConnectionLost(self,connector, reason):
        print("Connection has been lost")
        reactor.stop()



class Board():
    def __init__(self, n, offset):


        self.length = n
        self.white = Player("WHITE")
        self.black = Player("BLACK")
        self.offset = offset #0 for the board you are playing on 1000 for the other board
        self.blackLoses=[] # holds the pieces lost by the black player
        self.whiteLoses=[] # holds the pieces lost by the white player

    def draw_pieces(self, surface,black,white): #draws the pieces for the black and white players provided
        #print(len(self.white.pieces))

        for piece in black.pieces: #draw all the black pieces
            x = self.length/8 * piece.xCoord+self.offset
            y = self.length/8 * piece.yCoord
            img = pieceimages[piece.image] # reference the pieceimages dict from images
            surface.blit(img, (x+13,y+13)) # shifts pieces over 13 pixels so they are centered in square

        for piece in white.pieces: #same process as above but for white pieces
            x = self.length/8 * piece.xCoord+self.offset
            y = self.length/8 * piece.yCoord
            img = pieceimages[piece.image]
            surface.blit(img, (x+13,y+13))

    def sendMove(self,piece,x,y): #sends the made move to the server
        queue = deque()
        move = str(self.player)+","+str(piece.xCoord)+","+str(piece.yCoord)+","+str(x)+","+str(y) #encodes move in format of playerNum,startX,startY,endX,endY
        reactor.connectTCP("localhost",8000,GameFactory(move,queue,False)) # sends move to server
        reactor.run()

    def getMove(self,otherBoard): # gets move that was made from server
        queue = deque()
        reactor.listenTCP(8000,GameFactory("",queue,False))
        reactor.run()
        move = queue[0]
        if(move is not None): # if a move was made
            data = move.split(',') #splits string into relevant pieces
            player = int(data[0])
            if(self.opponentNumber): #if the move was made by my opponent
                makeMove(player,int(data[1]),int(data[2]),int(data[3]),int(data[4])) #makes the move on my board
                return None
            else: #otherwise, updates the otherboard and returns it
                otherBoard.makeMove(player,int(data[1]),int(data[2]),int(data[3]),int(data[4]))
                return otherBoard
        else: #not move was made
            return None

    def makeMove(self,player,x1,y1,x2,y2): #makes updates the piece at x1,y1 and moves it to x2,y2
        if(player==1 or player==3): # players 1 and 3 are white players
            piece = self.white.get_piece_at(x1,y1)
            piece.xCoord=x2
            piece.yCoord=y2
            self.black.remove_piece_at(x2,y2) # in case a piece is taken have black remove any piece it has at x2,y2
        else: #players 2 and 4 are black players
            piece = self.black.get_piece_at(x1,y1)
            piece.xCoord=x2
            piece.yCoord=y2
            self.white.remove_piece_at(x2,y2) #in case a piece is taken, have white remove any piece at x2,y2


    def flipBoard(self): #flips the board. 
        p1 = self.white
        p2 = self.black
        for piece in p1.pieces: # flips the y coordinates of the black pieces
            if(piece.yCoord==0):
                piece.yCoord=7
            elif(piece.yCoord==1):
                piece.yCoord=6
            elif(piece.yCoord==2):
                piece.yCoord=5
            elif(piece.yCoord==3):
                piece.yCoord=4
            elif(piece.yCoord==4):
                piece.yCoord=3
            elif(piece.yCoord==5):
                piece.yCoord=2
            elif(piece.yCoord==6):
                piece.yCoord=1
            else:
                piece.yCoord=0
        for piece in p2.pieces: #flips the y coordinates of the black pieces
            if(piece.yCoord==0):
                piece.yCoord=7
            elif(piece.yCoord==1):
                piece.yCoord=6
            elif(piece.yCoord==2):
                piece.yCoord=5
            elif(piece.yCoord==3):
                piece.yCoord=4
            elif(piece.yCoord==4):
                piece.yCoord=3
            elif(piece.yCoord==5):
                piece.yCoord=2
            elif(piece.yCoord==6):
                piece.yCoord=1
            else:
                piece.yCoord=0

        return p1,p2
    def drawBoard(self, surface): # only called for the board on the right side of the screen. This flips and draws the board on the surface
        colors=[(255,0,0),(0,0,255)]
        n = 8
        sq_sz = self.length/n
        for row in range(n): #draws the grid in red and blue
            c_indx = row % 2
            for col in range(n):
                    the_square = (col*sq_sz+self.offset, row*sq_sz, sq_sz, sq_sz)
                    surface.fill(colors[c_indx], the_square)
                    c_indx = (c_indx + 1) % 2
        p1,p2 = self.flipBoard() # gets players with y coordinates of pieces flipped

        self.draw_pieces(surface,p2,p1) # draws the pieces on the board
        return surface

    def clearPath(self,piece,x,y): #makes sure there are no pieces between where you are and where you want to go. Does not check the actual target space because isLegalMove already does that
        px = piece.xCoord # piece to be moved current x coordinate
        py = piece.yCoord # piece to be moved current y coordinate
        if(piece.pieceType=='Horse'): # if the piece is a knight, it ignores collision
            return True
        elif(x==px and y!=py): # vertical movement check
            if(py<y): #moving down
                py+=1 # simulates moving the piece one step forward
                while(py<y): #while the piece has not arrived one step from its destination
                    if(self.white.get_piece_at(x,py) is not None or self.black.get_piece_at(x,py) is not None): #if a piece of either color is found
                        return False
                    py+=1 #move to the next space on the path
            else: #moving up
                py-=1
                while(py>y):
                    if(self.white.get_piece_at(x,py) is not None or self.black.get_piece_at(x,py) is not None):
                        return False
                    py-=1
            return True #if no obstruction is found return true
        elif(y==py and x!=px): # horizontal movement check
            if(px<x): # piece is moving to the right
                px+=1
                while(px<x):
                    if(self.white.get_piece_at(px,py) is not None or self.black.get_piece_at(px,py) is not None):
                        return False
                    px+=1
            else: # piece is moving to the left
                px-=1
                while(px>x):
                    if(self.white.get_piece_at(px,y) is not None or self.black.get_piece_at(px,py) is not None):
                        return False
                    px-=1
            return True
        elif(px>x and py>y): # piece is moving left and up
            px-=1
            py-=1
            while(px>x):
                if(self.white.get_piece_at(px,py) is not None or self.black.get_piece_at(px,py) is not None):
                    print(str(px)+" "+str(py))
                    return False
                px-=1
                py-=1
            return True
        elif(px<x and py>y): # piece is moving right and up
            px+=1
            py-=1
            while(px<x):
                if(self.white.get_piece_at(px,py) is not None or self.black.get_piece_at(px,py) is not None):
                    print(str(px)+" "+str(py))
                    return False
                px+=1
                py-=1
            return True
        elif(px>x and py<y): # piece is moving left and down
            px-=1
            py+=1
            while(px>x):
                if(self.white.get_piece_at(px,py) is not None or self.black.get_piece_at(px,py) is not None):
                    print(str(px)+" "+str(py))
                    return False
                px-=1
                py+=1
            return True
        elif(px<x and py<y): # piece is moving right and down
            px+=1
            py+=1
            while(px<x):
                if(self.white.get_piece_at(px,py) is not None or self.black.get_piece_at(px,py) is not None):
                    print(str(px)+" "+str(py))
                    return False
                px+=1
                py+=1
            return True
        return False

    def play_board(self, otherBoard,clickedPiece): #draws and plays the game
        pygame.init()
        colors = [(255, 0, 0), (0, 0, 255)]

        n = 8
        sq_sz = self.length / n
        #clickedPiece = None # holds the piece selected by the player
        surface = pygame.display.set_mode((2*self.length+200, self.length))
        currentPlayer = "WHITE"
        surface = otherBoard.drawBoard(surface) # draws the other board

        while True:
            for row in range(n): #draw the board the player is acting on
                c_indx = row % 2
                for col in range(n):
                    the_square = (col*sq_sz,  row*sq_sz, sq_sz, sq_sz)
                    surface.fill(colors[c_indx], the_square)
                    c_indx = (c_indx + 1) % 2

            self.draw_pieces(surface,self.black,self.white) #draw the pieces the player is playing with
            ev = pygame.event.get() # if there is a button pressed or a mouse click
            for event in ev:
                '''if event.type == pygame.KEYDOWN:
                    if event.key==K_RETURN:
                        message = input(">")
                        factory = chatFactory(message)
                        reactor.connectTCP("localhost",8000,factory)
                '''        
                if event.type == pygame.MOUSEBUTTONUP: #if the mouse is pressed
                    #convert the mouse click position to grid coordinates
                    pos = pygame.mouse.get_pos()
                    x = pos[0]
                    y = pos[1]
                    x = math.floor(x/sq_sz)
                    y = math.floor(y/sq_sz)

                    if(clickedPiece is not None): # if a piece was previously clicked
                        #get the piece if any, at the square you want to move to
                        pieceAtClickedSq = self.white.get_piece_at(x,y)
                        if(pieceAtClickedSq==None):
                            pieceAtClickedSq = self.black.get_piece_at(x,y)
                            
                        if(clickedPiece.isLegalMove(x,y,pieceAtClickedSq) and clickedPiece.owner==currentPlayer and self.clearPath(clickedPiece,x,y)): #if the move is legal for the piece, and its your turn, and the path is clear make the move
                            if(pieceAtClickedSq is not None and pieceAtClickedSq.owner=='BLACK'): # if a black piece will be taken
                                self.black.remove_piece_at(x,y) # remove the black piece from the board
                                self.blackLoses.append(pieceAtClickedSq.pieceType) # add the piece to the list of black pieces taken
                            if(pieceAtClickedSq is not None and pieceAtClickedSq.owner=='WHITE'):# if a white piece will be taken
                                self.white.remove_piece_at(x,y)
                                self.whiteLoses.append(pieceAtClickedSq.pieceType)
                            #update the coordinates of the piece to be moved
                            clickedPiece.xCoord = x
                            clickedPiece.yCoord = y

                            if(clickedPiece.pieceType=='Pawn'): # if a pawn has been moved
                                if(y==0 and clickedPiece.owner=='WHITE'): #if a white pawn makes it to the other side of the board
                                    print (self.whiteLoses) # print the pieces the white player has lost
                                    ans = input("What piece from the above do you want back? ") # Ask the player what piece they want back
                                    self.white.remove_piece_at(x,y) # remove the pawn from position x,y
                                    self.whiteLoses.append(clickedPiece.pieceType) # add a pawn to the list of pieces white has lost
                                    self.white.add_piece(ans,x,y) #adds a piece of the desired type to the board
                                    self.whiteLoses.remove(ans)
                                elif(y==7 and clickedPiece.owner=='BLACK'): # if a black pawn makes it to the other side of the board
                                    print (self.blackLoses)
                                    ans = input("What piece from the above do you want back?")
                                    self.black.remove_piece_at(x,y)
                                    self.blackLoses.append(clickedPiece.pieceType)
                                    self.black.add_piece(ans,x,y)
                                    self.blackLoses.remove(ans)
                            clickedPiece = None # reset the clicked piece to nothing
                            if(currentPlayer=='WHITE'): # switch turns
                                currentPlayer='BLACK'
                            else:
                                currentPlayer='WHITE'
                        else:
                            clickedPiece=None
                            
                    elif(self.white.get_piece_at(x,y) is not None): #if no piece was selected last click, check is clicked square has a piece
                        clickedPiece = self.white.get_piece_at(x,y)
                    elif(self.black.get_piece_at(x,y) is not None):
                        clickedPiece = self.black.get_piece_at(x,y)
                    else: # default to the player clicked no piece
                        clickedPiece=None
            pygame.display.flip()
            #return self,otherBoard,clickedPiece

def runGame(board1, board2, clickedPiece):
    #while(1):
    board1.play_board(board2,clickedPiece)

if __name__ == "__main__":
    chessboard1 = Board(800,0) # board 1 is the one you play on
    chessboard2 = Board(800,1000) # board 2 is the board your teammate plays on
    #chessboard1.play_board(chessboard2) # play board1 and draw board2
    clickedPiece = None
    #t = LoopingCall(runGame,(chessboard1,chessboard2,clickedPiece))
    #t.start(1/60)
    runGame(chessboard1,chessboard2, clickedPiece)
    #reactor.run()
