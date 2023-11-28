########################################################
# CMPS 3500 - Class Project
# Checkers game simulator
# This is a program that will simulate a checkers board
# and provide basic game functionalities.
# This program does not abide all rules of checkers
########################################################

import pygame
import random
import sys
from itertools import combinations
import os

# current directory
dirname = os.path.dirname(__file__)

WIDTH = 800
ROWS = 8

# CHECKERS PIECES
###################
RED= pygame.image.load(os.path.join(dirname, 'images/red.png'))
GREEN= pygame.image.load(os.path.join(dirname, 'images/green.png'))

REDKING = pygame.image.load(os.path.join(dirname, 'images/redking.png'))
GREENKING = pygame.image.load(os.path.join(dirname, 'images/greenking.png'))

# CHESS PIECES
##########################
BLACKKING = pygame.image.load(os.path.join(dirname, 'images/b_king.png'))
BLACKBISHOP = pygame.image.load(os.path.join(dirname, 'images/b_bishop.png'))
BLACKKNIGHT = pygame.image.load(os.path.join(dirname, 'images/b_knight.png'))
BLACKPAWN = pygame.image.load(os.path.join(dirname, 'images/b_pawn.png'))
BLACKQUEEN = pygame.image.load(os.path.join(dirname, 'images/b_queen.png'))
BLACKROOK = pygame.image.load(os.path.join(dirname, 'images/b_rook.png'))

WHITEKING = pygame.image.load(os.path.join(dirname, 'images/w_king.png'))
WHITEBISHOP = pygame.image.load(os.path.join(dirname, 'images/w_bishop.png'))
WHITEKNIGHT = pygame.image.load(os.path.join(dirname, 'images/w_knight.png'))
WHITEPAWN = pygame.image.load(os.path.join(dirname, 'images/w_pawn.png'))
WHITEQUEEN = pygame.image.load(os.path.join(dirname, 'images/w_queen.png'))
WHITEROOK = pygame.image.load(os.path.join(dirname, 'images/w_rook.png'))

WHITE = (255,255,255)
BLACK = (0,0,0)
ORANGE = (235, 168, 52)
BLUE = (76, 252, 241)


pygame.init()
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption('Checkers')

priorMoves=[]
class Node:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = int(row * width)
        self.y = int(col * width)
        self.colour = WHITE
        self.piece = None

    def draw(self, WIN):
        pygame.draw.rect(WIN, self.colour, (self.x, self.y, WIDTH / ROWS, WIDTH / ROWS))
        if self.piece:
            WIN.blit(self.piece.image, (self.x, self.y))


def update_display(win, grid, rows, width):
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()


def make_grid(rows, width):
    grid = []
    gap = width// rows
    count = 0
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(j,i, gap)
            if abs(i-j) % 2 == 0:
                node.colour=BLACK
            if (abs(i+j)%2==0) and (i<3):
                node.piece = Piece('R')
            elif(abs(i+j)%2==0) and i>4:
                node.piece=Piece('G')
            count+=1
            grid[i].append(node)
    return grid


def draw_grid(win, rows, width):
    gap = width // ROWS
    for i in range(rows):
        pygame.draw.line(win, BLACK, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, BLACK, (j * gap, 0), (j * gap, width))

RED_PIECES_COUNT = 12
GREEN_PIECES_COUNT = 12

class Piece:
    def __init__(self, team):
        self.team=team
        self.image= RED if self.team=='R' else GREEN
        self.type=None

    def draw(self, x, y):
        WIN.blit(self.image, (x,y))


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
        grid[nodeX][nodeY].colour = BLACK if abs(nodeX - nodeY) % 2 == 0 else WHITE

def HighlightpotentialMoves(piecePosition, grid):
    positions = generatePotentialMoves(piecePosition, grid)
    for position in positions:
        Column,Row = position
        grid[Column][Row].colour=BLUE

def opposite(team):
    return "R" if team=="G" else "G"

def generatePotentialMoves(nodePosition, grid):
    checker = lambda x,y: x+y>=0 and x+y<8
    positions= []
    column, row = nodePosition
    if grid[column][row].piece:
        vectors = [[1, -1], [1, 1]] if grid[column][row].piece.team == "R" else [[-1, -1], [-1, 1]]
        if grid[column][row].piece.type=='KING':
            vectors = [[1, -1], [1, 1],[-1, -1], [-1, 1]]
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


"""
Error with locating possible moves row col error
"""
def highlight(ClickedNode, Grid, OldHighlight):
    Column,Row = ClickedNode
    Grid[Column][Row].colour=ORANGE
    if OldHighlight:
        resetColours(Grid, OldHighlight)
    HighlightpotentialMoves(ClickedNode, Grid)
    return (Column,Row)

def move(grid, piecePosition, newPosition):
    global RED_PIECES_COUNT, GREEN_PIECES_COUNT
    resetColours(grid, piecePosition)
    newColumn, newRow = newPosition
    oldColumn, oldRow = piecePosition

    piece = grid[oldColumn][oldRow].piece
    grid[newColumn][newRow].piece = piece
    grid[oldColumn][oldRow].piece = None

    if newColumn == 7 and grid[newColumn][newRow].piece.team == 'R':
        grid[newColumn][newRow].piece.type = 'KING'
        grid[newColumn][newRow].piece.image = REDKING
    if newColumn == 0 and grid[newColumn][newRow].piece.team == 'G':
        grid[newColumn][newRow].piece.type = 'KING'
        grid[newColumn][newRow].piece.image = GREENKING

    if abs(newColumn - oldColumn) == 2 or abs(newRow - oldRow) == 2:
        grid[int((newColumn + oldColumn) / 2)][int((newRow + oldRow) / 2)].piece = None
        if grid[newColumn][newRow].piece.team == 'R':
            GREEN_PIECES_COUNT -= 1
        elif grid[newColumn][newRow].piece.team == 'G':
            RED_PIECES_COUNT -= 1

        # Check for a winner
        if RED_PIECES_COUNT == 0:
            print("Green wins!")
            display_winner("Green", WIDTH) 
        elif GREEN_PIECES_COUNT == 0:
            print("Red wins!")
            display_winner("Red", WIDTH) 

        return grid[newColumn][newRow].piece.team

    return opposite(grid[newColumn][newRow].piece.team)


def reset_game():
    global RED_PIECES_COUNT, GREEN_PIECES_COUNT
    RED_PIECES_COUNT = 12
    GREEN_PIECES_COUNT = 12


def display_winner(winner, WIDTH):
    pygame.init()
    win_size = (int(WIDTH * 0.4), int(WIDTH * 0.3))
    WIN = pygame.display.set_mode(win_size)
    pygame.display.set_caption('Game Over')

    font_size = int(WIDTH * 0.05)
    font = pygame.font.Font(None, font_size)
    text = font.render(f"{winner} wins!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(win_size[0] // 2, win_size[1] // 3))

    button_size = (win_size[0] // 3, win_size[1] // 7)
    play_again_rect = pygame.Rect(win_size[0] // 2 - button_size[0] // 2, int(win_size[1] * 0.6), *button_size)
    exit_rect = pygame.Rect(win_size[0] // 2 - button_size[0] // 2, int(win_size[1] * 0.75), *button_size)

    button_color = (200, 0, 0)
    button_text_size = int(WIDTH * 0.03)
    button_font = pygame.font.Font(None, button_text_size)

    play_again_text = button_font.render("Play Again", True, (255, 255, 255))
    play_again_text_rect = play_again_text.get_rect(center=play_again_rect.center)

    exit_text = button_font.render("Exit", True, (255, 255, 255))
    exit_text_rect = exit_text.get_rect(center=exit_rect.center)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('EXIT SUCCESSFUL')
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_again_rect.collidepoint(event.pos):
                    reset_game()  # Reset the game state
                    return True  # Signal to play again
                elif exit_rect.collidepoint(event.pos):
                    print('EXIT SUCCESSFUL')
                    pygame.quit()
                    sys.exit()

        WIN.fill((0, 0, 0))
        pygame.draw.rect(WIN, button_color, play_again_rect)
        pygame.draw.rect(WIN, button_color, exit_rect)
        WIN.blit(play_again_text, play_again_text_rect)
        WIN.blit(exit_text, exit_text_rect)
        WIN.blit(text, text_rect)

        pygame.display.flip()


def main(WIDTH, ROWS):
    global RED_PIECES_COUNT, GREEN_PIECES_COUNT
    play_again = True  # Initial value to enter the loop

    while play_again:
        reset_game()  # Reset the game state
        grid = make_grid(ROWS, WIDTH)
        highlightedPiece = None
        currMove = 'G'

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print('EXIT SUCCESSFUL')
                    pygame.quit()
                    sys.exit()

                # Check for the "1" key press to decrement red pieces count
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                    RED_PIECES_COUNT = 0

                if event.type == pygame.MOUSEBUTTONDOWN:
                    clickedNode = getNode(grid, ROWS, WIDTH)
                    ClickedPositionColumn, ClickedPositionRow = clickedNode
                    if grid[ClickedPositionColumn][ClickedPositionRow].colour == BLUE:
                        if highlightedPiece:
                            pieceColumn, pieceRow = highlightedPiece
                        if currMove == grid[pieceColumn][pieceRow].piece.team:
                            resetColours(grid, highlightedPiece)
                            currMove = move(grid, highlightedPiece, clickedNode)
                    elif highlightedPiece == clickedNode:
                        pass
                    else:
                        if grid[ClickedPositionColumn][ClickedPositionRow].piece:
                            if currMove == grid[ClickedPositionColumn][ClickedPositionRow].piece.team:
                                highlightedPiece = highlight(clickedNode, grid, highlightedPiece)

            update_display(WIN, grid, ROWS, WIDTH)

            # Check for a winner after each iteration
            if RED_PIECES_COUNT == 0 or GREEN_PIECES_COUNT == 0:
                play_again = display_winner("Green" if RED_PIECES_COUNT == 0 else "Red", WIDTH)
                if play_again:
                    break  # Break out of the inner loop to reset the game

main(WIDTH, ROWS)


