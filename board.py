import pygame
import sys
from images import *
from player import *
from piece import *
from pygame.locals import*

'''class Tile(pygame.sprite.Sprite):
    def __init__(self, image, location):
         pygame.sprite.Sprite.__init__(self)

         self.image = image.convert()
         self.rect = pygame.Rect(location, self.image.get_size())'''

class Board():
    def __init__(self, n, offset):
        self.squares = [['br', 'bh', 'bb', 'bq', 'bk', 'bb', 'bh', 'br'], \
                        ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'], \
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], \
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], \
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], \
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], \
                        ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'], \
                        ['wr', 'wh', 'wb', 'wq', 'wk', 'wb', 'wh', 'wr']]

        self.length = n
        self.white = Player("WHITE")
        self.black = Player("BLACK")
        self.offset = offset
        self.blackLoses=[]
        self.whiteLoses=[]

    def draw_pieces(self, surface,black,white):
        #print(len(self.white.pieces))

        for piece in black.pieces:
            x = self.length/8 * piece.xCoord+self.offset
            y = self.length/8 * piece.yCoord
            img = pieceimages[piece.image]
            surface.blit(img, (x+13,y+13))

        for piece in white.pieces:
            x = self.length/8 * piece.xCoord+self.offset
            y = self.length/8 * piece.yCoord
            img = pieceimages[piece.image]
            surface.blit(img, (x+13,y+13))

    def flipBoard(self):
        p1 = self.white
        p2 = self.black
        for piece in p1.pieces:
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
        for piece in p2.pieces:
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
    def drawBoard(self, surface):
        colors=[(255,0,0),(0,0,255)]
        n = 8
        sq_sz = self.length/n
        for row in range(n):
            c_indx = row % 2
            for col in range(n):
                    the_square = (col*sq_sz+self.offset, row*sq_sz, sq_sz, sq_sz)
                    surface.fill(colors[c_indx], the_square)
                    c_indx = (c_indx + 1) % 2
        p1,p2 = self.flipBoard()

        self.draw_pieces(surface,p2,p1)
        return surface

    def play_board(self, otherBoard):
        pygame.init()
        colors = [(255, 0, 0), (0, 0, 255)]

        n = 8
        sq_sz = self.length / n
        clickedPiece = None
        surface = pygame.display.set_mode((2*self.length+100, self.length))
        currentPlayer = "WHITE"
        surface = otherBoard.drawBoard(surface)

        while True:
            pygame.event.get()
            for row in range(n):
                c_indx = row % 2
                for col in range(n):
                    the_square = (col*sq_sz,  row*sq_sz, sq_sz, sq_sz)
                    surface.fill(colors[c_indx], the_square)
                    c_indx = (c_indx + 1) % 2

            self.draw_pieces(surface,self.black,self.white)
            ev = pygame.event.get()
            for event in ev:
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    x = pos[0]
                    y = pos[1]
                    x = math.floor(x/sq_sz)
                    y = math.floor(y/sq_sz)
                    if(clickedPiece is not None):
                        pieceAtClickedSq = self.white.get_piece_at(x,y)
                        if(pieceAtClickedSq==None):
                            pieceAtClickedSq = self.black.get_piece_at(x,y)
                        if(clickedPiece.isLegalMove(x,y,pieceAtClickedSq) and clickedPiece.owner==currentPlayer):
                            if(pieceAtClickedSq is not None and pieceAtClickedSq.owner=='BLACK'):
                                self.black.remove_piece_at(x,y)
                                self.blackLoses.append(pieceAtClickedSq.pieceType)
                                print(self.blackLoses)
                            if(pieceAtClickedSq is not None and pieceAtClickedSq.owner=='WHITE'):
                                self.white.remove_piece_at(x,y)
                                self.whiteLoses.append(pieceAtClickedSq.pieceType)
                                print(self.whiteLoses)
                            clickedPiece.xCoord = x
                            clickedPiece.yCoord = y
                            if(clickedPiece.pieceType=='Pawn'):
                                print("a pawn has been clicked")
                                if(y==0 and clickedPiece.owner=='WHITE'):
                                    print (self.whiteLoses)
                                    ans = input("What piece from the above do you want back? ")
                                    print (ans)
                                    self.white.remove_piece_at(x,y)
                                    self.whiteLoses.append(clickedPiece.pieceType)
                                    self.white.add_piece(ans,x,y)
                            clickedPiece = None
                            if(currentPlayer=='WHITE'):
                                currentPlayer='BLACK'
                            else:
                                currentPlayer='WHITE'
                        else:
                            clickedPiece=None
                            
                    elif(self.white.get_piece_at(x,y) is not None):
                        clickedPiece = self.white.get_piece_at(x,y)
                    elif(self.black.get_piece_at(x,y) is not None):
                        clickedPiece = self.black.get_piece_at(x,y)
                    else:
                        clickedPiece=None
            pygame.display.flip()
if __name__ == "__main__":
    chessboard1 = Board(800,0)
    chessboard2 = Board(800,900)
    chessboard1.play_board(chessboard2)
