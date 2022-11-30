import pygame
from pygame import mixer
import random
import time
import math
import sys
import threading
import os

def non_use():
    pygame.init()
    window = (1080, 1920)
    screen = pygame.display.set_mode(window)

    screen.fill((255,255,255))
    middlesex = pygame.image.load('Middlesex.png')
    middlesex = pygame.transform.scale(middlesex, (800, 164))
    screen.blit(middlesex, ((window[0] - 800)/2, 50))
    recycle = pygame.image.load('recycle_logo.png')
    mca = pygame.image.load("mca.png")
    recycle = pygame.transform.scale(recycle, (800, 800))
    screen.blit(recycle, ((window[0] - 800)/2, (window[1] - 800)/2))
    mca = pygame.transform.scale(mca, (600, 400))
    screen.blit(mca, ((window[0] - 600)/2, 1500))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Set Face to Neutral
                # controller.face_update(getFaceNum())

                pygame.quit()
                quit()
        pygame.display.update()
if __name__ == '__main__':
    non_use()
