import pygame
import sys

pygame.init()

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 900

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Quoridor")

clock = pygame.time.Clock()
FPS = 60

running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))

    pygame.display.flip()

pygame.quit()
sys.exit()