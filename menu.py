# Find/Use Mouse Position in Pygame
import pygame
import subprocess

pygame.init()

WIDTH = 500
HEIGHT = 500
fps = 60
timer = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Menu')
main_menu = False
font = pygame.font.Font('freesansbold.ttf', 24)
menu_command = 0


class Button:
    def __init__(self, txt, pos):
        self.text = txt
        self.pos = pos
        self.button = pygame.rect.Rect((self.pos[0], self.pos[1]), (260, 40))

    def draw(self):
        pygame.draw.rect(screen, 'light gray', self.button, 0, 4)
        pygame.draw.rect(screen, 'dark gray', [self.pos[0], self.pos[1], 260, 40], 5, 5)
        text2 = font.render(self.text, True, 'black')
        screen.blit(text2, (self.pos[0] + 15, self.pos[1] + 7))

    def check_clicked(self):
        if self.button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return True
        else:
            return False


def draw_menu():
    command = -1
    pygame.draw.rect(screen, 'black', [100, 100, 300, 380])
    pygame.draw.rect(screen, 'green', [100, 100, 300, 380], 5)
    pygame.draw.rect(screen, 'white', [120, 120, 260, 40], 0, 5)
    pygame.draw.rect(screen, 'gray', [120, 120, 260, 40], 5, 5)
    txt = font.render('Select Option', True, 'black')
    
    menu = Button('Select Option', (120, 120))
    menu.draw()
    button1 = Button('Play Checkers', (120, 180))
    button1.draw()
    button2 = Button('Play Chess', (120, 240))
    button2.draw()
    button3 = Button('Test Checkers', (120, 300))
    button3.draw()
    button4 = Button('Test Chess', (120, 360))
    button4.draw()
    button5 = Button('Exit Menu' , (120, 420))
    button5.draw()

    if menu.check_clicked():
        command = 0
    if button1.check_clicked():
        command = 1
    if button2.check_clicked():
        command = 2
    if button3.check_clicked():
        command = 3
    return command


def draw_game():
    menu_btn = Button('Main Menu', (230, 450))
    menu_btn.draw()
    menu = menu_btn.check_clicked()
    return menu


def execute(file):
    try:
         subprocess.run(['python3', file], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    


run = True
while run:
    screen.fill('dark green')
    timer.tick(fps)
    if main_menu:
        menu_command = draw_menu()
        if menu_command != -1:
            main_menu = False
    else:
        main_menu = draw_game()
        if menu_command > 0:
            if menu_command == 1:
                execute("checkers.py")
                pygame.QUIT
                run = False
            if menu_command == 2:
                execute("chess.py")
                pygame.QUIT
                run = False


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()
pygame.quit()