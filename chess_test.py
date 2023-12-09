########################################################
# NAME: GROUP 4
# NAME1: Edwin Aviles
# NAME2: Sandra Mateiro 
# NAME3: Ricardo Rivas Navarro
# NAME4: Jason Rodriguez
# ASGT: Class Project
# ORGN: CSUB - CMPS 3500
# FILE: chess_test.py
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
WIDTH = 1000
ROWS = 10

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

DARK = (111, 78, 55) # dark green
LIGHT = (210, 180, 140) #light green

BLUE = (76, 252, 241)
BLACK = (0,0,0)
ORANGE = (255, 255, 0) #actually yellow
YELLOW = (235, 168, 52) #actually orange
WHITE = (255,255,255)
RED = (255, 0, 0)

pygame.font.init()
BUTTON_FONT = pygame.font.SysFont("comicsans", 40)


win = ''  #used later to draw menu buttons
winner = ''# flag to determine end of game and winner. Set to empty until a king is checkmated.
saves = []



pygame.init()
SCREEN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption('Chess')
font = pygame.font.Font('freesansbold.ttf', 20)

# keeps track of squares on the board
class Node:

    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = int(row * width)
        self.y = int(col * width)
        self.colour = DARK
        self.piece = None
        self.button = None

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
            if i == 9 and j == 0:
                node.colour = BLACK
                node.button = 'RESET'
            elif i == 0 and j == 9:
                node.colour = BLACK
                node.button = 'QUIT'
            elif i == 9 and j == 9:
                node.colour = BLACK
                node.button = 'TEST'
            elif i == 0 and j == 0:
                node.colour = BLACK
                node.button = 'MENU'
            elif i == 0 or i == 9 or j == 0 or j == 9:
                node.colour = BLACK
            elif abs(i-j) % 2 == 0:
                node.colour=LIGHT
            if count == 11 or count == 18:
                node.piece = Piece('ROOK', 'B')
            elif count == 12 or count == 17:
                node.piece = Piece('KNIGHT', 'B')
            elif count == 13 or count == 16:
                node.piece = Piece('BISHOP', 'B')
            elif count == 14:
                node.piece = Piece('QUEEN', 'B')
            elif count == 15:
                node.piece = Piece('KING', 'B')
            elif count > 20 and count < 29:
                node.piece = Piece('PAWN', 'B')
            elif count == 81 or count == 88:
                node.piece = Piece('ROOK', 'W')
            elif count == 82 or count == 87:
                node.piece = Piece('KNIGHT', 'W')
            elif count == 83 or count == 86:
                node.piece = Piece('BISHOP', 'W')
            elif count == 84:
                node.piece = Piece('QUEEN', 'W')
            elif count == 85:
                node.piece = Piece('KING', 'W')
            elif count > 70 and count < 79:
                node.piece = Piece('PAWN', 'W')
            count += 1
            grid[i].append(node)
    return grid

# test board creator with pieces, sets them to corret spots
def make_test(rows, width):
    grid = []
    gap = width//rows
    count = 0
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(j,i, gap)
            if i == 9 and j == 0:
                node.colour = BLACK
                node.button = 'RESET'
            elif i == 0 and j == 9:
                node.colour = BLACK
                node.button = 'QUIT'
            elif i == 9 and j == 9:
                node.colour = BLACK
                node.button = 'TEST'
            elif i == 0 and j == 0:
                node.colour = BLACK
                node.button = 'MENU'
            elif i == 0 or i == 9 or j == 0 or j == 9:
                node.colour = BLACK
            elif abs(i-j) % 2 == 0:
                node.colour=LIGHT
            if count == 11 or count == 18:
                node.piece = Piece('ROOK', 'B')
            elif count == 33 or count == 36:
                node.piece = Piece('KNIGHT', 'B')
            elif count == 25 or count == 35:
                node.piece = Piece('BISHOP', 'B')
            elif count == 38:
                node.piece = Piece('QUEEN', 'B')
            elif count == 15:
                node.piece = Piece('KING', 'B')
            elif count > 20 and count < 24 or count == 34 or count == 45 or count > 25 and count < 29:
                node.piece = Piece('PAWN', 'B')
                if count == 34 or count == 45:
                    node.piece.hasMoved = True
            elif count == 81 or count == 86:
                node.piece = Piece('ROOK', 'W')
                if count == 86:
                    node.piece.hasMoved = True
            elif count == 51 or count == 66:
                node.piece = Piece('KNIGHT', 'W')
            elif count == 42 or count == 83:
                node.piece = Piece('BISHOP', 'W')
            elif count == 84:
                node.piece = Piece('QUEEN', 'W')
            elif count == 87:
                node.piece = Piece('KING', 'W')
            elif count == 55 or count > 70 and count < 75 or count > 75 and count < 79:
                node.piece = Piece('PAWN', 'W')
                if count == 55:
                    node.piece.hasMoved = True
            count += 1
            grid[i].append(node)
    return grid

# used to draw the board lines
def draw_grid(win, rows, width):
    gap = width // ROWS
    for i in range(rows):
        pygame.draw.line(win, DARK, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, DARK, (j * gap, 0), (j * gap, width))

            # Draw column labels (a-j) on the first and last row
            if i == 0 or i == rows - 1:
                label = chr(ord('a') + j - 1) if 1 <= j <= 8 else ''
                label_text = BUTTON_FONT.render(label, 1, WHITE)
                win.blit(label_text, (j * gap + gap // 2 - label_text.get_width() // 2, i * gap + gap // 2 - label_text.get_height() // 2))

            # Draw row labels (1-8) on the first and last column
            if j == 0 or j == rows - 1:
                label = str(9 - i) if 1 <= i <= 8 else ''
                label_text = BUTTON_FONT.render(label, 1, WHITE)
                win.blit(label_text, (j * gap + gap // 2 - label_text.get_width() // 2, i * gap + gap // 2 - label_text.get_height() // 2))
            
            if i == 0 and j == 0:
                label = 'menu'
                label_text = BUTTON_FONT.render(label, 1, WHITE)
                win.blit(label_text, (j * gap + gap // 2 - label_text.get_width() // 2, i * gap + gap // 2 - label_text.get_height() // 2))
            
            if i == 0 and j == 9:
                label = 'quit'
                label_text = BUTTON_FONT.render(label, 1, WHITE)
                win.blit(label_text, (j * gap + gap // 2 - label_text.get_width() // 2, i * gap + gap // 2 - label_text.get_height() // 2))
            
            if i == 9 and j == 0:
                label = 'reset'
                label_text = BUTTON_FONT.render(label, 1, WHITE)
                win.blit(label_text, (j * gap + gap // 2 - label_text.get_width() // 2, i * gap + gap // 2 - label_text.get_height() // 2))
            
            if i == 9 and j == 9:
                label = 'test'
                label_text = BUTTON_FONT.render(label, 1, WHITE)
                win.blit(label_text, (j * gap + gap // 2 - label_text.get_width() // 2, i * gap + gap // 2 - label_text.get_height() // 2))

# holds the difference pieces on the board
class Piece:
    def __init__(self, name, team):
        self.name = name
        self.team = team
        self.promoted = False
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
        self.kingInCheck = False # for use with Kings. Flag will always be false for non-King pieces.

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
    pieceColumn, pieceRow = piecePosition
    KingCoords = getKingCoords(grid[pieceColumn][pieceRow].piece.team, grid)
    KingColumn, KingRow = KingCoords
    if not grid[KingColumn][KingRow].piece.kingInCheck:
        positions = generatePotentialMoves(piecePosition, grid)
        for position in positions:
            Column,Row = position
            if grid[Column][Row].piece and grid[Column][Row].piece.team != grid[pieceColumn][pieceRow].piece.team:
                grid[Column][Row].colour = RED
            else:
                grid[Column][Row].colour=BLUE
    else:
        basepositions = generatePotentialMoves(piecePosition, grid)
        savepositions = getSaveMoves(grid, KingCoords)
        positions = set(basepositions) & set(savepositions)
        for position in positions:
            Column,Row = position
            if grid[Column][Row].piece and grid[Column][Row].piece.team != grid[pieceColumn][pieceRow].piece.team:
                grid[Column][Row].colour = RED
            else:
                grid[Column][Row].colour=BLUE

# function to check the color of the piece
def opposite(team):
    return "W" if team=="B" else "B"

# calculate moves a piece can take
def generatePotentialMoves(nodePosition, grid):
    global saves
    piece = lambda x,y: x+y>=1 and x+y<9
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
                if row >= 1 and column >= 1 and grid[column - 1][row - 1].piece and grid[column - 1][row - 1].piece.team == opposite(grid[column][row].piece.team):
                    vectors.append([-1, -1])
                if row < 9 and column >= 1 and grid[column - 1][row + 1].piece and grid[column - 1][row + 1].piece.team == opposite(grid[column][row].piece.team):
                    vectors.append([-1, 1])
            else:
                vectors = [[1, 0]]
                if grid[column][row].piece.hasMoved == False and not grid[column + 1][row].piece:
                    vectors = [[1, 0], [2, 0]]  
                if row < 9 and grid[column + 1][row + 1].piece and grid[column + 1][row + 1].piece.team == opposite(grid[column][row].piece.team):
                    vectors.append([1, 1])
                if row >= 1 and grid[column + 1][row - 1].piece and grid[column + 1][row - 1].piece.team == opposite(grid[column][row].piece.team):
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
            while column - up >= 1 and not grid[column - up][row].piece:
                vectors.append([-up, 0])
                up += 1
            if column - up >= 1 and grid[column - up][row].piece and grid[column - up][row].piece.team == opposite(grid[column][row].piece.team):
                vectors.append([-up, 0])
            while 1 <= column + down < 9 and not grid[column + down][row].piece:
                vectors.append([down, 0])
                down += 1
            if column + down < 9 and grid[column + down][row].piece and grid[column + down][row].piece.team == opposite(grid[column][row].piece.team):
                vectors.append([down, 0])
            while 1 <= row - left < 9 and not grid[column][row - left].piece:
                vectors.append([0, -left])
                left += 1
            if row - left >= 1 and grid[column][row - left].piece and grid[column][row - left].piece.team == opposite(grid[column][row].piece.team):
                vectors.append([0, -left])
            while 1 <= row + right < 9 and not grid[column][row + right].piece:
                vectors.append([0, right])
                right += 1
            if row + right < 9 and grid[column][row + right].piece and grid[column][row + right].piece.team == opposite(grid[column][row].piece.team):
                vectors.append([0, right])

        # bishop moveset
        if grid[column][row].piece.name =='BISHOP':
            upLeft = upRight = downLeft = downRight = 1
            while 1 <= column - upLeft < 9 and 1 <= row - upLeft < 9 and not grid[column - upLeft][row - upLeft].piece:
                vectors.append([-upLeft, -upLeft])
                upLeft += 1
            if column - upLeft >= 1 and row - upLeft >= 1 and grid[column - upLeft][row - upLeft].piece and grid[column - upLeft][row - upLeft].piece.team == opposite(grid[column][row].piece.team):
                vectors.append([-upLeft, -upLeft])
            while 1 <= column - upRight < 9 and 1 <= row + upRight < 9 and not grid[column - upRight][row + upRight].piece:
                vectors.append([-upRight, upRight])
                upRight += 1
            if column - upRight >= 1 and row + upRight < 9 and grid[column - upRight][row + upRight].piece and grid[column - upRight][row + upRight].piece.team == opposite(grid[column][row].piece.team):
                vectors.append([-upRight, upRight])
            while 1 <= column + downLeft < 9 and 1 <= row - downLeft < 9 and not grid[column + downLeft][row - downLeft].piece:
                vectors.append([downLeft, -downLeft])
                downLeft += 1
            if column + downLeft < 9 and row - downLeft >= 1 and grid[column + downLeft][row - downLeft].piece and grid[column + downLeft][row - downLeft].piece.team == opposite(grid[column][row].piece.team):
                vectors.append([downLeft, -downLeft])
            while 1 <= column + downRight < 9 and 1 <= row + downRight < 9 and not grid[column + downRight][row + downRight].piece:
                vectors.append([downRight, downRight])
                downRight += 1
            if column + downRight < 9 and row + downRight < 9 and grid[column + downRight][row + downRight].piece and grid[column + downRight][row + downRight].piece.team == opposite(grid[column][row].piece.team):
                vectors.append([downRight, downRight])

        # queen moveset is rook moveset + bishop moveset
        if grid[column][row].piece.name =='QUEEN':
            up = down = left = right = 1
            upLeft = upRight = downLeft = downRight = 1
            while column - up >= 1 and not grid[column - up][row].piece:
                vectors.append([-up, 0])
                up += 1
            if column - up >= 1 and grid[column - up][row].piece and grid[column - up][row].piece.team == opposite(grid[column][row].piece.team):
                vectors.append([-up, 0])
            while 1 <= column + down < 9 and not grid[column + down][row].piece:
                vectors.append([down, 0])
                down += 1
            if column + down < 9 and grid[column + down][row].piece and grid[column + down][row].piece.team == opposite(grid[column][row].piece.team):
                vectors.append([down, 0])
            while 1 <= row - left < 9 and not grid[column][row - left].piece:
                vectors.append([0, -left])
                left += 1
            if row - left >= 1 and grid[column][row - left].piece and grid[column][row - left].piece.team == opposite(grid[column][row].piece.team):
                vectors.append([0, -left])
            while 1 <= row + right < 9 and not grid[column][row + right].piece:
                vectors.append([0, right])
                right += 1
            if row + right < 9 and grid[column][row + right].piece and grid[column][row + right].piece.team == opposite(grid[column][row].piece.team):
                vectors.append([0, right])
            while 1 <= column - upLeft < 9 and 1 <= row - upLeft < 9 and not grid[column - upLeft][row - upLeft].piece:
                vectors.append([-upLeft, -upLeft])
                upLeft += 1
            if column - upLeft >= 1 and row - upLeft >= 1 and grid[column - upLeft][row - upLeft].piece and grid[column - upLeft][row - upLeft].piece.team == opposite(grid[column][row].piece.team):
                vectors.append([-upLeft, -upLeft])
            while 1 <= column - upRight < 9 and 0 <= row + upRight < 9 and not grid[column - upRight][row + upRight].piece:
                vectors.append([-upRight, upRight])
                upRight += 1
            if column - upRight >= 1 and row + upRight < 9 and grid[column - upRight][row + upRight].piece and grid[column - upRight][row + upRight].piece.team == opposite(grid[column][row].piece.team):
                vectors.append([-upRight, upRight])
            while 1 <= column + downLeft < 9 and 0 <= row - downLeft < 9 and not grid[column + downLeft][row - downLeft].piece:
                vectors.append([downLeft, -downLeft])
                downLeft += 1
            if column + downLeft < 9 and row - downLeft >= 1 and grid[column + downLeft][row - downLeft].piece and grid[column + downLeft][row - downLeft].piece.team == opposite(grid[column][row].piece.team):
                vectors.append([downLeft, -downLeft])
            while 1 <= column + downRight < 9 and 1 <= row + downRight < 9 and not grid[column + downRight][row + downRight].piece:
                vectors.append([downRight, downRight])
                downRight += 1
            if column + downRight < 9 and row + downRight < 9 and grid[column + downRight][row + downRight].piece and grid[column + downRight][row + downRight].piece.team == opposite(grid[column][row].piece.team):
                vectors.append([downRight, downRight])



        # determines what will happen if piece moves into new grid slot?
        for vector in vectors:
            columnVector, rowVector = vector
            if piece(columnVector,column) and piece(rowVector,row):
                if not grid[(column+columnVector)][(row+rowVector)].piece:
                    if grid[column][row].piece.name == 'KING': #checking to make sure Kings cannot move into vulnerable spots.
                        enemyList = getEnemyList(opposite(grid[column][row].piece.team), grid)
                        if (column + columnVector, row + rowVector) not in enemyList:
                            positions.append((column + columnVector, row + rowVector))
                    else: 
                        positions.append((column + columnVector, row + rowVector))
                elif grid[column+columnVector][row+rowVector].piece and\
                        grid[column+columnVector][row+rowVector].piece.team==opposite(grid[column][row].piece.team) and\
                        grid[column][row].piece.name != 'PAWN':
                    positions.append((column+columnVector, row+rowVector))
                elif grid[column+columnVector][row+rowVector].piece and\
                        grid[column+columnVector][row+rowVector].piece.team==opposite(grid[column][row].piece.team) and\
                        grid[column][row].piece.name == 'PAWN' and\
                        rowVector != 0:
                    positions.append((column+columnVector, row+rowVector))
        # CASTLING            
        team = grid[column][row].piece.team
        if grid[column][row].piece:
            if ((column == 8 or column == 1) and row == 5):
                if grid[column][row].piece.name == 'KING' and not grid[column][row].piece.kingInCheck: # Adding positions for castling move. Actual move will be handled in move function.
                    if not grid[column][row].piece.hasMoved:
                        if grid[column][1].piece and not grid[column][1].piece.hasMoved:
                            count = 0
                            for i in range(2, 5):
                                if not SpaceUnderAttack(team, (column, i), grid) and isEmpty(grid, (column, i)):
                                    count += 1
                            if count == 3:
                                positions.append((column, 1))
                                # print(positions)
                        if grid[column][8].piece and not grid[column][8].piece.hasMoved:
                            count = 0
                            for i in range(6, 8):
                                if not SpaceUnderAttack(team, (column, i), grid) and isEmpty(grid, (column, i)):
                                    count += 1
                            if count == 2:
                                positions.append((column, 8))
                                # print(positions)
    return positions

# function for getting a list of all possible enemy moves to prevent the King from being able to move there
def getEnemyList(enemyTeam, grid):
    enemyList = []
    for i in range(1, 9):
        for j in range(1, 9): # these for loops cycle through the whole board
            if grid[i][j].piece:
                if grid[i][j].piece.team==enemyTeam and grid[i][j].piece.name != 'KING': # checking if the piece is a piece, is an enemy, and is not a King
                    enemyList.extend(generatePotentialMoves((i, j), grid))  # Code absolutely CANNOT call gPM function on a King, as it will recursively break.
                elif grid[i][j].piece.team==enemyTeam and grid[i][j].piece.name == 'KING': # So here it will add all squares around enemy King to enemyList, to make sure.
                    for x in range(-1, 2):
                        for y in range(-1, 2):
                            enemyList.append((i+x, j+y)) # this adds each coordinate around the enemy King one-by-one.
                if grid[i][j].piece.team==enemyTeam and grid[i][j].piece.name == 'PAWN': # also adding positions where a pawn can take a piece if moved there.
                    enemyList.append((i + 1, j - 1))
                    enemyList.append((i + 1, j + 1))
    return enemyList

def getKingCoords(kingTeam, grid):
    for i in range(1, 9):
        for j in range(1, 9): # these for loops cycle through the whole board
            if grid[i][j].piece:
                if grid[i][j].piece.name == 'KING' and grid[i][j].piece.team == kingTeam:
                    return (i, j)
                    
                
def SpaceUnderAttack(friendlyTeam, coords, grid):
    enemyList = getEnemyList(opposite(friendlyTeam), grid)
    if coords in enemyList:
        return True
    else:
        return False

def kingsMonitor(grid): # pass this function in main game loop, wil handle checking, unchecking, checkmate
    bKingCoords = getKingCoords('B', grid)
    wKingCoords = getKingCoords('W', grid)
    wAttacks = getEnemyList('W', grid)
    bAttacks = getEnemyList('B', grid)
    bKingX, bKingY = bKingCoords
    wKingX, wKingY = wKingCoords
    global saves    
    if SpaceUnderAttack('B', bKingCoords, grid): # if the black king is in check
        grid[bKingX][bKingY].piece.kingInCheck = True
        grid[bKingX][bKingY].colour = YELLOW
        #print(saves)
        if len(getSaveMoves(grid, bKingCoords)) <= 1 and len(generatePotentialMoves((bKingX, bKingY), grid)) < 1:
            checkmate(grid, (bKingX, bKingY))
        #print('CaseA')
    elif SpaceUnderAttack('W', wKingCoords, grid): # if the white king is in check
        grid[wKingX][wKingY].piece.kingInCheck = True
        grid[wKingX][wKingY].colour = YELLOW
        #print(saves)
        if len(getSaveMoves(grid, wKingCoords)) <= 1 and len(generatePotentialMoves((wKingX, wKingY), grid)) < 1:
            checkmate(grid, (wKingX, wKingY))
        #print('CaseB')
    elif (not SpaceUnderAttack('W', wKingCoords, grid) and not SpaceUnderAttack('B', bKingCoords, grid)): # if neither king is in check
        if grid[wKingX][wKingY].piece.kingInCheck or grid[bKingX][bKingY].piece.kingInCheck:
            grid[wKingX][wKingY].piece.kingInCheck = False
            grid[bKingX][bKingY].piece.kingInCheck = False
            saves = []
            resetColours(grid, (wKingX, wKingY))
            resetColours(grid, (bKingX, bKingY))
            #print('CaseC')
    

        
def checkmate(grid, kingCoords):
    kingX, kingY = kingCoords
    global winner
    global gameOver
    winner = opposite(grid[kingX][kingY].piece.team)
    gameOver = True
    if winner == 'B':
            pygame.draw.rect(SCREEN, 'black', [200, 200, 400, 70])
            SCREEN.blit(font.render(f'Black won the match!', True, 'white'), (210, 210))
            SCREEN.blit(font.render(f'Press Enter to Restart!', True, 'white'), (210, 240))
    elif winner == 'W':
        pygame.draw.rect(SCREEN, 'black', [200, 200, 400, 70])
        SCREEN.blit(font.render(f'White won the match!', True, 'white'), (210, 210))
        SCREEN.blit(font.render(f'Press Enter to Restart!', True, 'white'), (210, 240))
    
        
def getSaveMoves(grid, kingCoords):
    saves = []
    lineOfAttack = []
    kingX, kingY = kingCoords
    attackX = 9
    attackY = 9 # initializing
    for i in range(1, 9):
        for j in range(1, 9): # these for loops cycle through the whole board
            if grid[i][j].piece:
                if grid[kingX][kingY].piece.team != grid[i][j].piece.team and grid[i][j].piece.name != 'KING': # if the current space is a piece AND it's an enemy piece
                    if kingCoords in generatePotentialMoves((i, j), grid):
                        attackX = i
                        attackY = j
    lineOfAttack.append((attackX, attackY)) # The piece itself counts in the LoA, as capturing the piece is a save move.
    saves.append((attackX, attackY))
    if (1 <= attackX < 9) and (1 <= attackY < 9):
        if grid[attackX][attackY].piece.name == 'ROOK':
            if attackX == kingX:
                if kingY > attackY:
                    for k in range(attackY, kingY):
                        lineOfAttack.append((attackX, k))
                else:
                    for k in range(kingY, attackY):
                        lineOfAttack.append((attackX, k))
            elif attackY == kingY:
                if kingX > attackX:
                    for k in range(attackX, kingX):
                        lineOfAttack.append((k, attackY))
                else:
                    for k in range(kingX, attackX):
                        lineOfAttack.append((attackX, k))
        elif grid[attackX][attackY].piece.name == 'BISHOP':
            if attackY > kingY and attackX > kingX:
                i = kingX + 1
                j = kingY + 1
                while i < attackX and j < attackY:
                    lineOfAttack.append((i, j))
                    i += 1
                    j += 1
            elif attackY > kingY and attackX < kingX:
                i = kingX - 1
                j = kingY + 1
                while i > attackX and j < attackY:
                    lineOfAttack.append((i, j))
                    i -= 1
                    j += 1
            elif attackY < kingY and attackX < kingX:
                i = kingX - 1
                j = kingY - 1
                while i > attackX and j > attackY:
                    lineOfAttack.append((i, j))
                    i -= 1
                    j -= 1
            elif attackY < kingY and attackX > kingX:
                i = kingX + 1
                j = kingY - 1
                while i < attackX and j > attackY:
                    lineOfAttack.append((i, j))
                    i += 1
                    j -= 1
        elif grid[attackX][attackY].piece.name == 'QUEEN':
            if attackX == kingX:
                if kingY > attackY:
                    for k in range(attackY, kingY):
                        lineOfAttack.append((attackX, k))
                else:
                    for k in range(kingY, attackY):
                        lineOfAttack.append((attackX, k))
            elif attackY == kingY:
                if kingX > attackX:
                    for k in range(attackX, kingX):
                        lineOfAttack.append((k, attackY))
                else:
                    for k in range(kingX, attackX):
                        lineOfAttack.append((attackX, k))
            elif attackY > kingY and attackX > kingX:
                i = kingX + 1
                j = kingY + 1
                while i < attackX and j < attackY:
                    lineOfAttack.append((i, j))
                    i += 1
                    j += 1
            elif attackY > kingY and attackX < kingX:
                i = kingX - 1
                j = kingY + 1
                while i > attackX and j < attackY:
                    lineOfAttack.append((i, j))
                    i -= 1
                    j += 1
            elif attackY < kingY and attackX < kingX:
                i = kingX - 1
                j = kingY - 1
                while i > attackX and j > attackY:
                    lineOfAttack.append((i, j))
                    i -= 1
                    j -= 1
            elif attackY < kingY and attackX > kingX:
                i = kingX + 1
                j = kingY - 1
                while i < attackX and j > attackY:
                    lineOfAttack.append((i, j))
                    i += 1
                    j -= 1
    # print(lineOfAttack)
    
    testCoords = []
    for i in range(1, 9):
        for j in range(1, 9): # these for loops cycle through the whole board
            if grid[i][j].piece: # if piece is friendly and not the king
                enemyList = getEnemyList(grid[i][j].piece.team, grid)
                if grid[i][j].piece.team == grid[kingX][kingY].piece.team and grid[i][j].piece.name != 'KING':
                    potentialMoves = generatePotentialMoves((i, j), grid)
                    for a in range(1, 9):
                        for b in range(1, 9):
                            if ((a, b) in potentialMoves) and ((a, b) in lineOfAttack):
                                saves.append((a, b))
                elif grid[i][j].piece.team == grid[kingX][kingY].piece.team and grid[i][j].piece.name == 'KING':
                        for x in range(-1, 2): # cycles through spaces around the King to add saves
                            for y in range(-1, 2): # below is if the space is not under attack, and the space is within the range of the board
                                testX = i + x
                                testY = j + y
                                if ((1 <= testX < 9) and (1 <= testY < 9)):
                                    if grid[testX][testY].piece and grid[testX][testY].piece.team != grid[i][j].piece.team:
                                        testCoords.append((testX, testY)) # if there's a piece and it's an enemy piece
                                    elif not grid[testX][testY].piece:
                                        testCoords.append((testX, testY)) # if there's no piece                
    safeCoords = set(testCoords) - set(enemyList)
    saves.extend(safeCoords)                                
    print(len(saves))
    return saves

def isEmpty(grid, Coords):
    CoordsX, CoordsY = Coords
    if grid[CoordsX][CoordsY].piece:
        return False
    else:
        return True

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
    # Castling handling
    if ((grid[newColumn][newRow].piece and grid[oldColumn][oldRow].piece) and (grid[newColumn][newRow].piece.team == grid[oldColumn][oldRow].piece.team)):
        if (grid[newColumn][newRow].piece.name == 'ROOK'):
            if newRow == 1:
                rook = grid[oldColumn][1].piece
                piece = grid[oldColumn][oldRow].piece
                
                grid[oldColumn][oldRow - 2].piece = piece
                grid[oldColumn][oldRow].piece = None
                grid[oldColumn][oldRow - 1].piece = rook
                grid[oldColumn][1].piece = None

                grid[oldColumn][oldRow - 2].piece.hasMoved = True
                grid[oldColumn][oldRow - 1].piece.hasMoved = True

                return opposite(grid[oldColumn][oldRow - 2].piece.team)
            elif newRow == 8:
                rook = grid[oldColumn][8].piece
                piece = grid[oldColumn][oldRow].piece
                
                grid[oldColumn][oldRow + 2].piece = piece
                grid[oldColumn][oldRow].piece = None
                grid[oldColumn][oldRow + 1].piece = rook
                grid[oldColumn][8].piece = None

                grid[oldColumn][oldRow + 2].piece.hasMoved = True
                grid[oldColumn][oldRow + 1].piece.hasMoved = True

                return opposite(grid[oldColumn][oldRow + 2].piece.team)
    else:
        piece = grid[oldColumn][oldRow].piece
        grid[newColumn][newRow].piece = piece
        grid[oldColumn][oldRow].piece = None

        grid[newColumn][newRow].piece.hasMoved = True
        # Check for pawn promotion when reaching the first or last column
        if piece.name == 'PAWN' and (newColumn == 1 or newColumn == 8):
            promote_pawn(grid, newColumn, newRow)

        return opposite(grid[newColumn][newRow].piece.team)
# Modify the promote_pawn function

def promote_pawn(grid, column, row):
    # Set the promoted piece to queen
    grid[column][row].piece = Piece('QUEEN', grid[column][row].piece.team)

def main(WIDTH, ROWS):
    grid = make_test(ROWS, WIDTH)
    highlightedPiece = None
    currMove = 'W'
    global winner
    global gameOver
    gameOver = False

    while True:
        kingsMonitor(grid)
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                print('EXIT SUCCESSFUL')
                pygame.quit()
                sys.exit()

            # what happens when a node is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                clickedNode = getNode(grid, ROWS, WIDTH)
                #print(clickedNode)
                ClickedPositionColumn, ClickedPositionRow = clickedNode
                if grid[ClickedPositionColumn][ClickedPositionRow].colour == BLUE or grid[ClickedPositionColumn][ClickedPositionRow].colour == RED:
                    if highlightedPiece:
                        pieceColumn, pieceRow = highlightedPiece
                    if currMove == grid[pieceColumn][pieceRow].piece.team:
                        resetColours(grid, highlightedPiece)
                        currMove=move(grid, highlightedPiece, clickedNode)
                elif grid[ClickedPositionColumn][ClickedPositionRow].colour == BLACK:
                    if grid[ClickedPositionColumn][ClickedPositionRow].button == 'RESET':
                        grid = make_grid(ROWS, WIDTH)
                        highlightedPiece = None
                        currMove = 'W'
                    elif grid[ClickedPositionColumn][ClickedPositionRow].button == 'QUIT':
                        print('EXIT SUCCESSFUL')
                        pygame.quit()
                        sys.exit()
                    elif grid[ClickedPositionColumn][ClickedPositionRow].button == 'TEST':
                        grid = make_test(ROWS, WIDTH)
                        highlightedPiece = None
                        currMove = 'W'
                    elif grid[ClickedPositionColumn][ClickedPositionRow].button == 'MENU':
                        #button for menu goes here
                        print("Menu has not been implimented yet!")
                elif highlightedPiece == clickedNode:
                    pass
                else:
                    if grid[ClickedPositionColumn][ClickedPositionRow].piece:
                        if currMove == grid[ClickedPositionColumn][ClickedPositionRow].piece.team:
                            highlightedPiece = highlight(clickedNode, grid, highlightedPiece)
            if event.type == pygame.KEYDOWN and gameOver:
                gameOver = False
                grid = make_grid(ROWS, WIDTH)
                highlightedPiece = None
                currMove = 'W'
                winner = ''
        if not gameOver:
            update_display(SCREEN, grid,ROWS,WIDTH)
        pygame.display.flip()


main(WIDTH, ROWS)