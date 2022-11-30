#!/usr/bin/python3
import rospy
from std_msgs.msg import Int16, Bool
import time
import sys
import non_use.py
import pygame
from pygame import mixer
import random
import math
import threading
import os


from recycle_it.Recycle import Recycle_IT
from electricity_quiz.ElectricityQuiz import ElectricityQuiz
from sustainability_quiz.SustainabilityQuiz import SustainabilityQuiz
from whats_wrong.Game_File import WhatsWrong
from water_calculator.water_calculator import WaterCalc
from display_class.py import Display_Controller
from game_interface import Game_Interface

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


if __name__=="__main__":
    try:
        rospy.init_node("Display_Controller")
        controller = Display_Controller()

        homedir = os.getcwd()
        self.ros_controller = Game_Interface()
        self.ros_controller.game_update("None")
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

        while True:

            if controller.current_mode != 3:
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
                pygame.display.update()


            else:
                screen.fill((255, 255, 255))
                electricityButton.generate()
                sustainabilityButton.generate()
                whatswrongButton.generate()
                RecycleItButton.generate()
                WaterButton.generate()
                screen.blit(middlesex, ((window[0] - 512)/2, 50))
                screen.blit(textSurf, textRect)
                pygame.display.update()

                for event in pygame.event.get():
                    print(event)

                    if event.type == pygame.QUIT:
                        # Set Face to Neutral
                        # controller.face_update(getFaceNum())

                        pygame.quit()
                        quit()

                    if event.type == pygame.MOUSEBUTTONUP:
                        touch_status = True

                        #Check if buttons are pressed if mouse button is down
                        if electricityButton.is_pressed(touch_status):
                            try:
                                self.ros_controller.game_update("Electricity Quiz")
                                os.chdir('./electricity_quiz')
                                game = ElectricityQuiz(ros_controller)
                                game.game_intro()

                            except:
                                os.chdir('..')
                                screen.fill(white)
                                self.ros_controller.game_update("None")

                        elif sustainabilityButton.is_pressed(touch_status):
                            try:
                                self.ros_controller.game_update("Sustainability Quiz")
                                os.chdir('./sustainability_quiz')
                                game = SustainabilityQuiz(ros_controller)
                                game.game_intro()
                            except:
                                os.chdir('..')
                                screen.fill(white)
                                self.ros_controller.game_update("None")

                        elif whatswrongButton.is_pressed(touch_status):
                            try:
                                self.ros_controller.game_update("What's Wrong With The Room")
                                os.chdir('./whats_wrong')
                                game = WhatsWrong(ros_controller)
                                game.intro()
                            except:
                                os.chdir('..')
                                screen.fill(white)
                                self.ros_controller.game_update("None")
                        elif RecycleItButton.is_pressed(touch_status):
                            try:
                                self.ros_controller.game_update("Recycle It")
                                os.chdir('./recycle_it')
                                game = Recycle_IT(ros_controller)
                                game.intro()

                            except:
                                os.chdir('..')
                                screen.fill(white)
                                self.ros_controller.game_update("None")


                        elif WaterButton.is_pressed(touch_status):
                            try:
                                self.ros_controller.game_update("Water Calculator")
                                os.chdir('./water_calculator')
                                game = WaterCalc(ros_controller)
                                game.game_intro()

                            except:
                                os.chdir('..')
                                screen.fill(white)
                                self.ros_controller.game_update("None")




                    electricityButton.generate()
                    sustainabilityButton.generate()
                    whatswrongButton.generate()
                    RecycleItButton.generate()
                    WaterButton.generate()
                    screen.blit(middlesex, ((window[0] - 512)/2, 50))
                    screen.blit(textSurf, textRect)
                    pygame.display.update()

    except KeyboardInterrupt:
        pass
    except rospy.ROSInterruptException:
        pass
