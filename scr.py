import pygame

background_color = (255,255,255)
screen_size = (300, 300)
screen = pygame.display.set_mode(screen_size)

def rect(pos: tuple, size: tuple, color: tuple):
    pygame.draw.rect(screen, color, (size, pos))