import pygame
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
    def __init__(self, n):
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

    def draw_pieces(self, surface):
        #print(len(self.white.pieces))

        for piece in self.black.pieces:
            x = self.length/8 * piece.xCoord
            y = self.length/8 * piece.yCoord
            img = pieceimages[piece.image]
            surface.blit(img, (x+13,y+13))

        for piece in self.white.pieces:
            x = self.length/8 * piece.xCoord
            y = self.length/8 * piece.yCoord
            img = pieceimages[piece.image]
            surface.blit(img, (x+13,y+13))

        pygame.display.flip()

        '''for piece in self.black.pieces:
            x = self.length * piece.xCoord
            y = self.length * piece.yCoord
            img = pieceimages[piece.image]
            surface.blit(img, (x,y))'''

    def draw_board(self):
        pygame.init()
        colors = [(255, 0, 0), (0, 0, 255)]

        n = 8
        sq_sz = self.length / n

        surface = pygame.display.set_mode((self.length, self.length))

        while True:
            pygame.event.get()
            for row in range(n):
                c_indx = row % 2
                for col in range(n):
                    the_square = (col*sq_sz,  row*sq_sz, sq_sz, sq_sz)
                    surface.fill(colors[c_indx], the_square)
                    c_indx = (c_indx + 1) % 2

            self.draw_pieces(surface)

if __name__ == "__main__":
    chessboard = Board(800)
    chessboard.draw_board()
