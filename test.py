from piece import *

pawn = Pawn()
pawn.setCoords(4,1)
pawn.setOwner('BLACK')

horse = Horse()
horse.setCoords(5,2)
horse.setOwner('WHITE')

rook = Rook()
rook.setCoords(4,4)
rook.setOwner('WHITE')

bishop = Bishop()
bishop.setCoords(5,5)
bishop.setOwner('BLACK')

queen = Queen()
queen.setCoords(0,4)
queen.setOwner('BLACK')

print queen.isLegalMove(4,4,None)
print queen.isLegalMove(0,7,None)
print queen.isLegalMove(1,5,None)

