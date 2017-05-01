import pygame
from piece import *

class Player():
    def __init__(self, name):
        self.color = name
        offset_pawn = 1
        offset_royals = 0
        if name == "WHITE":
            offset_pawn = 6
            offset_royals = 7

        self.pieces = []
        for x in range(0, 8):
            pawn = Pawn()
            pawn.owner = self.color
            if name == "WHITE":
                pawn.image = "WPawn"
            else:
                pawn.image = "BPawn"

            pawn.xCoord = x
            pawn.yCoord = offset_pawn
            self.pieces.append(pawn)

        for x in range(0, 8):
            piece = None
            image_key = "W"
            if name == "BLACK":
                image_key = "B"

            if x == 0 or x == 7:
                image_key += "Rook"
                piece = Rook()
            elif x == 1 or x == 6:
                image_key += "Knight"
                piece = Horse()
            elif x == 2 or x == 5:
                image_key += "Bishop"
                piece = Bishop()
            elif x == 3:
                if image_key == "B":
                    image_key += "Queen"
                    piece = Queen()
                else:
                    image_key += "King"
                    piece = King()
            else:
                if image_key == "W":
                    image_key += "Queen"
                    piece = Queen()
                else:
                    image_key += "King"
                    piece = King()

            piece.owner = self.color
            piece.image = image_key
            piece.xCoord = x
            piece.yCoord = offset_royals
            self.pieces.append(piece)

    def get_piece_at(self, x, y):
        for piece in self.pieces:
            if piece.xCoord == x and piece.yCoord == y:
                return piece

        return None

    def remove_piece_at(self, x, y):
        for piece in self.pieces:
            if piece.xCoord == x and piece.yCoord == y:
                del self.pieces[piece]

    def add_piece(self, piece):
        if piece.owner == self.color:
            self.pieces.append(piece)
