import pygame

background_color = (255,255,255)
screen_size = (300, 300)
screen = pygame.display.set_mode(screen_size)

def rect(pos: tuple, size: tuple, color: tuple):
    pygame.draw.rect(screen, color, (pos, size))
def circle(pos: tuple, size: float, color: tuple):
    pygame.draw.circle(screen, color, pos, size)