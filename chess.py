########################################################
# NAME: GROUP 4
# ASGT: Class Project
# ORGN: CSUB - CMPS 3500
# FILE: chess.py
# DATE: 12/03/2023
# This is a program that will simulate a chess board
# and provide basic game functionalities.
# This program does not abide all rules of chess
########################################################
import os
import pygame
import random
import sys
from itertools import combinations

# current directory
dirname = os.path.dirname(__file__)

# set board width and set number of rows
WIDTH = 800
ROWS = 8

# load images for pieces
B_BISHOP = pygame.image.load(os.path.join(dirname, 'images2/b_bishop.png'))
B_KING = pygame.image.load(os.path.join(dirname, 'images2/b_king.png'))
B_KNIGHT = pygame.image.load(os.path.join(dirname, 'images2/b_knight.png'))
B_PAWN = pygame.image.load(os.path.join(dirname, 'images2/b_pawn.png'))
B_QUEEN = pygame.image.load(os.path.join(dirname, 'images2/b_queen.png'))
B_ROOK = pygame.image.load(os.path.join(dirname, 'images2/b_rook.png'))
W_BISHOP = pygame.image.load(os.path.join(dirname, 'images2/w_bishop.png'))
W_KING = pygame.image.load(os.path.join(dirname, 'images2/w_king.png'))
W_KNIGHT = pygame.image.load(os.path.join(dirname, 'images2/w_knight.png'))
W_PAWN = pygame.image.load(os.path.join(dirname, 'images2/w_pawn.png'))
W_QUEEN = pygame.image.load(os.path.join(dirname, 'images2/w_queen.png'))
W_ROOK = pygame.image.load(os.path.join(dirname, 'images2/w_rook.png'))

DARK = (118, 150, 86) # dark green
LIGHT = (238, 238, 210) #light green

BLUE = (76, 252, 241)
BLACK = (0,0,0)
ORANGE = (186,202,68) #actually yellow
YELLOW = (235, 168, 52) #actually orange
WHITE = (255,255,255)
RED = (255, 0, 0)


pygame.init()
SCREEN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption('Chess')

# keeps track of squares on the board
class Node:

    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = int(row * width)
        self.y = int(col * width)
        self.colour = DARK
        self.piece = None

    def draw(self, SCREEN):
        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y, WIDTH / ROWS, WIDTH / ROWS))
        if self.piece:
            SCREEN.blit(self.piece.image, (self.x, self.y))

# updates display, including board anf pieces
def update_display(win, grid, rows, width):
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()

# initial board creator with pieces, sets them to corret spots
def make_grid(rows, width):
    grid = []
    gap = width//rows
    count = 0
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(j,i, gap)
            if abs(i-j) % 2 == 0:
                node.colour=LIGHT
            if count == 0 or count == 7:
                node.piece = Piece('ROOK', 'B')
            elif count == 1 or count == 6:
                node.piece = Piece('KNIGHT', 'B')
            elif count == 2 or count == 5:
                node.piece = Piece('BISHOP', 'B')
            elif count == 3:
                node.piece = Piece('QUEEN', 'B')
            elif count == 4:
                node.piece = Piece('KING', 'B')
            elif count > 7 and count < 16:
                node.piece = Piece('PAWN', 'B')
            elif count == 56 or count == 63:
                node.piece = Piece('ROOK', 'W')
            elif count == 57 or count == 62:
                node.piece = Piece('KNIGHT', 'W')
            elif count == 58 or count == 61:
                node.piece = Piece('BISHOP', 'W')
            elif count == 59:
                node.piece = Piece('QUEEN', 'W')
            elif count == 60:
                node.piece = Piece('KING', 'W')
            elif count > 47 and count < 56:
                node.piece = Piece('PAWN', 'W')
            count += 1
            grid[i].append(node)
    return grid

# used to draw the board, along with pieces
def draw_grid(win, rows, width):
    gap = width // ROWS
    for i in range(rows):
        pygame.draw.line(win, DARK, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, DARK, (j * gap, 0), (j * gap, width))

# holds the difference pieces on the board
class Piece:
    def __init__(self, name, team):
        self.name = name
        self.team = team
        if self.team == 'B':
            if self.name == 'BISHOP':
                self.image = B_BISHOP
            elif self.name == 'KING':
                self.image = B_KING
            elif self.name == 'KNIGHT':
                self.image = B_KNIGHT
            elif self.name == 'QUEEN':
                self.image = B_QUEEN
            elif self.name == 'ROOK':
                self.image = B_ROOK
            else:
                self.image = B_PAWN
        else:
            if self.name == 'BISHOP':
                self.image = W_BISHOP
            elif self.name == 'KING':
                self.image = W_KING
            elif self.name == 'KNIGHT':
                self.image = W_KNIGHT
            elif self.name == 'QUEEN':
                self.image = W_QUEEN
            elif self.name == 'ROOK':
                self.image = W_ROOK
            else:
                self.image = W_PAWN

        self.type=None
        self.hasMoved = False # for pawns, rooks, and kings

    def draw(self, x, y):
        SCREEN.blit(self.image, (x,y))

# used to determine what column/row was clicked
def getNode(grid, rows, width):
    gap = width//rows
    RowX,RowY = pygame.mouse.get_pos()
    Row = RowX//gap
    Col = RowY//gap
    return (Col,Row)

# resets colors back to original, used if changes occur
def resetColours(grid, node):
    positions = generatePotentialMoves(node, grid)
    positions.append(node)

    for colouredNodes in positions:
        nodeX, nodeY = colouredNodes
        grid[nodeX][nodeY].colour = LIGHT if abs(nodeX - nodeY) % 2 == 0 else DARK

# changes color of spaces a piece can move to
def HighlightpotentialMoves(piecePosition, grid):
    positions = generatePotentialMoves(piecePosition, grid)
    for position in positions:
        Column,Row = position
        if grid[Column][Row].piece:
            grid[Column][Row].colour = RED
        else:
            grid[Column][Row].colour=BLUE

# function to check the color of the piece
def opposite(team):
    return "W" if team=="B" else "B"

# calculate moves a piece can take
def generatePotentialMoves(nodePosition, grid):
    piece = lambda x,y: x+y>=0 and x+y<8
    positions= []
    vectors = []
    column, row = nodePosition
    if grid[column][row].piece:
        
        # pawn moveset
        if grid[column][row].piece.name =='PAWN':
            if grid[column][row].piece.team =='W':
                vectors = [[-1, 0]]
                if grid[column][row].piece.hasMoved == False and not grid[column - 1][row].piece:
                    vectors = [[-1, 0], [-2, 0]]
                if row >= 0 and column >= 0 and grid[column - 1][row - 1].piece and grid[column - 1][row - 1].piece.team == opposite(grid[column][row].piece.team):
                    vectors.append([-1, -1])
                if row < 7 and column >= 0 and grid[column - 1][row + 1].piece and grid[column - 1][row + 1].piece.team == opposite(grid[column][row].piece.team):
                    vectors.append([-1, 1])
            else:
                vectors = [[1, 0]]
                if grid[column][row].piece.hasMoved == False and not grid[column + 1][row].piece:
                    vectors = [[1, 0], [2, 0]]  
                if row < 7 and grid[column + 1][row + 1].piece and grid[column + 1][row + 1].piece.team == opposite(grid[column][row].piece.team):
                    vectors.append([1, 1])
                if row >= 0 and grid[column + 1][row - 1].piece and grid[column + 1][row - 1].piece.team == opposite(grid[column][row].piece.team):
                    vectors.append([1, -1])
                
         

        # knight moveset
        if grid[column][row].piece.name =='KNIGHT':
            vectors = [[-2, 1], [-2, -1], [-1, 2], [-1, -2], [1, -2], [1, 2], [2, -1], [2, 1]] 

        # king moveset
        if grid[column][row].piece.name =='KING':
            vectors = [[1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1], [0, 1]] 

        # rook moveset
        if grid[column][row].piece.name =='ROOK':
            up = down = left = right = 1
            while column - up >= 0 and not grid[column - up][row].piece:
                vectors.append([-up, 0])
                up += 1
            if column - up >= 0 and grid[column - up][row].piece and grid[column - up][row].piece.team == opposite(grid[column][row].piece.team):
                vectors.append([-up, 0])
            while 0 <= column + down < 8 and not grid[column + down][row].piece:
                vectors.append([down, 0])
                down += 1
            if column + down < 8 and grid[column + down][row].piece and grid[column + down][row].piece.team == opposite(grid[column][row].piece.team):
                vectors.append([down, 0])
            while 0 <= row - left < 8 and not grid[column][row - left].piece:
                vectors.append([0, -left])
                left += 1
            if row - left >= 0 and grid[column][row - left].piece and grid[column][row - left].piece.team == opposite(grid[column][row].piece.team):
                vectors.append([0, -left])
            while 0 <= row + right < 8 and not grid[column][row + right].piece:
                vectors.append([0, right])
                right += 1
            if row + right < 8 and grid[column][row + right].piece and grid[column][row + right].piece.team == opposite(grid[column][row].piece.team):
                vectors.append([0, right])

        # bishop moveset
        if grid[column][row].piece.name =='BISHOP':
            upLeft = upRight = downLeft = downRight = 1
            while 0 <= column - upLeft < 8 and 0 <= row - upLeft < 8 and not grid[column - upLeft][row - upLeft].piece:
                vectors.append([-upLeft, -upLeft])
                upLeft += 1
            if column - upLeft >= 0 and row - upLeft >= 0 and grid[column - upLeft][row - upLeft].piece and grid[column - upLeft][row - upLeft].piece.team == opposite(grid[column][row].piece.team):
                vectors.append([-upLeft, -upLeft])
            while 0 <= column - upRight < 8 and 0 <= row + upRight < 8 and not grid[column - upRight][row + upRight].piece:
                vectors.append([-upRight, upRight])
                upRight += 1
            if column - upRight >= 0 and row + upRight < 8 and grid[column - upRight][row + upRight].piece and grid[column - upRight][row + upRight].piece.team == opposite(grid[column][row].piece.team):
                vectors.append([-upRight, upRight])
            while 0 <= column + downLeft < 8 and 0 <= row - downLeft < 8 and not grid[column + downLeft][row - downLeft].piece:
                vectors.append([downLeft, -downLeft])
                downLeft += 1
            if column + downLeft < 8 and row - downLeft >= 0 and grid[column + downLeft][row - downLeft].piece and grid[column + downLeft][row - downLeft].piece.team == opposite(grid[column][row].piece.team):
                vectors.append([downLeft, -downLeft])
            while 0 <= column + downRight < 8 and 0 <= row + downRight < 8 and not grid[column + downRight][row + downRight].piece:
                vectors.append([downRight, downRight])
                downRight += 1
            if column + downRight < 8 and row + downRight < 8 and grid[column + downRight][row + downRight].piece and grid[column + downRight][row + downRight].piece.team == opposite(grid[column][row].piece.team):
                vectors.append([downRight, downRight])

        # queen moveset is rook moveset + bishop moveset
        if grid[column][row].piece.name =='QUEEN':
            up = down = left = right = 1
            upLeft = upRight = downLeft = downRight = 1
            while column - up >= 0 and not grid[column - up][row].piece:
                vectors.append([-up, 0])
                up += 1
            if column - up >= 0 and grid[column - up][row].piece and grid[column - up][row].piece.team == opposite(grid[column][row].piece.team):
                vectors.append([-up, 0])
            while 0 <= column + down < 8 and not grid[column + down][row].piece:
                vectors.append([down, 0])
                down += 1
            if column + down < 8 and grid[column + down][row].piece and grid[column + down][row].piece.team == opposite(grid[column][row].piece.team):
                vectors.append([down, 0])
            while 0 <= row - left < 8 and not grid[column][row - left].piece:
                vectors.append([0, -left])
                left += 1
            if row - left >= 0 and grid[column][row - left].piece and grid[column][row - left].piece.team == opposite(grid[column][row].piece.team):
                vectors.append([0, -left])
            while 0 <= row + right < 8 and not grid[column][row + right].piece:
                vectors.append([0, right])
                right += 1
            if row + right < 8 and grid[column][row + right].piece and grid[column][row + right].piece.team == opposite(grid[column][row].piece.team):
                vectors.append([0, right])
            while 0 <= column - upLeft < 8 and 0 <= row - upLeft < 8 and not grid[column - upLeft][row - upLeft].piece:
                vectors.append([-upLeft, -upLeft])
                upLeft += 1
            if column - upLeft >= 0 and row - upLeft >= 0 and grid[column - upLeft][row - upLeft].piece and grid[column - upLeft][row - upLeft].piece.team == opposite(grid[column][row].piece.team):
                vectors.append([-upLeft, -upLeft])
            while 0 <= column - upRight < 8 and 0 <= row + upRight < 8 and not grid[column - upRight][row + upRight].piece:
                vectors.append([-upRight, upRight])
                upRight += 1
            if column - upRight >= 0 and row + upRight < 8 and grid[column - upRight][row + upRight].piece and grid[column - upRight][row + upRight].piece.team == opposite(grid[column][row].piece.team):
                vectors.append([-upRight, upRight])
            while 0 <= column + downLeft < 8 and 0 <= row - downLeft < 8 and not grid[column + downLeft][row - downLeft].piece:
                vectors.append([downLeft, -downLeft])
                downLeft += 1
            if column + downLeft < 8 and row - downLeft >= 0 and grid[column + downLeft][row - downLeft].piece and grid[column + downLeft][row - downLeft].piece.team == opposite(grid[column][row].piece.team):
                vectors.append([downLeft, -downLeft])
            while 0 <= column + downRight < 8 and 0 <= row + downRight < 8 and not grid[column + downRight][row + downRight].piece:
                vectors.append([downRight, downRight])
                downRight += 1
            if column + downRight < 8 and row + downRight < 8 and grid[column + downRight][row + downRight].piece and grid[column + downRight][row + downRight].piece.team == opposite(grid[column][row].piece.team):
                vectors.append([downRight, downRight])



        # determines what will happen if piece moves into new grid slot?
        for vector in vectors:
            columnVector, rowVector = vector
            if piece(columnVector,column) and piece(rowVector,row):
                if not grid[(column+columnVector)][(row+rowVector)].piece:
                    positions.append((column + columnVector, row + rowVector))
                elif grid[column+columnVector][row+rowVector].piece and\
                        grid[column+columnVector][row+rowVector].piece.team==opposite(grid[column][row].piece.team) and\
                        grid[column][row].piece.name != 'PAWN':
                    positions.append([column+columnVector, row+rowVector])
                elif grid[column+columnVector][row+rowVector].piece and\
                        grid[column+columnVector][row+rowVector].piece.team==opposite(grid[column][row].piece.team) and\
                        grid[column][row].piece.name == 'PAWN' and\
                        rowVector != 0:
                    positions.append([column+columnVector, row+rowVector])

    return positions

# highlights clicked piece on board
def highlight(ClickedNode, Grid, OldHighlight):
    Column,Row = ClickedNode
    Grid[Column][Row].colour=ORANGE
    if OldHighlight:
        resetColours(Grid, OldHighlight)
    HighlightpotentialMoves(ClickedNode, Grid)
    return (Column,Row)

# moves piece into new position
def move(grid, piecePosition, newPosition):
    resetColours(grid, piecePosition)
    newColumn, newRow = newPosition
    oldColumn, oldRow = piecePosition

    piece = grid[oldColumn][oldRow].piece
    grid[newColumn][newRow].piece = piece
    grid[oldColumn][oldRow].piece = None

    grid[newColumn][newRow].piece.hasMoved = True

    return opposite(grid[newColumn][newRow].piece.team)

def main(WIDTH, ROWS):
    grid = make_grid(ROWS, WIDTH)
    highlightedPiece = None
    currMove = 'W'

    while True:
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                print('EXIT SUCCESSFUL')
                pygame.quit()
                sys.exit()

            # what happens when a node is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                clickedNode = getNode(grid, ROWS, WIDTH)
                ClickedPositionColumn, ClickedPositionRow = clickedNode
                if grid[ClickedPositionColumn][ClickedPositionRow].colour == BLUE or grid[ClickedPositionColumn][ClickedPositionRow].colour == RED:
                    if highlightedPiece:
                        pieceColumn, pieceRow = highlightedPiece
                    if currMove == grid[pieceColumn][pieceRow].piece.team:
                        resetColours(grid, highlightedPiece)
                        currMove=move(grid, highlightedPiece, clickedNode)
                elif highlightedPiece == clickedNode:
                    pass
                else:
                    if grid[ClickedPositionColumn][ClickedPositionRow].piece:
                        if currMove == grid[ClickedPositionColumn][ClickedPositionRow].piece.team:
                            highlightedPiece = highlight(clickedNode, grid, highlightedPiece)

        update_display(SCREEN, grid,ROWS,WIDTH)


main(WIDTH, ROWS)
