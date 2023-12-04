import pygame, sys
from button import Button
import random
from itertools import combinations
import os

dirname = os.path.dirname(__file__)

WIDTH = 800
ROWS = 8

RED= pygame.image.load(os.path.join(dirname, 'images/red.png'))
GREEN= pygame.image.load(os.path.join(dirname, 'images/green.png'))

REDKING = pygame.image.load(os.path.join(dirname, 'images/redking.png'))
GREENKING = pygame.image.load(os.path.join(dirname, 'images/greenking.png'))

WHITE = (255,255,255)
BLACK = (0,0,0)
ORANGE = (235, 168, 52)
BLUE = (76, 252, 241)

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def play():

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
        resetColours(grid, piecePosition)
        newColumn, newRow = newPosition
        oldColumn, oldRow = piecePosition

        piece = grid[oldColumn][oldRow].piece
        grid[newColumn][newRow].piece=piece
        grid[oldColumn][oldRow].piece = None

        if newColumn==7 and grid[newColumn][newRow].piece.team=='R':
            grid[newColumn][newRow].piece.type='KING'
            grid[newColumn][newRow].piece.image=REDKING
        if newColumn==0 and grid[newColumn][newRow].piece.team=='G':
            grid[newColumn][newRow].piece.type='KING'
            grid[newColumn][newRow].piece.image=GREENKING
        if abs(newColumn-oldColumn)==2 or abs(newRow-oldRow)==2:
            grid[int((newColumn+oldColumn)/2)][int((newRow+oldRow)/2)].piece = None
            return grid[newColumn][newRow].piece.team
        return opposite(grid[newColumn][newRow].piece.team)




    def main(WIDTH, ROWS):
        grid = make_grid(ROWS, WIDTH)
        highlightedPiece = None
        currMove = 'G'

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


            update_display(WIN, grid,ROWS,WIDTH)


    main(WIDTH, ROWS)
    
'''def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()'''

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 250), 
                            text_input="CHECKERS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
                            text_input="CHESS?", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()