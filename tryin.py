import pygame
import random
pygame.init()

white = (255, 255, 255)
black = (0, 155, 0)
red = (255, 0, 0)
font = pygame.font.SysFont(None, 15)
display_size = round(310/10.0)*10.0
display_size_2 = round(230/10.0)*10.0
display_size = int(display_size)
display_size_2 = int(display_size_2)
gameDisplay = pygame.display.set_mode((310, 230), pygame.NOFRAME)
pygame.display.set_caption("Slither")
clock = pygame.time.Clock()

pygame.mouse.set_visible(False)
joysticks = []
clock = pygame.time.Clock()
gameDisplay.fill(red)
for i in range(0, pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
    joysticks[-1].init()
    print("Detected Joystick", joysticks[-1].get_name(), "'")

pygame.display.toggle_fullscreen()


def snake(block_size, snakelist):
    for XnY in snakelist:
        pygame.draw.rect(gameDisplay, black, [XnY[0], XnY[1], block_size, block_size])


def message_to_screen(msg, color):
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, [20, 105])


def game_loop():
    snakelist = []
    snakelength = 1
    lead_x = round(155/10.0)*10.0
    lead_y = round(115/10.0)*10.0
    lead_x_change = 0
    lead_y_change = 0
    block_size = 10
    gameover = False
    gameexit = False
    gameStart = False
    randAppleX = round(random.randrange(0, 310-block_size)/10.0)*10.0
    randAppleY = round(random.randrange(0, 230-block_size)/10.0)*10.0
    while not gameStart:
        gameDisplay.fill(white)
        screen_text = font.render("SLITHER", True, red)
        screen_text_2 = font.render("Press START", True, black)
        gameDisplay.blit(screen_text_2, [120, 120])
        gameDisplay.blit(screen_text, [130, 90])
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 9:
                    gameStart = True
    while not gameexit:

        while gameover:
            gameDisplay.fill(white)
            message_to_screen("Game Over, Press SELECT to restart and START to quit", red)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 9:
                        gameexit = True
                        gameover = False
                    elif event.button == 8:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 1:
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.button == 3:
                    lead_x_change = - block_size
                    lead_y_change = 0
                elif event.button == 0:
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.button == 2:
                    lead_y_change = block_size
                    lead_x_change = 0
                elif event.button == 9:
                    gameexit = True
        if lead_x >= 302 or lead_x < 0 or lead_y >= 222 or lead_y < 0:
            gameover = True

        lead_x += lead_x_change
        lead_y += lead_y_change
        gameDisplay.fill(white)
        pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, block_size, block_size])

        snakehead = []

        snakehead.append(lead_x)
        snakehead.append(lead_y)
        snakelist.append(snakehead)
        if len(snakelist) > snakelength:
            del snakelist[0]
        for eackSegment in snakelist[:-1]:
            if eackSegment == snakehead:
                gameover = True
        snake(block_size, snakelist)
        pygame.display.update()
        if lead_x == randAppleX and lead_y == randAppleY:
            randAppleX = round(random.randrange(0, 310 - block_size) / 10.0) * 10.0
            randAppleY = round(random.randrange(0, 230 - block_size) / 10.0) * 10.0
            snakelength += 1
        clock.tick(12)

    pygame.quit()
    quit()
game_loop()



