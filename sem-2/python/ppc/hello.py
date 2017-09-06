import pygame
import pygame.key
import pygame.event
import pygame.constants
import pygame.font
import pygame.time
import time
import random

pygame.init()
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
display_width = 800
display_height = 600
gamedisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('SnakeGame')


block_size = 10
clock = pygame.time.Clock()
fps = 20
fonts  = pygame.font.SysFont(None , 25)

def message_to_screen(msg , col):
    text = fonts.render(msg , True , col)
    gamedisplay.blit(text ,[display_width/2,display_height/2])
def gameloop():
    gamexit = False
    gameover = False
    lead_x = display_width / 2
    lead_y = display_height / 2
    lead_x_change = 0
    lead_y_change = 0
    randoms_x = random.randrange(0,display_width-block_size)
    randoms_y = random.randrange(0,display_height - block_size)


    while not gamexit:
        while gameover == True:
            gamedisplay.fill(white)
            message_to_screen('Game over press c to continue or q to quit',red)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameover = False
                        gamexit = True
                    if event.key == pygame.K_c:
                        gameloop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gamexit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    lead_x_change = -block_size
                    lead_y_change = 0
                if event.key == pygame.K_RIGHT:
                    lead_x_change = block_size
                    lead_y_change = 0
                if event.key == pygame.K_UP:
                    lead_y_change = -block_size
                    lead_x_change = 0
                if event.key == pygame.K_DOWN:
                    lead_y_change = block_size
                    lead_x_change = 0
        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
            gameover = True

        lead_x += lead_x_change
        lead_y += lead_y_change
        gamedisplay.fill(white)
        pygame.draw.rect(gamedisplay , red , [randoms_x , randoms_y , block_size , block_size])
        pygame.draw.rect(gamedisplay, black, [lead_x,lead_y, block_size, block_size])

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()
gameloop()
