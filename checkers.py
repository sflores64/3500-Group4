import pygame
import random
import sys
from itertools import combinations
import os


# Constants 
WIDTH = 1000
ROWS = 10
WHITE = (255,255,255)
BLACK = (0,0,0)
ORANGE = (235, 168, 52)
BLUE = (76, 252, 241)

# Load images
dirname = os.path.dirname(__file__)
RED= pygame.image.load(os.path.join(dirname, 'images/red.png'))
GREEN= pygame.image.load(os.path.join(dirname, 'images/green.png'))
REDKING = pygame.image.load(os.path.join(dirname, 'images/redking.png'))
GREENKING = pygame.image.load(os.path.join(dirname, 'images/greenking.png'))

# Initialize Pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Load sounds
kinged_sound = pygame.mixer.Sound('sounds/chime.wav')

# Set up game window
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption('Checkers')

# Fonts
GAME_OVER_FONT = pygame.font.SysFont("comicsans", 100)
BUTTON_FONT = pygame.font.SysFont("comicsans", 40)
EXIT_BUTTON_COLOR = (200, 0, 0)

# Global Variables
game_over = False
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
    gap = width // rows
    count = 0
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(j, i, gap)

            # Check if in the central 8x8 area
            if 1 <= i <= 8 and 1 <= j <= 8:
                if abs(i - j) % 2 == 0:
                    node.colour = BLACK
                if (abs(i + j) % 2 == 0) and (i < 4):
                    node.piece = Piece('R')
                elif (abs(i + j) % 2 == 0) and i > 5:
                    node.piece = Piece('G')
            else:
                node.colour = 'dimgrey'  # Set color to grey for the border area
                node.piece = None

            count += 1
            grid[i].append(node)
    return grid

def draw_grid(win, rows, width):
    gap = width // ROWS

    for i in range(rows):
        pygame.draw.line(win, BLACK, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, BLACK, (j * gap, 0), (j * gap, width))

            # Draw column labels (a-j) on the first and last row
            if i == 0 or i == rows - 1:
                label = chr(ord('a') + j - 1) if 1 <= j <= 8 else ''
                label_text = BUTTON_FONT.render(label, 1, BLACK)
                win.blit(label_text, (j * gap + gap // 2 - label_text.get_width() // 2, i * gap + gap // 2 - label_text.get_height() // 2))

            # Draw row labels (1-8) on the first and last column
            if j == 0 or j == rows - 1:
                label = str(i + 0) if 1 <= i <= 8 else ''
                label_text = BUTTON_FONT.render(label, 1, BLACK)
                win.blit(label_text, (j * gap + gap // 2 - label_text.get_width() // 2, i * gap + gap // 2 - label_text.get_height() // 2))
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
    valid_positions = []
    forced_captures = hasForcedCaptures(grid, grid[piecePosition[0]][piecePosition[1]].piece.team)

    for position in positions:
        Column, Row = position
        is_valid_move = (forced_captures and abs(position[0] - piecePosition[0]) == 2) or \
                         (not forced_captures and grid[Column][Row].colour == BLACK)
        if is_valid_move:
            valid_positions.append(position)
            grid[Column][Row].colour = BLUE

    return valid_positions

def opposite(team):
    return "R" if team=="G" else "G"

def generatePotentialMoves(nodePosition, grid):
    checker = lambda x, y: 1 <= x + y <= 16  # Update to 16
    positions = []
    column, row = nodePosition

    # Check if in the central 8x8 area
    if 1 <= column <= 8 and 1 <= row <= 8:
        if grid[column][row].piece:
            vectors = [[1, -1], [1, 1]] if grid[column][row].piece.team == "R" else [[-1, -1], [-1, 1]]
            if grid[column][row].piece.type == 'KING':
                vectors = [[1, -1], [1, 1], [-1, -1], [-1, 1]]
            for vector in vectors:
                columnVector, rowVector = vector
                if checker(columnVector, column) and checker(rowVector, row):
                    destination = (column + columnVector, row + rowVector)
                    if not grid[destination[0]][destination[1]].piece and \
                            1 <= destination[0] <= 8 and 1 <= destination[1] <= 8:
                        positions.append(destination)
                    elif grid[destination[0]][destination[1]].piece and \
                            grid[destination[0]][destination[1]].piece.team == opposite(grid[column][row].piece.team):
                        jumpDestination = (column + 2 * columnVector, row + 2 * rowVector)
                        if checker((2 * columnVector), column) and checker((2 * rowVector), row) \
                                and not grid[jumpDestination[0]][jumpDestination[1]].piece and \
                                1 <= jumpDestination[0] <= 8 and 1 <= jumpDestination[1] <= 8:
                            positions.append(jumpDestination)

    return positions

def hasForcedCaptures(grid, player):
    for i in range(ROWS):
        for j in range(ROWS):
            if grid[i][j].piece and grid[i][j].piece.team == player:
                moves = generatePotentialMoves((i, j), grid)
                for move in moves:
                    if abs(move[0] - i) == 2:
                        return True
    return False

def check_win_conditions(grid, currMove):
    if all(grid[i][j].piece is None or grid[i][j].piece.team == currMove for i in range(ROWS) for j in range(ROWS)):
        return True
    
    for i in range(ROWS):
        for j in range(ROWS):
            if grid[i][j].piece and grid[i][j].piece.team == opposite(currMove):
                moves = generatePotentialMoves((i, j), grid)
                if moves:
                    return False
    return True

def game_over_screen(winner):
    WIN.fill(WHITE)

    game_over_text = GAME_OVER_FONT.render(f"Team {winner} wins!", 1, BLACK)
    WIN.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, 200))

    exit_button = pygame.draw.rect(WIN, EXIT_BUTTON_COLOR, (WIDTH // 2 - 100, 400, 200, 50))
    exit_text = BUTTON_FONT.render("Exit", 1, WHITE)
    WIN.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, 415))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if exit_button.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()


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
    grid[newColumn][newRow].piece = piece
    grid[oldColumn][oldRow].piece = None

    # Check for kinging conditions
    if newColumn == 1 and grid[newColumn][newRow].piece.team == 'G':
        grid[newColumn][newRow].piece.type = 'KING'
        grid[newColumn][newRow].piece.image = GREENKING
        kinged_sound.play()
    elif newColumn == 8 and grid[newColumn][newRow].piece.team == 'R':
        grid[newColumn][newRow].piece.type = 'KING'
        grid[newColumn][newRow].piece.image = REDKING
        kinged_sound.play()

    if abs(newColumn - oldColumn) == 2 or abs(newRow - oldRow) == 2:
        grid[int((newColumn + oldColumn) / 2)][int((newRow + oldRow) / 2)].piece = None
        return grid[newColumn][newRow].piece.team
    return opposite(grid[newColumn][newRow].piece.team)

def main(WIDTH, ROWS):
    global game_over
    grid = make_grid(ROWS, WIDTH)
    highlightedPiece = None
    currMove = 'G'

    # Main game loop
    while not game_over:
        # Check for events
        for event in pygame.event.get():
            # Window is closed
            if event.type == pygame.QUIT:
                print('EXIT SUCCESSFUL')
                pygame.quit()
                sys.exit()
            # Mouse pressed down
            if event.type == pygame.MOUSEBUTTONDOWN:
                clickedNode = getNode(grid, ROWS, WIDTH)
                # Check if clickedNode is not None
                if clickedNode is not None:
                    ClickedPositionColumn, ClickedPositionRow = clickedNode
                    # Clicked on a Blue Area
                    if grid[ClickedPositionColumn][ClickedPositionRow].colour == BLUE:
                        if highlightedPiece:
                            pieceColumn, pieceRow = highlightedPiece
                            # Check if there are forced captures
                            if hasForcedCaptures(grid, currMove):
                                print(f"Forced capture available for {currMove}")
                                # Reset colors before highlighting forced capture path
                                resetColours(grid, highlightedPiece)
                                # Get valid forced capture moves
                                valid_forced_moves = [
                                    move for move in generatePotentialMoves(highlightedPiece, grid)
                                    if abs(move[0] - pieceColumn) == 2  # Check if it's a capture move
                                ]
                                if clickedNode in valid_forced_moves:
                                    currMove = move(grid, highlightedPiece, clickedNode)
                                    game_over = check_win_conditions(grid, currMove)
                                    if game_over:
                                        print(f'Team {currMove} wins!')
                                        game_over_screen(currMove)
                            # If not in a forced capture scenario, handle regular move
                            else:
                                currMove = move(grid, highlightedPiece, clickedNode)
                                game_over = check_win_conditions(grid, currMove)
                                if game_over:
                                    print(f'Team {currMove} wins!')
                                    game_over_screen(currMove)
                    # Ensure that ClickedPositionColumn and ClickedPositionRow are assigned before this block
                    elif grid[ClickedPositionColumn][ClickedPositionRow].piece:
                        if currMove == grid[ClickedPositionColumn][ClickedPositionRow].piece.team:
                            highlightedPiece = highlight(clickedNode, grid, highlightedPiece)

        update_display(WIN, grid, ROWS, WIDTH)

main(WIDTH, ROWS)

