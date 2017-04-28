import math

class Piece:
    def __init__(self):
        self.image=None
        self.xCoord=None
        self.yCoord=None
        self.owner=None
    

    def setImage(self,img):
        self.image=img

    def setOwner(self,player):
        self.owner=player
    
    def setCoords(self,x,y):
        self.xCoord=x
        self.yCoord=y

    def manhatDist(self,x,y):
        xdiff = abs(self.xCoord-x)
        ydiff = abs(self.yCoord-y)
        return xdiff+ydiff

class Pawn(Piece):

    pieceType='Pawn'

    def __init__(self):
        self.hasMoved=0
        self.lastMoveSize=0

    def isLegalMove(self,x,y,piece):
        if(x<0 or y<0 or x>7 or y>7): #if move is out of bounds return false
            return False
        elif(self.owner=='BLACK'): # set rules for movement of black pawn
            if(self.hasMoved==0 and x==self.xCoord and (y==(self.yCoord+1) or y==(self.yCoord+2))):
                self.hasMoved=1
                self.lastMoveSize=2
                return True
            elif(x==self.xCoord and y==(self.yCoord+1) and piece==None):
                self.lastMoveSize=1
                return True
            elif(y==(self.yCoord+1) and (x==(self.xCoord-1) or x==(self.xCoord+1)) and piece!=None and piece.owner=='WHITE'):
                self.lastMoveSize=1
                return True
            elif(y==(self.yCoord+1) and (x==(self.xCoord-1) or x==(self.xCoord+1)) and piece.pieceType=='Pawn' and piece.lastMoveSize==2 and piece.owner=='WHITE'):
                self.lastMoveSize=1
                return True
            else:
                return False
        else: #piece is a white pawn
            if(self.hasMoved==0 and x==self.xCoord and (y==(self.yCoord-1) or y==(self.yCoord-2))):
                self.hasMoved=1
                self.lastMoveSize=2
                return True
            elif(x==self.xCoord and y==(self.yCoord-1) and piece==None):
                self.lastMoveSize=1
                return True
            elif(y==(self.yCoord-1) and (x==(self.xCoord-1) or x==(self.xCoord+1)) and piece!=None and piece.owner=='BLACK'):
                self.lastMoveSize=1
                return True
            elif(y==(self.yCoord-1) and (x==(self.xCoord-1) or x==(self.xCoord+1)) and piece.pieceType=='Pawn' and piece.lastMoveSize==2 and piece.owner=='BLACK'):
                self.lastMoveSize=1
                return True
            else:
                return False

class Rook(Piece):
    pieceType='Rook'
    

    def isLegalMove(self,x,y,piece):
        if(x>7 or y>7 or x<0 or y<0):
            return False
        elif(piece==None or piece.owner!=self.owner):
            if((x==self.xCoord and y!=self.yCoord) or (x!=self.xCoord and y==self.yCoord)):
                return True
        return False

class Horse(Piece):
    pieceType='Horse'


    def isLegalMove(self,x,y,piece):
        if(x>7 or y>7 or x<0 or y<0):
            return False
        elif(piece==None or piece.owner!=self.owner):
            if(self.manhatDist(x,y)==3 and x!=self.xCoord and y!=self.yCoord):
                return True
        return False

class Bishop(Piece):
    pieceType='Bishop'


    def isLegalMove(self,x,y,piece):
        if(x>7 or y>7 or x<0 or y<0):
            return False
        elif(piece==None or piece.owner!=self.owner):
            if(self.manhatDist(x,y)%2==0 and self.manhatDist(x,y)>0 and x!=self.xCoord and y!=self.yCoord):
                return True
        return False

class Queen(Piece):
    pieceType='Queen'


    def isLegalMove(self,x,y,piece):
        if(x>7 or y>7 or x<0 or y<0):
            return False
        elif(piece==None or piece.owner!=self.owner):
            if((x==self.xCoord and y!=self.yCoord) or (x!=self.xCoord and y==self.yCoord)):
                return True
            elif(self.manhatDist(x,y)%2==0 and self.manhatDist(x,y)>0 and x!=self.xCoord and y!=self.yCoord):
                return True
        return False

class King(Piece):
    pieceType='King'


    def isLegalMove(self,x,y,piece):
        if(x>7 or y>7 or x<0 or y<0):
            return False
        elif(piece==None or piece.owner!=self.owner):
            if(((x==self.xCoord and y!=self.yCoord) or (x!=self.xCoord and y==self.yCoord)) and Piece.manhatDist(x,y)==1):
                return True
            elif(self.manhatDist(x,y)%2==0 and self.manhatDist(x,y)==1 and x!=self.xCoord and y!=self.yCoord):
                return True
        return False
        
