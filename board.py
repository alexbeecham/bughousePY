import pygame

'''class Tile(pygame.sprite.Sprite):
    def __init__(self, image, location):
         pygame.sprite.Sprite.__init__(self)

         self.image = image.convert()
         self.rect = pygame.Rect(location, self.image.get_size())'''

class Board():
    def __init__(self):
        self.squares = [['br', 'bh', 'bb', 'bq', 'bk', 'bb', 'bh', 'br'], \
                        ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'], \
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], \
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], \
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], \
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], \
                        ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'], \
                        ['wr', 'wh', 'wb', 'wq', 'wk', 'wb', 'wh', 'wr']]

    def draw_board(self):
        pygame.init()
        colors = [(255, 255, 255), (0, 0, 0)]

        n = 8
        surface_sz = 480
        sq_sz = surface_sz // n
        surface_sz = n * sq_sz

        surface = pygame.display.set_mode((surface_sz, surface_sz))

        while True:
            pygame.event.get()
            for row in range(n):
                c_indx = row % 2
                for col in range(n):
                    the_square = (col*sq_sz,  row*sq_sz, sq_sz, sq_sz)
                    surface.fill(colors[c_indx], the_square)
                    c_indx = (c_indx + 1) % 2

if __name__ == "__main__":
    chessboard = Board()
    chessboard.draw_board()
