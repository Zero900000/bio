import pygame
import var
import scr

while var.game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            var.game = False
    pygame.display.update()
    scr.screen.fill(scr.background_color)