import pygame 
import sys

pygame.init()

res = (720,720)

screen = pygame.display.set_mode(res)

color = (255,255,255)

color_light = (110,0,0)

color_dark = (0,0,100)

width = screen.get_width()

height = screen.get_height()

smallfont = pygame.font.SysFont('Corbel',35)  
   
bigfont = pygame.font.SysFont('Corbel',50)

text1 = bigfont.render('Welcome To The Game', True , color)

text = smallfont.render('quit' , True , color)  
  
while True:  
      
    for ev in pygame.event.get():  
          
        if ev.type == pygame.QUIT:  
            pygame.quit()  
              
          
        if ev.type == pygame.MOUSEBUTTONDOWN:  
              
              
              
            if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40:  
                pygame.quit()  
                  
      
    screen.fill((0,150,50))  
      
      
    mouse = pygame.mouse.get_pos()  
      
      
    if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40:  
        pygame.draw.rect(screen,color_light,[width/2,height/2,140,40])  
          
    else:  
        pygame.draw.rect(screen,color_dark,[width/2,height/2,140,40])  
      
    screen.blit(text1 ,(width/4,height/7))
    screen.blit(text , (width/4,height/2,140,40))  
      
     
    pygame.display.update()  