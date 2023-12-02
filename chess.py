import os
import pygame
import random
import sys
from itertools import combinations

# current directory
dirname = os.path.dirname(__file__)

WIDTH = 800
ROWS = 8

B_BISHOP = pygame.image.load(os.path.join(dirname, 'images/b_bishop.png'))
B_KING = pygame.image.load(os.path.join(dirname, 'images/b_king.png'))
B_KNIGHT = pygame.image.load(os.path.join(dirname, 'images/b_knight.png'))
B_PAWN = pygame.image.load(os.path.join(dirname, 'images/b_pawn.png'))
B_QUEEN = pygame.image.load(os.path.join(dirname, 'images/b_queen.png'))
B_ROOK = pygame.image.load(os.path.join(dirname, 'images/b_rook.png'))
W_BISHOP = pygame.image.load(os.path.join(dirname, 'images/w_bishop.png'))
W_KING = pygame.image.load(os.path.join(dirname, 'images/w_king.png'))
W_KNIGHT = pygame.image.load(os.path.join(dirname, 'images/w_knight.png'))
W_PAWN = pygame.image.load(os.path.join(dirname, 'images/w_pawn.png'))
W_QUEEN = pygame.image.load(os.path.join(dirname, 'images/w_queen.png'))
W_ROOK = pygame.image.load(os.path.join(dirname, 'images/w_rook.png'))

DARK = (118, 150, 86)
LIGHT = (238, 238, 210)

BLUE = (76, 252, 241)
BLACK = (0,0,0)
ORANGE = (186,202,68)
WHITE = (255,255,255)


pygame.init()
SCREEN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption('Chess')

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

def update_display(win, grid, rows, width):
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()


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
                node.piece = Piece('rook', 'B')
            elif count == 1 or count == 6:
                node.piece = Piece('knight', 'B')
            elif count == 2 or count == 5:
                node.piece = Piece('bishop', 'B')
            elif count == 3:
                node.piece = Piece('queen', 'B')
            elif count == 4:
                node.piece = Piece('king', 'B')
            elif count > 7 and count < 16:
                node.piece = Piece('pawn', 'B')
            elif count == 56 or count == 63:
                node.piece = Piece('rook', 'W')
            elif count == 57 or count == 62:
                node.piece = Piece('knight', 'W')
            elif count == 58 or count == 61:
                node.piece = Piece('bishop', 'W')
            elif count == 59:
                node.piece = Piece('queen', 'W')
            elif count == 60:
                node.piece = Piece('king', 'W')
            elif count > 47 and count < 56:
                node.piece = Piece('pawn', 'W')
            #if (abs(i+j)%2==0) and (i<3):
                #node.piece = Piece('R')
            #elif(abs(i+j)%2==0) and i>4:
                #node.piece=Piece('G')
            count += 1
            grid[i].append(node)
    return grid


def draw_grid(win, rows, width):
    gap = width // ROWS
    for i in range(rows):
        pygame.draw.line(win, DARK, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, DARK, (j * gap, 0), (j * gap, width))

class Piece:
    def __init__(self, name, team):
        self.name = name
        self.team = team
        if self.team == 'B':
            if self.name == 'bishop':
                self.image = B_BISHOP
            elif self.name == 'king':
                self.image = B_KING
            elif self.name == 'knight':
                self.image = B_KNIGHT
            elif self.name == 'queen':
                self.image = B_QUEEN
            elif self.name == 'rook':
                self.image = B_ROOK
            else:
                self.image = B_PAWN
        else:
            if self.name == 'bishop':
                self.image = W_BISHOP
            elif self.name == 'king':
                self.image = W_KING
            elif self.name == 'knight':
                self.image = W_KNIGHT
            elif self.name == 'queen':
                self.image = W_QUEEN
            elif self.name == 'rook':
                self.image = W_ROOK
            else:
                self.image = W_PAWN

        self.type=None

    def draw(self, x, y):
        SCREEN.blit(self.image, (x,y))

def getNode(grid, rows, width):
    gap = width//rows
    RowX,RowY = pygame.mouse.get_pos()
    Row = RowX//gap
    Col = RowY//gap
    return (Col,Row)

def resetColours(grid, node):
    positions = generatePotentialMoves(node, grid)
    positions.append(node)

    for colouredNodes in positions:
        nodeX, nodeY = colouredNodes
        grid[nodeX][nodeY].colour = LIGHT if abs(nodeX - nodeY) % 2 == 0 else DARK

def HighlightpotentialMoves(piecePosition, grid):
    positions = generatePotentialMoves(piecePosition, grid)
    for position in positions:
        Column,Row = position
        grid[Column][Row].colour=BLUE

def opposite(team):
    return "W" if team=="B" else "B"

def generatePotentialMoves(nodePosition, grid):
    checker = lambda x,y: x+y>=0 and x+y<8
    positions= []
    column, row = nodePosition
    if grid[column][row].piece:
        vectors = [[1, -1], [1, 1]] if grid[column][row].piece.team == "B" else [[-1, -1], [-1, 1]]
<<<<<<< Updated upstream
        if grid[column][row].piece.type=='KING':
            vectors = [[1, -1], [1, 1],[-1, -1], [-1, 1]]
=======
        
        if grid[column][row].piece.name =='PAWN':
            if grid[column][row].piece.team =='W':
                vectors = [[-1, 0]]
                if grid[column][row].piece.hasMoved == False:
                    vectors = [[-1, 0], [-2, 0]]
                
            else:
                vectors = [[1, 0]]
                if grid[column][row].piece.hasMoved == False:
                    vectors = [[1, 0], [2, 0]]

        if grid[column][row].piece.name =='KNIGHT':
            vectors = [[-2, 1], [-2, -1], [-1, 2], [-1, -2], [1, -2], [1, 2], [2, -1], [2, 1]] 

        if grid[column][row].piece.name =='KING':
            vectors = [[1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1], [0, 1]] 

        if grid[column][row].piece.name == 'ROOK':
            
        if grid[column][row].piece.name == 'KNIGHT'
        
        
        '''if grid[column][row].piece.name =='BISHOP':

            for i in range(4):
                path = True
                chain = 1
                if i == 0:
                    x = 1
                    y = -1
                elif i == 1:
                    x = -1
                    y = -1
                elif i == 2:
                    x = 1
                    y = 1
                else:
                    x = -1
                    y = 1
                while path:
                    if grid[column + x][row + 1]


                    if (piece[0] + (chain * x), piece[1] + (chain * y)) not in friends_list and \
                            0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                        moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                        if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                            path = False
                        chain += 1
                    else:
                        path = False'''

>>>>>>> Stashed changes
        for vector in vectors:
            columnVector, rowVector = vector
            if checker(columnVector,column) and checker(rowVector,row):
                #grid[(column+columnVector)][(row+rowVector)].colour=ORANGE
                if not grid[(column+columnVector)][(row+rowVector)].piece:
                    positions.append((column + columnVector, row + rowVector))
                elif grid[column+columnVector][row+rowVector].piece and\
                        grid[column+columnVector][row+rowVector].piece.team==opposite(grid[column][row].piece.team):

                    if checker((2* columnVector), column) and checker((2* rowVector), row) \
                            and not grid[(2* columnVector)+ column][(2* rowVector) + row].piece:
                        positions.append((2* columnVector+ column,2* rowVector+ row ))

    return positions

def highlight(ClickedNode, Grid, OldHighlight):
    Column,Row = ClickedNode
    Grid[Column][Row].colour=ORANGE
    if OldHighlight:
        resetColours(Grid, OldHighlight)
    HighlightpotentialMoves(ClickedNode, Grid)
    return (Column,Row)

def move(grid, piecePosition, newPosition):
    resetColours(grid, piecePosition)
    newColumn, newRow = newPosition
    oldColumn, oldRow = piecePosition

    piece = grid[oldColumn][oldRow].piece
    grid[newColumn][newRow].piece=piece
    grid[oldColumn][oldRow].piece = None

    if newColumn==7 and grid[newColumn][newRow].piece.team=='R':
        grid[newColumn][newRow].piece.type='KING'
        #grid[newColumn][newRow].piece.image=REDKING
    if newColumn==0 and grid[newColumn][newRow].piece.team=='G':
        grid[newColumn][newRow].piece.type='KING'
        #grid[newColumn][newRow].piece.image=GREENKING
    if abs(newColumn-oldColumn)==2 or abs(newRow-oldRow)==2:
        grid[int((newColumn+oldColumn)/2)][int((newRow+oldRow)/2)].piece = None
        return grid[newColumn][newRow].piece.team
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

            if event.type == pygame.MOUSEBUTTONDOWN:
                clickedNode = getNode(grid, ROWS, WIDTH)
                ClickedPositionColumn, ClickedPositionRow = clickedNode
                if grid[ClickedPositionColumn][ClickedPositionRow].colour == BLUE:
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
