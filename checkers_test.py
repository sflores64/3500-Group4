import pygame
import random
import sys
from itertools import combinations
import os

# Constants
WIDTH = 1000
ROWS = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (235, 168, 52)
BLUE = (76, 252, 241)

# Load images
dirname = os.path.dirname(__file__)
RED = pygame.image.load(os.path.join(dirname, 'images/red.png'))
GREEN = pygame.image.load(os.path.join(dirname, 'images/green.png'))
REDKING = pygame.image.load(os.path.join(dirname, 'images/redking.png'))
GREENKING = pygame.image.load(os.path.join(dirname, 'images/greenking.png'))

# Initialize Pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Load sounds
kinged_sound = pygame.mixer.Sound('sounds/chime.wav')

# Set up game window
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption('Checkers')

# Fonts
GAME_OVER_FONT = pygame.font.SysFont("comicsans", 100)
BUTTON_FONT = pygame.font.SysFont("comicsans", 40)
EXIT_BUTTON_COLOR = (200, 0, 0)

# Global Variables
game_over = False
priorMoves = []
  
# Class representing a grid node
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

# Function to update the display
def update_display(win, grid, rows, width):
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()

# Function to create the game grid
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
                node.colour = (33, 33, 33)  # Set color to grey for the border area
                node.piece = None

            count += 1
            grid[i].append(node)
    return grid

# Function to draw the grid lines
def draw_grid(win, rows, width):
    gap = width // ROWS

    for i in range(rows):
        pygame.draw.line(win, BLACK, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, BLACK, (j * gap, 0), (j * gap, width))

            # Draw column labels (a-j) on the first and last row
            if i == 0 or i == rows - 1:
                label = chr(ord('a') + j - 1) if 1 <= j <= 8 else ''
                label_text = BUTTON_FONT.render(label, 1, WHITE)
                win.blit(label_text, (j * gap + gap // 2 - label_text.get_width() // 2, i * gap + gap // 2 - label_text.get_height() // 2))

            # Draw row labels (1-8) on the first and last column
            if j == 0 or j == rows - 1:
                label = str(i + 0) if 1 <= i <= 8 else ''
                label_text = BUTTON_FONT.render(label, 1, WHITE)
                win.blit(label_text, (j * gap + gap // 2 - label_text.get_width() // 2, i * gap + gap // 2 - label_text.get_height() // 2))

# Class representing a checkers piece
class Piece:
    def __init__(self, team):
        self.team = team
        self.image = RED if self.team == 'R' else GREEN
        self.type = None

    def draw(self, x, y):
        WIN.blit(self.image, (x, y))

# Function to get the current node based on mouse position
def getNode(grid, rows, width):
    gap = width // rows
    RowX, RowY = pygame.mouse.get_pos()
    Row = RowX // gap
    Col = RowY // gap
    return (Col, Row)

# Function to reset colors of nodes
def resetColours(grid, node):
    positions = generatePotentialMoves(node, grid)
    positions.append(node)

    for colouredNodes in positions:
        nodeX, nodeY = colouredNodes
        grid[nodeX][nodeY].colour = BLACK if abs(nodeX - nodeY) % 2 == 0 else WHITE

# Function to highlight potential moves for a piece
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


# Function to determine the opposite team
def opposite(team):
    return "R" if team == "G" else "G"

# Function to generate potential moves for a given node
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


# Function to check if forced captures are available
def hasForcedCaptures(grid, player):
    for i in range(ROWS):
        for j in range(ROWS):
            if grid[i][j].piece and grid[i][j].piece.team == player:
                moves = generatePotentialMoves((i, j), grid)
                for move in moves:
                    if abs(move[0] - i) == 2:
                        return True
    return False

# Function to recursively check for multiple captures
def checkForMultipleCaptures(grid, position, captured_pieces):
    moves = generatePotentialMoves(position, grid)
    forced_captures = []

    for move in moves:
        if abs(move[0] - position[0]) == 2:
            captured_position = ((move[0] + position[0]) // 2, (move[1] + position[1]) // 2)
            if captured_position not in captured_pieces:
                forced_captures.append(move)
                captured_pieces.add(captured_position)
                # Recursive call to check for more captures
                forced_captures += checkForMultipleCaptures(grid, move, captured_pieces)

    return forced_captures

# Function to check win conditions
def check_win_conditions(grid, currMove):
    # Check if the current player has no pieces left
    if all(grid[i][j].piece is None or grid[i][j].piece.team != currMove for i in range(ROWS) for j in range(ROWS)):
        return True

    # Check if the opposing player has no available moves
    for i in range(ROWS):
        for j in range(ROWS):
            if grid[i][j].piece and grid[i][j].piece.team == opposite(currMove):
                moves = generatePotentialMoves((i, j), grid)
                if moves:
                    return False
    return True


# Function to display the game over screen
def game_over_screen(winner):
    global grid  # Declare grid as a global variable
    WIN.fill(WHITE)

    game_over_text = GAME_OVER_FONT.render(f"Team {winner} wins!", 1, BLACK)
    text_rect = game_over_text.get_rect(center=(WIDTH // 2, 200))
    WIN.blit(game_over_text, text_rect)

    # Exit button
    exit_button = pygame.draw.rect(WIN, EXIT_BUTTON_COLOR, (WIDTH // 2 - 125, 400, 250, 50))
    exit_text = BUTTON_FONT.render("Exit", 1, WHITE)
    text_rect = exit_text.get_rect(center=(WIDTH // 2, 420))
    WIN.blit(exit_text, text_rect)

    # Play Again button 
    play_again_button = pygame.draw.rect(WIN, EXIT_BUTTON_COLOR, (WIDTH // 2 - 125, 475, 250, 50))
    play_again_text = BUTTON_FONT.render("Play Again", 1, WHITE)
    text_rect = play_again_text.get_rect(center=(WIDTH // 2, 495))
    WIN.blit(play_again_text, text_rect)

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
                elif play_again_button.collidepoint(mouse_x, mouse_y):
                    print("play again pressed")
                    return  # Exit the function, breaking out of the infinite loop

                    
# Function to highlight nodes and handle moves
def highlight(ClickedNode, Grid, OldHighlight):
    Column, Row = ClickedNode
    Grid[Column][Row].colour = ORANGE
    if OldHighlight:
        resetColours(Grid, OldHighlight)
    HighlightpotentialMoves(ClickedNode, Grid)
    return (Column, Row)

# Function to handle piece movement
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
    

      
def set_up_custom_board(grid):
    
    # Clear the existing pieces on the grid
    for i in range(ROWS):
        for j in range(ROWS):
            grid[i][j].piece = None

    # Set up a custom board configuration
    
    grid[1][1].piece = Piece('R')
    grid[1][5].piece = Piece('R')
    grid[2][4].piece = Piece('R')
    grid[2][6].piece = Piece('R')
    grid[2][8].piece = Piece('R')
    grid[3][1].piece = Piece('R')
    grid[3][7].piece = Piece('R')
    grid[4][2].piece = Piece('R')
    grid[8][4].piece = Piece('R')
    grid[8][4].piece.type = 'KING'
    grid[8][4].piece.image = REDKING

    grid[4][4].piece = Piece('G')
    grid[6][2].piece = Piece('G')
    grid[6][4].piece = Piece('G')
    grid[6][8].piece = Piece('G')
    grid[7][1].piece = Piece('G')
    grid[7][3].piece = Piece('G')
    grid[7][7].piece = Piece('G')

    # Update the display
    #update_display(WIN, grid, ROWS, WIDTH)


def main(WIDTH, ROWS):
    global game_over
    grid = make_grid(ROWS, WIDTH)
    set_up_custom_board(grid)
    highlightedPiece = None
    currMove = 'G'  # Start with GREEN's turn
    capture_in_progress = False

    # Main game loop
    while not game_over:
        # Check for events
        for event in pygame.event.get():
            # Window is closed
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("First preset")
                    set_up_custom_board(grid)
                    currMove = 'G'
                
                if event.key == pygame.K_1:
                    print("Base case")
                    grid = make_grid(ROWS, WIDTH)
                    currMove = 'G'

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
                            move(grid, highlightedPiece, clickedNode)
                            # Check for multiple captures
                            captured_pieces = {(pieceColumn, pieceRow), (ClickedPositionColumn, ClickedPositionRow)}
                            multiple_captures = checkForMultipleCaptures(grid, clickedNode, captured_pieces)
                            if not multiple_captures or not capture_in_progress:
                                currMove = 'G' if currMove == 'R' else 'R'
                                highlightedPiece = None
                                capture_in_progress = False
                            else:
                                # If there are multiple captures and capture is in progress, keep the same player's turn
                                highlightedPiece = clickedNode
                                capture_in_progress = True if multiple_captures else False
                        # If clicked on an empty blue cell without selecting a piece, ignore the click

                    # Ensure that ClickedPositionColumn and ClickedPositionRow are assigned before this block
                    elif grid[ClickedPositionColumn][ClickedPositionRow].piece:
                        if currMove == grid[ClickedPositionColumn][ClickedPositionRow].piece.team:
                            highlightedPiece = highlight(clickedNode, grid, highlightedPiece)
                            capture_in_progress = hasForcedCaptures(grid, currMove)

        # Check for game over conditions after each player's move
        game_over = check_win_conditions(grid, currMove)

        # If the game is over, display the game over screen
        if game_over:
            game_over = game_over_screen(opposite(currMove))
            if not game_over:  # If "Play Again" is pressed, reset game_over to False
                grid = make_grid(ROWS, WIDTH)
        # Update the display
        update_display(WIN, grid, ROWS, WIDTH)

# Run the game
main(WIDTH, ROWS)
