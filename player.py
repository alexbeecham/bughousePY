import pygame
from piece import *

class Player():
    def __init__(self, name):
        self.color = name
        # assume the player is black
        offset_pawn = 1 # black pawns start in the 2nd row
        offset_royals = 0 #black royals start in the top row
        if name == "WHITE":
            offset_pawn = 6 # white pawns start in the 6th row
            offset_royals = 7 # white royals start in the bottom row

        self.pieces = []
        for x in range(0, 8): # add all the pawns for the player
            pawn = Pawn()
            pawn.owner = self.color
            if name == "WHITE":
                pawn.image = "WPawn"
            else:
                pawn.image = "BPawn"

            pawn.xCoord = x
            pawn.yCoord = offset_pawn
            self.pieces.append(pawn)

        for x in range(0, 8): #add the royals
            piece = None
            image_key = "W" #builds the key value for the image dictionary for the piece being added
            if name == "BLACK":
                image_key = "B"

            if x == 0 or x == 7: #if piece is a rook 
                image_key += "Rook"
                piece = Rook()
            elif x == 1 or x == 6: #knight/horse
                image_key += "Knight"
                piece = Horse()
            elif x == 2 or x == 5:#bishop
                image_key += "Bishop"
                piece = Bishop()
            elif x == 3:#queen if black, king if white
                if image_key == "B":
                    image_key += "Queen"
                    piece = Queen()
                else:
                    image_key += "King"
                    piece = King()
            else: #queen if white, king if black
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

    def get_piece_at(self, x, y): #returns the piece at the given location. Defaults to None
        for piece in self.pieces:
            if piece.xCoord == x and piece.yCoord == y:
                return piece

        return None

    def remove_piece_at(self, x, y): #attempts to remove the piece at x,y
        for piece in range(0,len(self.pieces)-1):
            if self.pieces[piece].xCoord == x and self.pieces[piece].yCoord == y:
                del self.pieces[piece]

    def add_piece(self, ans,x,y): #adds the desired piece at the location
        imageKey = "W" #build the image key
        piece = None
        if(self.color=='BLACK'):
            imageKey="B"
        if(ans=='None'):
            return
        elif(ans=='Rook'):
            imageKey+="Rook"
            piece = Rook()
        elif(ans=='Horse'):
            imageKey+='Horse'
            piece = Horse()
        elif(ans=='Bishop'):
            imageKey+='Bishop'
            piece=Bishop()
        elif(ans=='Queen'):
            imageKey+='Queen'
            piece=Queen()
        elif(ans=='King'):
            imageKey+='King'
            piece=King()
        piece.image = imageKey
        piece.owner = self.color
        piece.xCoord = x
        piece.yCoord = y
        self.pieces.append(piece)
