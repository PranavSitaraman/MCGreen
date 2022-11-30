#Sustainability Quiz Game for MC Green robot
#Designed and written by Manas Harbola (harbolam@mcvts.net) on behalf of Middlesex County Academy

import time
import pygame
import json
from PIL import Image
import random
import sys
import threading
import textwrap
sys.path.append("../")
import error
#from game_interface import Game_Interface

class Button:
    def __init__ (self, surfaceName, ac, ic, rectVals, text, font):
        self.ac = ac #Active color of button
        self.ic = ic #Inactive color of button
        self.rectAttrs = rectVals #(x, y, w, h) of button
        self.surfaceName = surfaceName
        self.text = text
        self.font = font

    def text_objects(self, text, font, color=(0,0,0)):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()


    def generate(self):
        x, y, w, h = self.rectAttrs
        mouse = pygame.mouse.get_pos()

        #Check if mouse is on button
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self.surfaceName, self.ac, self.rectAttrs)

        #Else just show darker button
        else:
            pygame.draw.rect(self.surfaceName, self.ic, self.rectAttrs)

        textSurf, textRect = self.text_objects(self.text, self.font)

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

#UNCOMMENT BOTTOM TWO LINES BEFORE USING BOTTOM TWO LINES
# sys.path.append("../")
# from head_controller import Head_comm
# controller = Head_comm("Sust. Quiz")

class SustainabilityQuiz:
    def __init__(self, ros_controller):
        #Screen size of window
        self.window_size = (1080,1920)

        #Max FPS (frames per second) of game
        self.FPS = 30

        #Define basic colors
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.darker_red = (200, 0, 0)
        self.green = (0, 255, 0)
        self.darker_green = (0, 200, 0)
        self.blue = (50, 89, 250)
        self.darker_blue = (35, 67, 250)
        self.yellow = (255, 255, 0)
        self.darker_yellow = (200, 200, 0)
        #self.ros_controller = ros_controller

        #Load questions JSON file
        with open('questions.json', 'r') as file:
            self.data = json.load(file)

        #Define background
        self.background = pygame.image.load('background.jpg')
        self.background = pygame.transform.scale(self.background, self.window_size)
        self.backgroundRect = self.background.get_rect()

        #Initiate pygame
        pygame.init() #SUPER IMPORTANT

        #Define basic text sizes
        self.largeText = pygame.font.Font('FreeSansBold.ttf', 64)   #Large text, ideal for headings
        self.mediumText = pygame.font.Font('FreeSansBold.ttf', 48)   #Medium text, ideal for subheadings
        self.smallText =  pygame.font.Font('FreeSansBold.ttf', 16)   #Small text, ideal for small buttons

        #Instantiate window/surface
        self.gameDisplay = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption('Sustainability Quiz')
        self.clock = pygame.time.Clock()


    #Class for generating buttons

    #Render text to a surface and a corresponding rectangle
    def text_objects(self, text, font, color=(0,0,0)):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()

    # def moveHeadUpDown():
    #     #Fine tune bottom as needed
    #     upDegree = 45
    #     downDegree = 90 + 45
    #     moveDelay = 0.5
    #     controller.head_update([90,upDegree])
    #     #Delay for moveDelay seconds
    #     time.sleep(moveDelay)
    #     controller.head_update([90, downDegree])
    #
    # def moveHeadLeftRight():
    #     #Fine tune bottom as needed
    #     leftDegree = 45
    #     rightDegree = 90 + 45
    #     moveDelay = 0.5
    #     controller.head_update([leftDegree, 90])
    #     #Delay for moveDelay seconds
    #     time.sleep(moveDelay)
    #     controller.head_update([rightDegree, 90])
    #     time.sleep(moveDelay)
    #     controller.head_update([90, 90])

    #Generate Sustainability Bar for game WORKS
    def generate_bar(self, surfaceName, x, y, num_right, num_wrong, num_questions, color):
        #Fixed width for full size bar
        fixed_width = 1500 / 2
        #Fixed height for full size bar
        fixed_height = 100 / 2

        width_div = fixed_width / num_questions

        #Calculate width of bar
        w = max((width_div * num_right) - (0.5 * width_div * num_wrong), 0)

        #Draw sustainability bar
        pygame.draw.rect(surfaceName, color, (x, y, w, fixed_height))

        #Draw bar outline
        pygame.draw.rect(surfaceName, self.white, (x, y, fixed_width, fixed_height), 3)



    def generate_q_page(self, surfaceName, status, pt_inc, question, choices, correct_ans):
        #Status is a list [score, num_right, num_wrong, num_questions]
        #self.ros_controller.face_update(2)

        #Button dimensions
        button_w = 1.5*(750 / 2); button_h = 1.05*(250 / 2)

        #Reference x, y coordinates for upper left button
        ref_x = (self.window_size[0] - button_w)/2
        ref_y = self.window_size[1] / 4;
        column_spacing = button_h + (0.5 * 200)
        line_spacing = 75

        #Shuffle answers from choices
        random.shuffle(choices)

        buttonText = pygame.font.Font('FreeSansBold.ttf', 32)

        up_up_button = Button(surfaceName, self.darker_red, self.red, (ref_x, ref_y, button_w, button_h), choices[0], buttonText)
        up_bottom_button = Button(surfaceName, self.darker_blue, self.blue, (ref_x, ref_y + column_spacing, button_w, button_h), choices[1], buttonText)
        bottom_up_button = Button(surfaceName, self.darker_yellow, self.yellow, (ref_x, ref_y + (2*column_spacing), button_w, button_h), choices[2], buttonText)
        bottom_right_button = Button(surfaceName, self.darker_green, self.green, (ref_x, ref_y + (3*column_spacing), button_w, button_h), choices[3], buttonText)

        #Need to include rects here for selective updating later

        #Textwrap the Question if needed
        q_text = question.split('||')
        QuestionSurf, QuestionRect = self.text_objects(q_text[0], self.mediumText, self.white)
        QuestionRect.center = ((self.window_size[0] / 2), (self.window_size[1] / 8))
        if '||' in question:
            QuestionPart2Surf, QuestionPart2Rect = self.text_objects(q_text[1], self.mediumText, self.white)
            QuestionPart2Rect.center = ((self.window_size[0] / 2), (self.window_size[1] / 8) + line_spacing)


        #Prepare question text and location

        ScoreSurf, ScoreRect = self.text_objects('Score: ' + str(status[0]) + ' points', self.mediumText, self.white)
        #ScoreRect.center = ((0.20 * window_size[0]), (window_size[1] / 16))
        ScoreRect.topleft = ((0.15 * self.window_size[0]), (self.window_size[1] / 16))


        ElectricSurf, ElectricRect = self.text_objects('Sustainability Bar: ', self.mediumText, self.white)
        ElectricRect.topleft = ((0.15 * self.window_size[0]), (0.70 * self.window_size[1]))

        #Make entire screen 'white' to 'clean' it
        surfaceName.fill(self.white)
        surfaceName.blit(self.background, self.backgroundRect)

        #Write text to buffer
        surfaceName.blit(QuestionSurf, QuestionRect)
        surfaceName.blit(ScoreSurf, ScoreRect)
        surfaceName.blit(ElectricSurf, ElectricRect)
        if '||' in question:
            surfaceName.blit(QuestionPart2Surf, QuestionPart2Rect)

        #Generate Electric bar
        self.generate_bar(surfaceName, 0.15 * self.window_size[0], 0.80 * self.window_size[1], status[1], status[2], status[3], self.yellow)

        up_up_rect = up_up_button.get_rect()
        up_bottom_rect = up_bottom_button.get_rect()
        bottom_up_rect = bottom_up_button.get_rect()
        bottom_right_rect = bottom_right_button.get_rect()

        updateList = [up_up_rect, up_bottom_rect, bottom_up_rect, bottom_right_rect]

        #Update ENTIRE screen just once
        pygame.display.update()

        running = True

        answer_choice = 'not_answered'

        while running:
            #Handle events here:
            for event in pygame.event.get():
                print(event)

                if event.type == pygame.QUIT:
                    # Set Face to Neutral
                    # controller.face_update(getFaceNum())
                    endGame()
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    touch_status = True

                    #Check if buttons are pressed if mouse button is down
                    if up_up_button.is_pressed(touch_status):
                        if up_up_button.text == correct_ans:
                            answer_choice = 'correct'
                        else:
                            answer_choice = 'incorrect'

                    if up_bottom_button.is_pressed(touch_status):
                        if up_bottom_button.text == correct_ans:
                            answer_choice = 'correct'
                        else:
                            answer_choice = 'incorrect'

                    if bottom_up_button.is_pressed(touch_status):
                        if bottom_up_button.text == correct_ans:
                            answer_choice = 'correct'
                        else:
                            answer_choice = 'incorrect'

                    if bottom_right_button.is_pressed(touch_status):
                         if bottom_right_button.text == correct_ans:
                            answer_choice = 'correct'
                         else:
                            answer_choice = 'incorrect'

                    if answer_choice == 'correct':
                       return 'correct'

                    elif answer_choice == 'incorrect':
                       return 'incorrect'
                else:
                    touch_status = False

            up_up_button.generate()
            up_bottom_button.generate()
            bottom_up_button.generate()
            bottom_right_button.generate()

            pygame.display.update(updateList)
            self.clock.tick(self.FPS)

    def generate_correct_page(self, surface, status, point_inc):

        #self.ros_controller.face_update(1)

        next_button = Button(surface, self.darker_blue, self.blue, (0.5 * self.window_size[0] - (0.5 * 375), 0.5 * self.window_size[1], 750 / 2, 250 / 2), 'Next Question', self.mediumText)

        next_button_rect = next_button.get_rect()
        updateList = [next_button_rect]

        HeadingSurf, HeadingRect = self.text_objects('Correct!', self.largeText)
        HeadingRect.center = ((self.window_size[0] / 2), (self.window_size[1] / 4))

        ScoreSurf, ScoreRect = self.text_objects('Score: ' + str(status[0]) + ' (+' + str(point_inc) + ' pts)', self.mediumText)
        ScoreRect.center = ((self.window_size[0] / 2), (0.35 * self.window_size[1]))

        ElectricSurf, ElectricRect = self.text_objects('Sustainability Bar: ', self.mediumText)
        ElectricRect.topleft = ((0.15 * self.window_size[0]), (0.70 * self.window_size[1]))



        surface.fill(self.green)


        surface.blit(HeadingSurf, HeadingRect)
        surface.blit(ScoreSurf, ScoreRect)
        surface.blit(ElectricSurf, ElectricRect)
        self.generate_bar(surface, 0.15 * self.window_size[0], 0.80 * self.window_size[1], status[1], status[2], status[3], self.yellow)

        pygame.display.update()

        running = True

        while running:

            #Handle events here:
            for event in pygame.event.get():
                print(event)

                if event.type == pygame.QUIT:
                    #Change face to neutral
                    # controller.face_update(getFaceNum())
                    endGame()
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    touch_status = True

                    #Check if buttons are pressed if mouse button is down
                    if next_button.is_pressed(touch_status):
                        #Change face to neutral
                        # controller.face_update(getFaceNum())

                        running = False
                else:
                    touch_status = False

            #surface.fill(white)
            next_button.generate()

            pygame.display.update(updateList)
            self.clock.tick(self.FPS)

        #Change face to neutral
        # controller.face_update(getFaceNum())

    def generate_incorrect_page(self, surface, status, point_dec, correct_ans):

        #self.ros_controller.face_update(3)

        next_button = Button(surface, self.darker_blue, self.blue, (0.5 * self.window_size[0] - (0.5 * 375), 0.5 * self.window_size[1], 750 / 2, 250 / 2), 'Next Question', self.mediumText)

        next_button_rect = next_button.get_rect()
        updateList = [next_button_rect]

        line_spacing = 100 / 2

        HeadingSurf, HeadingRect = self.text_objects('Sorry!', self.largeText)
        HeadingRect.center = ((self.window_size[0] / 2), (0.2 * self.window_size[1]))

        Heading2Surf, Heading2Rect = self.text_objects('Correct Answer Was:', self.mediumText)
        Heading2Rect.center = ((self.window_size[0] / 2), (self.window_size[1] / 4) + line_spacing)

        AnswerSurf, AnswerRect = self.text_objects(correct_ans, self.mediumText)
        AnswerRect.center = ((self.window_size[0] / 2), (0.25 * self.window_size[1]) + (2.5 * line_spacing))


        ScoreSurf, ScoreRect = self.text_objects('Score: ' + str(status[0]) + ' (-' + str(point_dec) + ' pts)', self.mediumText)
        ScoreRect.center = ((self.window_size[0] / 2), (0.25 * self.window_size[1]) + (4 * line_spacing))

        ElectricSurf, ElectricRect = self.text_objects('Sustainability Bar: ', self.mediumText)
        ElectricRect.topleft = ((0.15 * self.window_size[0]), (0.70 * self.window_size[1]))

        surface.fill(self.red)

        surface.blit(HeadingSurf, HeadingRect)
        surface.blit(Heading2Surf, Heading2Rect)
        surface.blit(AnswerSurf, AnswerRect)
        surface.blit(ScoreSurf, ScoreRect)
        surface.blit(ElectricSurf, ElectricRect)

        self.generate_bar(surface, 0.15 * self.window_size[0], 0.80 * self.window_size[1], status[1], status[2], status[3], self.yellow)


        pygame.display.update()

        running = True

        while running:

            #Handle events here:
            for event in pygame.event.get():
                print(event)

                if event.type == pygame.QUIT:
                    #Set Face to Neutral
                    # controller.face_update(getFaceNum())
                    endGame()
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    touch_status = True

                    #Check if buttons are pressed if mouse button is down
                    if next_button.is_pressed(touch_status):
                        running = False
                else:
                    touch_status = False

            next_button.generate()

            pygame.display.update(updateList)
            self.clock.tick(self.FPS)

    #Start Menu for Game
    def game_intro(self):
        #self.ros_controller.face_update(1)
        #Button Dimensions
        surface = self.gameDisplay
        button_w = 1.3*(750 / 2); button_h = 1.3*(250 / 2)
        button_y = 1200 / 2
        button_spacing = self.window_size[1]/8 #spacing between buttons in px
        button_x = (self.window_size[0] - button_w)/2

        #Instantiate buttons (Only needs to be done once)
        play_button = Button(surface, self.darker_green, self.green, (button_x, button_y, button_w, button_h), 'Play', self.mediumText)
        help_button = Button(surface, self.darker_blue, self.blue, (button_x, button_y + button_spacing, button_w, button_h), 'Help', self.mediumText)
        quit_button = Button(surface, self.darker_red, self.red, (button_x, button_y + (2*button_spacing), button_w, button_h), 'Quit', self.mediumText)

        #Portion of the screen that must ONLY be updated
        help_button_rect = help_button.get_rect()
        play_button_rect = play_button.get_rect()
        quit_button_rect = quit_button.get_rect()
        updateList = [help_button_rect, play_button_rect, quit_button_rect]

        #Prepare title text and location
        TextSurf, TextRect = self.text_objects('MC Green Sustainability Quiz!', self.largeText, self.white)
        TextRect.center = ((self.window_size[0] / 2), (self.window_size[1] / 8))

        #Make entire screen white to clean it
        surface.fill(self.white)

        surface.blit(self.background, self.backgroundRect)

        #Write text to buffer
        surface.blit(TextSurf, TextRect)

        #Update ENTIRE screen just once
        pygame.display.update()

        touch_status = False #False = no touch, True = touch present

        running = True

        while running:

            #Handle events here:
            for event in pygame.event.get():
                print(event)

                if event.type == pygame.QUIT:
                    #Set Face to Neutral
                    # controller.face_update(getFaceNum())
                    endGame()
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    touch_status = True

                    #Check if buttons are pressed if mouse button is down
                    if quit_button.is_pressed(touch_status):    #If 'Quit' button is tapped
                        endGame()
                        pygame.quit()
                        quit()

                    if play_button.is_pressed(touch_status):    #If 'Play' button is tapped
                        self.select_level(self.gameDisplay)

                    if help_button.is_pressed(touch_status):    #If 'Help' button is tapped
                        self.game_help(self.gameDisplay)
                else:
                    touch_status = False

            help_button.generate()
            play_button.generate()
            quit_button.generate()

            #Update only the portions that need to be updated
            pygame.display.update(updateList)
            self.clock.tick(self.FPS)

    #Help Menu for Game
    def game_help(self, surface):
        #self.ros_controller.face_update(1)
        #Instantiate button for returning back to intro page
        back_button = Button(surface, self.darker_green, self.green, (0.5 * self.window_size[0] - (0.5 * 375), 0.75 * self.window_size[1], 750 / 2, 250 / 2), 'Back', self.mediumText)

        #back_button_rect = pygame.rect.Rect(back_button.rectAttrs[0], back_button.rectAttrs[1], back_button.rectAttrs[2], back_button.rectAttrs[3])
        back_button_rect = back_button.get_rect()
        updateList = [back_button_rect]

        TextSurf, TextRect = self.text_objects('How to Play:', self.largeText, self.white)
        TextRect.center = ((self.window_size[0] / 2), (self.window_size[1] / 8))

        line_spacing = 75   #Spacing between each line of instructions

        Line1Surf, Line1Rect = self.text_objects('1.) Read each question carefully and select the best answer', pygame.font.Font('FreeSansBold.ttf', 35), self.white)
        Line1Rect.center = ((self.window_size[0] / 2), (self.window_size[1] / 4))

        Line2Surf, Line2Rect = self.text_objects('2.) If your answer is correct, you will earn points', pygame.font.Font('FreeSansBold.ttf', 35), self.white)
        Line2Rect.center = ((self.window_size[0] / 2), (self.window_size[1] / 4) + (2 * line_spacing))
        Line2part2Surf, Line2part2Rect = self.text_objects('and charge your sustainability meter', pygame.font.Font('FreeSansBold.ttf', 35), self.white)
        Line2part2Rect.center = ((self.window_size[0] / 2), (self.window_size[1] / 4) + (3 * line_spacing))

        Line3Surf, Line3Rect = self.text_objects('3.) If your answer is incorrect, you will lose points', pygame.font.Font('FreeSansBold.ttf', 35), self.white)
        Line3Rect.center = ((self.window_size[0] / 2), (self.window_size[1] / 4) + (5 * line_spacing))
        Line3part2Surf, Line3part2Rect = self.text_objects(' and your charge meter will go down', pygame.font.Font('FreeSansBold.ttf', 35), self.white)
        Line3part2Rect.center = ((self.window_size[0] / 2), (self.window_size[1] / 4) + (6 * line_spacing))


        #Make entire screen white to clean it
        surface.fill(self.white)

        surface.blit(self.background, self.backgroundRect)


        #Write text to buffer
        surface.blit(TextSurf, TextRect)
        surface.blit(Line1Surf, Line1Rect)
        surface.blit(Line2Surf, Line2Rect)
        surface.blit(Line2part2Surf, Line2part2Rect)
        surface.blit(Line3Surf, Line3Rect)
        surface.blit(Line3part2Surf, Line3part2Rect)

        #Update ENTIRE screen just once
        pygame.display.update()

        running = True

        while running:

            #Handle events here:
            for event in pygame.event.get():
                print(event)

                if event.type == pygame.QUIT:
                    #Set Face to Neutral
                    # controller.face_update(getFaceNum())
                    endGame()
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    touch_status = True

                    #Check if buttons are pressed if mouse button is down
                    if back_button.is_pressed(touch_status):
                        self.game_intro()
                else:
                    touch_status = False

            back_button.generate()

            pygame.display.update(updateList)
            self.clock.tick(self.FPS)


    def select_level(self, surface):
        #self.ros_controller.face_update(1)
        #Instantiate button for returning back to intro page
        button_w, button_h = 375, 125
        button_x = (self.window_size[0] - button_w)/2
        button_y = self.window_size[1]/4
        button_spacing = self.window_size[1]/8


        easy_button = Button(surface, self.darker_green, self.green, (button_x, button_y, button_w, button_h), 'Easy', self.mediumText)
        medium_button = Button(surface, self.darker_yellow, self.yellow, (button_x, button_y + button_spacing, button_w, button_h), 'Medium', self.mediumText)
        hard_button = Button(surface, self.darker_red, self.red, (button_x, button_y + (2*button_spacing), button_w, button_h), 'Hard', self.mediumText)
        back_button = Button(surface, self.darker_green, self.green, (button_x, button_y + (4*button_spacing), button_w, button_h), 'Back', self.mediumText)


        back_button_rect = back_button.get_rect()
        easy_button_rect = easy_button.get_rect()
        medium_button_rect = medium_button.get_rect()
        hard_button_rect = hard_button.get_rect()

        updateList = [back_button_rect, easy_button_rect, medium_button_rect, hard_button_rect]

        TextSurf, TextRect = self.text_objects('Select your level:', self.largeText, self.white)
        TextRect.center = ((self.window_size[0] / 2), (self.window_size[1] / 8))

        line_spacing = 75   #Spacing between each line of instructions

        #Make entire screen white to clean it
        surface.fill(self.white)

        surface.blit(self.background, self.backgroundRect)

        #Write text to buffer
        surface.blit(TextSurf, TextRect)

        #Update ENTIRE screen just once
        pygame.display.update()

        running = True

        while running:

            #Handle events here:
            for event in pygame.event.get():
                print(event)

                if event.type == pygame.QUIT:
                    #Set Face to Neutral
                    # controller.face_update(getFaceNum())
                    endGame()
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    touch_status = True

                    #Check if buttons are pressed if mouse button is down
                    if back_button.is_pressed(touch_status):
                        self.game_intro()
                    if easy_button.is_pressed(touch_status):
                        point_vals = self.data["point_vals"]["level_easy"]
                        q_set = [q for q in self.data["level_easy"]]
                        self.game_menu(self.gameDisplay, point_vals, q_set)
                    if medium_button.is_pressed(touch_status):
                        point_vals = self.data["point_vals"]["level_medium"]
                        q_set = [q for q in self.data["level_medium"]]
                        self.game_menu(self.gameDisplay, point_vals, q_set)
                    if hard_button.is_pressed(touch_status):
                        point_vals = self.data["point_vals"]["level_hard"]
                        q_set = [q for q in self.data["level_hard"]]
                        self.game_menu(self.gameDisplay, point_vals, q_set)

                else:
                    touch_status = False

            back_button.generate()
            easy_button.generate()
            medium_button.generate()
            hard_button.generate()

            pygame.display.update(updateList)
            self.clock.tick(self.FPS)


    def game_menu(self, surface, point_vals, q_set):
        #Status is a list [score, num_right, num_wrong, num_questions]
        status = [0, 0, 0, len(q_set)]

        #Randomize order of questions
        random.shuffle(q_set)

        for q in q_set:
            correct_ans = q["answer"]
            pt_inc = point_vals[0]
            pt_dec = point_vals[1]
            question = q["question"]
            correct_ans = q["answer"]
            choices = q["choices"]
            outcome = self.generate_q_page(surface, status, pt_inc, question, choices, correct_ans)

            if outcome == 'correct':
                status[0] += pt_inc
                status[1] += 1
                self.generate_correct_page(surface, status, pt_inc)

            elif outcome == 'incorrect':
                if (status[0] != 0):
                    status[0] -= pt_dec

                status[2] += 1
                self.generate_incorrect_page(surface, status, pt_dec, correct_ans)

        self.game_over(surface, status)


    def game_over(self, surface, status):
        #self.ros_controller.face_update(5)
        #Set Face to Happy, regardless of score
        # controller.face_update(getFaceNum(1))

        #Button Dimensions
        button_w = 750 / 2; button_h = 250 / 2

        menu_button = Button(surface, self.darker_blue, self.blue, (self.window_size[0] / 2 - (0.5 * 375), 0.75 * self.window_size[1], button_w, button_h), 'Menu', self.mediumText)

        menu_button_rect = menu_button.get_rect()

        updateList = [menu_button_rect]


        #Prepare title text and location
        TextSurf, TextRect = self.text_objects('Game Over!', self.largeText)
        TextRect.center = ((self.window_size[0] / 2), (self.window_size[1] / 4))

        FinalSurf, FinalRect = self.text_objects('Final Score: ' + str(status[0]) + ' pts', self.mediumText)
        FinalRect.center = ((self.window_size[0] / 2), (0.4 * self.window_size[1]))

        ElectricSurf, ElectricRect = self.text_objects('Sustainability Bar: ', self.mediumText)
        ElectricRect.topleft = ((0.15 * self.window_size[0]), (0.55 * self.window_size[1]))

        #Make entire screen white to clean it
        surface.fill(self.green)

        #Write text to buffer
        surface.blit(TextSurf, TextRect)
        surface.blit(FinalSurf, FinalRect)
        surface.blit(ElectricSurf, ElectricRect)
        self.generate_bar(surface, 0.15 * self.window_size[0], 0.65 * self.window_size[1], status[1], status[2], status[3], self.blue)

        #Update ENTIRE screen just once
        pygame.display.update()

        touch_status = False

        #makeFace()

        running = True

        while running:

            #Handle events here:
            for event in pygame.event.get():
                print(event)

                if event.type == pygame.QUIT:
                    #Set Face to Neutral
                    # controller.face_update(getFaceNum())
                    #
                    endGame()
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    touch_status = True

                    #Check if buttons are pressed if mouse button is down
                    if menu_button.is_pressed(touch_status):    #If 'Quit' button is tapped
                        #Set Face to Neutral
                        # controller.face_update(getFaceNum())

                        #Old code to quit instead of return to menu
                        #pygame.quit()
                        #quit()
                        pygame.display.update(updateList)
                        self.clock.tick(self.FPS)
                        self.game_intro()

                else:
                    touch_status = False

            menu_button.generate()

            #Update only the portions that need to be updated
            pygame.display.update(updateList)
            self.clock.tick(self.FPS)




# #Execute game
# game_intro(gameDisplay)
#
# # #Set Face to Neutral
# # controller.face_update(getFaceNum())
# # #Orient Head to proper position
# # controller.head_update([90, 90])
# pygame.quit()
# quit()

if __name__ == '__main__':
    quiz = SustainabilityQuiz()
    quiz.game_intro()
    pygame.quit()
    quit()
