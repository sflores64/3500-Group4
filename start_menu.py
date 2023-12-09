##########################################################################
# CMPS 3500 - Class Project
# Updated: 12/7/2023
# File: main_menu.py
# Name 1: Edwin Aviles
# Name 2: Sandra Mateiro 
# Name 3: Ricardo Rivas Navarro
# Name 4: Jason Rodriguez
# Description: Provides a main menu to access default games and test cases
##########################################################################

import pygame
import sys
import subprocess

# Initialize Pygame
pygame.init()

# Set up window
width, height = 800, 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game Menu")
# Adding custom background
background = pygame.image.load("back.jpeg")
# Colors
red = (128, 0, 0)
yellow = (255, 215, 100)
green = (0, 200, 150)
purple = (255,0,255)
black = (0, 0, 0)
white = (255, 255, 255)
# Fonts
font_title = pygame.font.Font(None, 64)
font_button = pygame.font.Font(None, 36)

# Text
title_text = font_title.render("GAME MENU", True, white)
play_checkers_text = font_button.render("Play Checkers", True, black)
test_checkers_text = font_button.render("Test Checkers", True, black)
play_chess_text = font_button.render("Play Chess", True, black)
test_chess_text = font_button.render("Test Chess", True, black)
exit_text = font_button.render("Exit Game", True, white)


# Rectangles for buttons
play_checkers_rect = pygame.Rect(300, 200, 200, 50)
test_checkers_rect = pygame.Rect(300, 300, 200, 50)
play_chess_rect = pygame.Rect(300, 400, 200, 50)
test_chess_rect = pygame.Rect(300, 500, 200, 50)
exit_rect = pygame.Rect(300, 600, 200, 50)


def execute(file):
    try:
        subprocess.run(['python3', file], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


# Game loop
while True:
    # Clear the screen
    win.blit(background, (0, 0))

    # Draw title
    win.blit(title_text, (width // 2 - title_text.get_width() // 2, 50))

    # Draw buttons
    pygame.draw.rect(win, yellow, play_checkers_rect)
    pygame.draw.rect(win, yellow, test_checkers_rect)
    pygame.draw.rect(win, yellow, play_chess_rect)
    pygame.draw.rect(win, yellow, test_chess_rect)
    pygame.draw.rect(win, red, exit_rect)
  
    


    win.blit(play_checkers_text, (play_checkers_rect.centerx - play_checkers_text.get_width() // 2, play_checkers_rect.centery - play_checkers_text.get_height() // 2))
    win.blit(test_checkers_text, (test_checkers_rect.centerx - test_checkers_text.get_width() // 2, test_checkers_rect.centery - test_checkers_text.get_height() // 2))
    win.blit(play_chess_text, (play_chess_rect.centerx - play_chess_text.get_width() // 2, play_chess_rect.centery - play_chess_text.get_height() // 2))
    win.blit(test_chess_text, (test_chess_rect.centerx - test_chess_text.get_width() // 2, test_chess_rect.centery - test_chess_text.get_height() // 2))
    win.blit(exit_text, (exit_rect.centerx - exit_text.get_width() // 2, exit_rect.centery - exit_text.get_height() // 2))
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_checkers_rect.collidepoint(event.pos):
                print("Play Checkers clicked")
                execute("checkers.py")
            elif play_chess_rect.collidepoint(event.pos):
                print("Play Chess clicked")
                execute("chess.py")
            elif test_checkers_rect.collidepoint(event.pos):
                print("Test Checkers clicked")
                execute("checkers_test.py")
            elif test_chess_rect.collidepoint(event.pos):
                print("Test Chess clicked")
                execute("chess_test.py")
            elif exit_rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()

    pygame.display.flip()
    pygame.display.update()
    