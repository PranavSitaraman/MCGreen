import pygame
from pygame import mixer
import random
import time
import math
import sys
import threading
import os
from pygame import mixer

from recycle_it.Recycle import Recycle_IT
from electricity_quiz.ElectricityQuiz import ElectricityQuiz
from sustainability_quiz.SustainabilityQuiz import SustainabilityQuiz
from whats_wrong.Game_File import WhatsWrong
from water_calculator.water_calculator import WaterCalc

class Button:
    def __init__ (self, surfaceName, ac, ic, rectVals, text, font):
        self.ac = ac #Active color of button
        self.ic = ic #Inactive color of button
        self.rectAttrs = rectVals #(x, y, w, h) of button
        self.surfaceName = surfaceName
        self.text = text
        self.font = font

    def generate(self):
        x, y, w, h = self.rectAttrs
        mouse = pygame.mouse.get_pos()

        #Check if mouse is on button
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self.surfaceName, self.ac, self.rectAttrs)

        #Else just show darker button
        else:
            pygame.draw.rect(self.surfaceName, self.ic, self.rectAttrs)

        textSurf, textRect = text_objects(self.text, self.font)

        textRect.center = (x + (w / 2), y + (h / 2))
        self.surfaceName.blit(textSurf, textRect)
        pygame.display.update(self.get_rect())

    def get_rect(self):
        x, y, w, h = self.rectAttrs
        return pygame.rect.Rect(x, y, w, h)

    def is_pressed(self, touch_status):
        x, y, w, h = self.rectAttrs
        mouse = pygame.mouse.get_pos()

        #Check if mouse is hovering over button or not
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            if touch_status == True:
                #print('CLICK DETECTED')
                return True

            elif touch_status == False:
                return False

        #If mouse is not hovering over button, button must obviously not be pressed
        else:
            return False

def text_objects(text, font, color=(0,0,0)):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()
#from recycle_it.Recycle.py import RecycleIT
def run_menu():

    homedir = os.getcwd()
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    darker_red = (200, 0, 0)
    green = (0, 255, 0)
    darker_green = (0, 200, 0)
    blue = (50, 89, 250)
    darker_blue = (35, 67, 250)
    yellow = (255, 255, 0)
    darker_yellow = (200, 200, 0)
    cyan = (0, 255, 255)
    darker_cyan = (0, 200, 200)
    pygame.display.set_caption("Games Menu")
    pygame.init()

    window = (1080, 1920)
    screen = pygame.display.set_mode(window)






    buttonText = pygame.font.Font('FreeSansBold.ttf', 32)
    font = pygame.font.Font('FreeSansBold.ttf', 50)
    electricityButton = Button(screen, darker_yellow, yellow, (1/4*window[0], 1/6*window[1], 1/2*window[0], 2/16*window[1]), "Electricity Quiz", buttonText)
    sustainabilityButton =  Button(screen, darker_green, green, (1/4*window[0], 2/6*window[1], 1/2*window[0], 2/16*window[1]), "Sustainability Quiz", buttonText)
    whatswrongButton =  Button(screen, darker_red, red, (1/4*window[0], 3/6*window[1], 1/2*window[0], 2/16*window[1]), "Whats Wrong Game", buttonText)
    RecycleItButton =  Button(screen, darker_blue, blue, (1/4*window[0], 4/6*window[1], 1/2*window[0], 2/16*window[1]), "Recycle It Game", buttonText)
    WaterButton =  Button(screen,  darker_cyan, cyan, (1/4*window[0], 5/6*window[1], 1/2*window[0], 2/16*window[1]), "Water Calculator", buttonText)
    screen.fill((255, 255, 255))
    middlesex = pygame.image.load('Middlesex.png')
    screen.blit(middlesex, ((window[0] - 512)/2, 50))
    textSurf, textRect = text_objects('Games Menu', font)
    textRect.center = ((window[0] / 2), 200)

    screen.blit(textSurf, textRect)
    ros_controller = 1
    while True:
        mixer.music.stop()
        for event in pygame.event.get():
            print(event)

            if event.type == pygame.QUIT:
                # Set Face to Neutral
                # controller.face_update(getFaceNum())

                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                touch_status = True

                #Check if buttons are pressed if mouse button is down
                if electricityButton.is_pressed(touch_status):
                    try:
                        os.chdir('./electricity_quiz')
                        game = ElectricityQuiz(ros_controller)
                        game.game_intro()
                    except:

                        os.chdir('..')
                        screen.fill(white)

                elif sustainabilityButton.is_pressed(touch_status):
                    try:
                        os.chdir('./sustainability_quiz')
                        game = SustainabilityQuiz(ros_controller)
                        game.game_intro()
                    except:
                        os.chdir('..')
                        screen.fill(white)

                elif whatswrongButton.is_pressed(touch_status):
                    try:
                        os.chdir('./whats_wrong')
                        game = WhatsWrong(ros_controller)
                        game.intro()
                    except:
                        os.chdir('..')
                        screen.fill(white)
                elif RecycleItButton.is_pressed(touch_status):
                    try:
                        os.chdir('./recycle_it')
                        game = Recycle_IT(ros_controller)
                        game.intro()

                    except:
                        os.chdir('..')
                        screen.fill(white)


                elif WaterButton.is_pressed(touch_status):
                    try:
                        os.chdir('./water_calculator')
                        game = WaterCalc(ros_controller)
                        game.game_intro()

                    except:
                        os.chdir('..')
                        screen.fill(white)



            electricityButton.generate()
            sustainabilityButton.generate()
            whatswrongButton.generate()
            RecycleItButton.generate()
            WaterButton.generate()
            screen.blit(middlesex, ((window[0] - 512)/2, 50))
            screen.blit(textSurf, textRect)
            pygame.display.update()
if __name__ == '__main__':
    run_menu()
