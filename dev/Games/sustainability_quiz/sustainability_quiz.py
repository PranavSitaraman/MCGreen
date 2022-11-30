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

#UNCOMMENT BOTTOM TWO LINES BEFORE USING BOTTOM TWO LINES
# sys.path.append("../")
# from head_controller import Head_comm
# controller = Head_comm("Sust. Quiz")

#Screen size of window
window_size = (1080,1920)

#Max FPS (frames per second) of game
FPS = 30

#Define basic colors
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

#Load questions JSON file
with open('questions.json', 'r') as file:
    data = json.load(file)

#Define background
background = pygame.image.load('background.jpg')
background = pygame.transform.scale(background, window_size)
backgroundRect = background.get_rect()

#Class for generating buttons
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

#Render text to a surface and a corresponding rectangle
def text_objects(text, font, color=(0,0,0)):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def getFaceNum(statusNum=2):
    #statusNum = 1 -> happy, 2 -> neutral, 3-> sad
    #1-3 -> Happy, 4 -> Neutral, 5-7 -> Sad
    #Choose happy face
    if statusNum == 1:
        return random.randint(1,3)
    #Choose sad face
    elif statusNum == 3:
        return random.randint(5,7)
    #Choose neutral face
    else:
        return 2

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
def generate_bar(surfaceName, x, y, num_right, num_wrong, num_questions, color):
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
    pygame.draw.rect(surfaceName, white, (x, y, fixed_width, fixed_height), 3)


def generate_q_page(surfaceName, status, pt_inc, question, choices, correct_ans):
    #Status is a list [score, num_right, num_wrong, num_questions]

    #Button dimensions
    button_w = 1.5*(750 / 2); button_h = 1.05*(250 / 2)

    #Reference x, y coordinates for upper left button
    ref_x = (window_size[0] - button_w)/2
    ref_y = window_size[1] / 4;
    column_spacing = button_h + (0.5 * 200)
    line_spacing = 75

    #Shuffle answers from choices
    random.shuffle(choices)

    buttonText = pygame.font.Font('FreeSansBold.ttf', 32)

    up_up_button = Button(surfaceName, darker_red, red, (ref_x, ref_y, button_w, button_h), choices[0], buttonText)
    up_bottom_button = Button(surfaceName, darker_blue, blue, (ref_x, ref_y + column_spacing, button_w, button_h), choices[1], buttonText)
    bottom_up_button = Button(surfaceName, darker_yellow, yellow, (ref_x, ref_y + (2*column_spacing), button_w, button_h), choices[2], buttonText)
    bottom_right_button = Button(surfaceName, darker_green, green, (ref_x, ref_y + (3*column_spacing), button_w, button_h), choices[3], buttonText)

    #Need to include rects here for selective updating later

    #Textwrap the Question if needed
    q_text = question.split('||')
    QuestionSurf, QuestionRect = text_objects(q_text[0], mediumText, white)
    QuestionRect.center = ((window_size[0] / 2), (window_size[1] / 8))
    if '||' in question:
        QuestionPart2Surf, QuestionPart2Rect = text_objects(q_text[1], mediumText, white)
        QuestionPart2Rect.center = ((window_size[0] / 2), (window_size[1] / 8) + line_spacing)



    #Prepare question text and location

    ScoreSurf, ScoreRect = text_objects('Score: ' + str(status[0]) + ' points', mediumText, white)
    #ScoreRect.center = ((0.20 * window_size[0]), (window_size[1] / 16))
    ScoreRect.topleft = ((0.15 * window_size[0]), (window_size[1] / 16))


    ElectricSurf, ElectricRect = text_objects('Sustainability Bar: ', mediumText, white)
    ElectricRect.topleft = ((0.15 * window_size[0]), (0.70 * window_size[1]))

    #Make entire screen 'white' to 'clean' it
    surfaceName.fill(white)
    surfaceName.blit(background, backgroundRect)

    #Write text to buffer
    surfaceName.blit(QuestionSurf, QuestionRect)
    surfaceName.blit(ScoreSurf, ScoreRect)
    surfaceName.blit(ElectricSurf, ElectricRect)
    if '||' in question:
        surfaceName.blit(QuestionPart2Surf, QuestionPart2Rect)

    #Generate Electric bar
    generate_bar(surfaceName, 0.15 * window_size[0], 0.80 * window_size[1], status[1], status[2], status[3], yellow)

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
        clock.tick(FPS)

def generate_correct_page(surface, status, point_inc):
    #Uncomment below
    #Make Face Happy
    # controller.face_update(getFaceNum(1))
    # #Instantiate motor thread and begin it
    # motorThread = threading.Thread(target=moveHeadUpDown, args=())
    # motorThread.start()

    next_button = Button(surface, darker_blue, blue, (0.5 * window_size[0] - (0.5 *375), 0.5 * window_size[1], 750 / 2, 250 / 2), 'Next Question', mediumText)

    next_button_rect = next_button.get_rect()
    updateList = [next_button_rect]

    HeadingSurf, HeadingRect = text_objects('Correct!', largeText)
    HeadingRect.center = ((window_size[0] / 2), (window_size[1] / 4))

    ScoreSurf, ScoreRect = text_objects('Score: ' + str(status[0]) + ' (+' + str(point_inc) + ' pts)', mediumText)
    ScoreRect.center = ((window_size[0] / 2), (0.35 * window_size[1]))

    ElectricSurf, ElectricRect = text_objects('Sustainability Bar: ', mediumText)
    ElectricRect.topleft = ((0.15 * window_size[0]), (0.70 * window_size[1]))


    surface.fill(green)


    surface.blit(HeadingSurf, HeadingRect)
    surface.blit(ScoreSurf, ScoreRect)
    surface.blit(ElectricSurf, ElectricRect)
    generate_bar(surface, 0.15 * window_size[0], 0.80 * window_size[1], status[1], status[2], status[3], blue)


    pygame.display.update()

    running = True

    while running:

        #Handle events here:
        for event in pygame.event.get():
            print(event)

            if event.type == pygame.QUIT:
                #Change face to neutral
                # controller.face_update(getFaceNum())

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
        clock.tick(FPS)

    #Change face to neutral
    # controller.face_update(getFaceNum())

def generate_incorrect_page(surface, status, pt_dec, correct_ans):
    #Make Face Sad
    # controller.face_update(getFaceNum(3))
    # #Instantiate motor thread and begin it
    # motorThread = threading.Thread(target=moveHeadLeftRight, args=())
    # motorThread.start()


    next_button = Button(surface, darker_blue, blue, (0.5 * window_size[0] - (0.5 * 375), 0.5 * window_size[1], 750 / 2, 250 / 2), 'Next Question', mediumText)

    next_button_rect = next_button.get_rect()
    updateList = [next_button_rect]

    line_spacing = 100 / 2

    HeadingSurf, HeadingRect = text_objects('Sorry!', largeText)
    HeadingRect.center = ((window_size[0] / 2), (0.2 * window_size[1]))

    Heading2Surf, Heading2Rect = text_objects('Correct Answer Was:', mediumText)
    Heading2Rect.center = ((window_size[0] / 2), (window_size[1] / 4) + line_spacing)

    AnswerSurf, AnswerRect = text_objects(correct_ans, mediumText)
    AnswerRect.center = ((window_size[0] / 2), (0.25 * window_size[1]) + (2.5 * line_spacing))


    ScoreSurf, ScoreRect = text_objects('Score: ' + str(status[0]) + ' (-' + str(pt_dec) + ' pts)', mediumText)
    ScoreRect.center = ((window_size[0] / 2), (0.25 * window_size[1]) + (4 * line_spacing))

    ElectricSurf, ElectricRect = text_objects('Sustainability Bar: ', mediumText)
    ElectricRect.topleft = ((0.15 * window_size[0]), (0.70 * window_size[1]))


    surface.fill(red)


    surface.blit(HeadingSurf, HeadingRect)
    surface.blit(Heading2Surf, Heading2Rect)
    surface.blit(AnswerSurf, AnswerRect)
    surface.blit(ScoreSurf, ScoreRect)
    surface.blit(ElectricSurf, ElectricRect)

    generate_bar(surface, 0.15 * window_size[0], 0.80 * window_size[1], status[1], status[2], status[3], blue)


    pygame.display.update()

    running = True

    while running:

        #Handle events here:
        for event in pygame.event.get():
            print(event)

            if event.type == pygame.QUIT:
                #Set Face to Neutral
                # controller.face_update(getFaceNum())

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
        clock.tick(FPS)

    #Set Face to Neutral
    # controller.face_update(getFaceNum())

#Initiate pygame
pygame.init() #SUPER IMPORTANT

#Define basic text sizes
largeText = pygame.font.Font('FreeSansBold.ttf', 64)   #Large text, ideal for headings

mediumText = pygame.font.Font('FreeSansBold.ttf', 48)   #Medium text, ideal for subheadings
smallText =  pygame.font.Font('FreeSansBold.ttf', 16)   #Small text, ideal for small buttons

#Instantiate window/surface
gameDisplay = pygame.display.set_mode(window_size)
pygame.display.set_caption('Sustainability Quiz')
clock = pygame.time.Clock()

#Define number of points for each correct answer
point_increment = 100

# #Set Face to Neutral
# controller.face_update(getFaceNum())
# #Orient Head to proper position
# controller.head_update([90, 90])

#Start Menu for Game
def game_intro(surface):
    #Button Dimensions
    button_w = 1.3*(750 / 2); button_h = 1.3*(250 / 2)
    button_y = 1200 / 2
    button_spacing = window_size[1]/8 #spacing between buttons in px
    button_x = (window_size[0] - button_w)/2


    #Instantiate buttons (Only needs to be done once)
    play_button = Button(surface, darker_green, green, (button_x, button_y, button_w, button_h), 'Play', mediumText)
    help_button = Button(surface, darker_blue, blue, (button_x, button_y + button_spacing, button_w, button_h), 'Help', mediumText)
    quit_button = Button(surface, darker_red, red, (button_x, button_y + (2*button_spacing), button_w, button_h), 'Quit', mediumText)

    #Portion of the screen that must ONLY be updated
    help_button_rect = help_button.get_rect()
    play_button_rect = play_button.get_rect()
    quit_button_rect = quit_button.get_rect()
    updateList = [help_button_rect, play_button_rect, quit_button_rect]

    #Prepare title text and location
    TextSurf, TextRect = text_objects('MC Green Sustainability Quiz!', largeText, white)
    TextRect.center = ((window_size[0] / 2), (window_size[1] / 8))

    #Make entire screen white to clean it
    surface.fill(white)

    surface.blit(background, backgroundRect)

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

                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                touch_status = True

                #Check if buttons are pressed if mouse button is down
                if quit_button.is_pressed(touch_status):    #If 'Quit' button is tapped
                    pygame.quit()
                    quit()

                if play_button.is_pressed(touch_status):    #If 'Play' button is tapped
                    select_level(gameDisplay)

                if help_button.is_pressed(touch_status):    #If 'Help' button is tapped
                    game_help(gameDisplay)
            else:
                touch_status = False

        help_button.generate()
        play_button.generate()
        quit_button.generate()

        #Update only the portions that need to be updated
        pygame.display.update(updateList)
        clock.tick(FPS)

#Help Menu for Game
def game_help(surface):
    #Instantiate button for returning back to intro page
    back_button = Button(surface, darker_green, green, (0.5 * window_size[0] - (0.5* 375), 0.75 * window_size[1], 750 / 2, 250 / 2), 'Back', mediumText)

    back_button_rect = back_button.get_rect()
    updateList = [back_button_rect]

    TextSurf, TextRect = text_objects('How to Play:', largeText, white)
    TextRect.center = ((window_size[0] / 2), (window_size[1] / 8))

    line_spacing = 75   #Spacing between each line of instructions

    Line1Surf, Line1Rect = text_objects('1.) Read each question carefully and select the best answer', pygame.font.Font('FreeSansBold.ttf', 35), white)
    Line1Rect.center = ((window_size[0] / 2), (window_size[1] / 4))

    Line2Surf, Line2Rect = text_objects('2.) If your answer is correct, you will earn points', pygame.font.Font('FreeSansBold.ttf', 35), white)
    Line2Rect.center = ((window_size[0] / 2), (window_size[1] / 4) + (2 * line_spacing))
    Line2part2Surf, Line2part2Rect = text_objects('and charge your sustainability meter', pygame.font.Font('FreeSansBold.ttf', 35), white)
    Line2part2Rect.center = ((window_size[0] / 2), (window_size[1] / 4) + (3 * line_spacing))

    Line3Surf, Line3Rect = text_objects('3.) If your answer is incorrect, you will lose points', pygame.font.Font('FreeSansBold.ttf', 35), white)
    Line3Rect.center = ((window_size[0] / 2), (window_size[1] / 4) + (5 * line_spacing))
    Line3part2Surf, Line3part2Rect = text_objects(' and your charge meter will go down', pygame.font.Font('FreeSansBold.ttf', 35), white)
    Line3part2Rect.center = ((window_size[0] / 2), (window_size[1] / 4) + (6 * line_spacing))


    #Make entire screen white to clean it
    surface.fill(white)

    surface.blit(background, backgroundRect)

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

                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                touch_status = True

                #Check if buttons are pressed if mouse button is down
                if back_button.is_pressed(touch_status):
                    game_intro(gameDisplay)
            else:
                touch_status = False

        back_button.generate()

        pygame.display.update(updateList)
        clock.tick(FPS)


def select_level(surface):
    #Instantiate button for returning back to intro page
    button_w, button_h = 375, 125
    button_x = (window_size[0] - button_w)/2
    button_y = window_size[1]/4
    button_spacing = window_size[1]/8


    easy_button = Button(surface, darker_green, green, (button_x, button_y, button_w, button_h), 'Easy', mediumText)
    medium_button = Button(surface, darker_yellow, yellow, (button_x, button_y + button_spacing, button_w, button_h), 'Medium', mediumText)
    hard_button = Button(surface, darker_red, red, (button_x, button_y + (2*button_spacing), button_w, button_h), 'Hard', mediumText)
    back_button = Button(surface, darker_green, green, (button_x, button_y + (4*button_spacing), button_w, button_h), 'Back', mediumText)


    back_button_rect = back_button.get_rect()
    easy_button_rect = easy_button.get_rect()
    medium_button_rect = medium_button.get_rect()
    hard_button_rect = hard_button.get_rect()

    updateList = [back_button_rect, easy_button_rect, medium_button_rect, hard_button_rect]

    TextSurf, TextRect = text_objects('Select your level:', largeText, white)
    TextRect.center = ((window_size[0] / 2), (window_size[1] / 8))

    line_spacing = 75   #Spacing between each line of instructions

    #Make entire screen white to clean it
    surface.fill(white)

    surface.blit(background, backgroundRect)

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

                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                touch_status = True

                #Check if buttons are pressed if mouse button is down
                if back_button.is_pressed(touch_status):
                    game_intro(gameDisplay)
                if easy_button.is_pressed(touch_status):
                    point_vals = data["point_vals"]["level_easy"]
                    q_set = [q for q in data["level_easy"]]
                    game_menu(gameDisplay, point_vals, q_set)
                if medium_button.is_pressed(touch_status):
                    point_vals = data["point_vals"]["level_medium"]
                    q_set = [q for q in data["level_medium"]]
                    game_menu(gameDisplay, point_vals, q_set)
                if hard_button.is_pressed(touch_status):
                    point_vals = data["point_vals"]["level_hard"]
                    q_set = [q for q in data["level_hard"]]
                    game_menu(gameDisplay, point_vals, q_set)

            else:
                touch_status = False

        back_button.generate()
        easy_button.generate()
        medium_button.generate()
        hard_button.generate()

        pygame.display.update(updateList)
        clock.tick(FPS)


def game_menu(surface, point_vals, q_set):
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
        outcome = generate_q_page(surface, status, pt_inc, question, choices, correct_ans)

        if outcome == 'correct':
            status[0] += pt_inc
            status[1] += 1
            generate_correct_page(surface, status, pt_inc)

        elif outcome == 'incorrect':
            if (status[0] != 0):
                status[0] -= pt_dec

            status[2] += 1
            generate_incorrect_page(surface, status, pt_dec, correct_ans)

    game_over(surface, status)


def game_over(surface, status):
    #Set Face to Happy, regardless of score
    # controller.face_update(getFaceNum(1))

    #Button Dimensions
    button_w = 750 / 2; button_h = 250 / 2

    menu_button = Button(surface, darker_blue, blue, (window_size[0] / 2 - (0.5 * 375), 0.75 * window_size[1], button_w, button_h), 'Menu', mediumText)

    menu_button_rect = menu_button.get_rect()

    updateList = [menu_button_rect]


    #Prepare title text and location
    TextSurf, TextRect = text_objects('Game Over!', largeText)
    TextRect.center = ((window_size[0] / 2), (window_size[1] / 4))

    FinalSurf, FinalRect = text_objects('Final Score: ' + str(status[0]) + ' pts', mediumText)
    FinalRect.center = ((window_size[0] / 2), (0.4 * window_size[1]))

    ElectricSurf, ElectricRect = text_objects('Sustainability Bar: ', mediumText)
    ElectricRect.topleft = ((0.15 * window_size[0]), (0.55 * window_size[1]))

    #Make entire screen white to clean it
    surface.fill(green)

    #Write text to buffer
    surface.blit(TextSurf, TextRect)
    surface.blit(FinalSurf, FinalRect)
    surface.blit(ElectricSurf, ElectricRect)
    generate_bar(surface, 0.15 * window_size[0], 0.65 * window_size[1], status[1], status[2], status[3], blue)

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
                    clock.tick(FPS)
                    game_intro(gameDisplay)

            else:
                touch_status = False

        menu_button.generate()

        #Update only the portions that need to be updated
        pygame.display.update(updateList)
        clock.tick(FPS)




#Execute game
game_intro(gameDisplay)

# #Set Face to Neutral
# controller.face_update(getFaceNum())
# #Orient Head to proper position
# controller.head_update([90, 90])
pygame.quit()
quit()
