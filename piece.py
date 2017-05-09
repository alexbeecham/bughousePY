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

    def manhatDist(self,x,y): # gives the manhattan distance from the piece to the given coordinates
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
            if(self.hasMoved==0 and x==self.xCoord and (y==(self.yCoord+1) or y==(self.yCoord+2))):#on its first move, a pawn can move 1 or 2 spaces forward
                self.hasMoved=1
                self.lastMoveSize=2
                return True
            elif(x==self.xCoord and y==(self.yCoord+1) and piece==None): #pawn can move one space forward
                self.lastMoveSize=1
                self.hasMoved=1
                return True
            elif(y==(self.yCoord+1) and (x==(self.xCoord-1) or x==(self.xCoord+1)) and piece!=None and piece.owner=='WHITE'):#pawn can take pieces forward and diagonal from it
                self.hasMoved=1
                self.lastMoveSize=1
                return True
            elif(y==(self.yCoord+1) and (x==(self.xCoord-1) or x==(self.xCoord+1)) and piece.pieceType=='Pawn' and piece.lastMoveSize==2 and piece.owner=='WHITE'): # en passant rule
                self.lastMoveSize=1
                self.hasMoved=1
                return True
            else:
                return False
        else: #piece is a white pawn same logic as above but y direction is reversed
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
        if(x>7 or y>7 or x<0 or y<0): #makes sure click is in bounds
            return False
        elif(piece==None or piece.owner!=self.owner): # if the space is empty or occupied by an opposing piece
            if((x==self.xCoord and y!=self.yCoord) or (x!=self.xCoord and y==self.yCoord)): #if the move only changes one coordinate
                return True
        return False

class Horse(Piece):
    pieceType='Horse'


    def isLegalMove(self,x,y,piece): # makes sure click is in bounds
        if(x>7 or y>7 or x<0 or y<0):
            return False
        elif(piece==None or piece.owner!=self.owner): # if space is occupied by enemy or nothing
            if(self.manhatDist(x,y)==3 and x!=self.xCoord and y!=self.yCoord): # knights must move such that the manhattan distance of the move is 3
                return True
        return False

class Bishop(Piece):
    pieceType='Bishop'


    def isLegalMove(self,x,y,piece): 
        if(x>7 or y>7 or x<0 or y<0):
            return False
        elif(piece==None or piece.owner!=self.owner):
            if(self.manhatDist(x,y)%2==0 and self.manhatDist(x,y)>0 and x!=self.xCoord and y!=self.yCoord and (abs(self.xCoord-x)==abs(self.yCoord-y))): #the manhattan distance must be a multiple of 2, both coordinates must change and in the same amount
                return True
        return False

class Queen(Piece):
    pieceType='Queen'


    def isLegalMove(self,x,y,piece):
        if(x>7 or y>7 or x<0 or y<0):
            return False
        elif(piece==None or piece.owner!=self.owner):
            if((x==self.xCoord and y!=self.yCoord) or (x!=self.xCoord and y==self.yCoord)): # if the move is purely horizontal or vertical like a rook
                return True
            elif(self.manhatDist(x,y)%2==0 and self.manhatDist(x,y)>0 and x!=self.xCoord and y!=self.yCoord and (abs(self.xCoord-x)==abs(self.yCoord-y))): # if move is diagonal like a bishop
                return True
        return False

class King(Piece):
    pieceType='King'


    def isLegalMove(self,x,y,piece):
        if(x>7 or y>7 or x<0 or y<0):
            return False
        elif(piece==None or piece.owner!=self.owner):
            if(((x==self.xCoord and y!=self.yCoord) or (x!=self.xCoord and y==self.yCoord)) and self.manhatDist(x,y)==1): # if move is horizontal or vertical and only 1 square away
                return True
            elif(self.manhatDist(x,y)%2==0 and self.manhatDist(x,y)==2 and x!=self.xCoord and y!=self.yCoord):# if move is diagonal and 2 squares away
                return True
        return False
        
