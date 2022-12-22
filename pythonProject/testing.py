import pygame
import sys
import random

s1 = pygame.sprite.Group()

class Example(pygame.sprite.Sprite):
    im = pygame.image.load('ex.jfif')

    def __init__(self, group):
        super().__init__(group)
        self.image = self.im
        self.rect = self.im.get_rect()
        self.rect.x = 0
        self.rect.y = 0


size = width, height = 500, 500
screen = pygame.display.set_mode(size)
ex = Example(s1)
pygame.display.set_caption('Humster on the beach')
clock = pygame.time.Clock()
running = True

screen.fill(pygame.Color('Black'))
while running:
    screen.fill(pygame.Color('Black'))
    s1.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
    clock.tick(100)
pygame.quit()
