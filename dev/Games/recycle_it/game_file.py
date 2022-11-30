#!/usr/bin/python3
import pygame
from pygame import mixer
import random
import time
import math
import sys
import json
import threading

# sys.path.append("../")
# from head_controller import Head_comm
#
# controller = Head_comm("Recycle It")
# Initialize pygame
pygame.init()

#threading trackers
active_head = 0
active_face = 0

# Screen Size (x,y)
window = (1080, 1920)
screen = pygame.display.set_mode(window)

# Background
background = pygame.image.load('gamebkg.png')
background = pygame.transform.scale(background, (window[0], window[1]//2))
game_lst = pygame.image.load('gameLostBkg.png')
#game_1st = pygame.transform.scale(game_lst, (window[0], window[1]//2))
game_wn = pygame.image.load('gameWonBkg.png')
#game_wn = pygame.transform.scale(game_wn, (window[0], window[1]//2))
menu = pygame.image.load('menubkg.png')
menu = pygame.transform.scale(menu, (window[0], window[1]//2))
menuForHelps = pygame.transform.scale(menu, (1080,590))
helps = pygame.image.load('newhelpbkg.png')
helps = pygame.transform.scale(helps, (1080, 740))

# Buttons
Back_Arrow = pygame.image.load('Back_Arrow.png')
Back_Arrow = pygame.transform.scale(Back_Arrow, (100,70))
empty = pygame.image.load('Empty.png')
playb = pygame.image.load('play.png')
playb = pygame.transform.scale(playb, (700,222))
helpb = pygame.image.load('help.png')
helpb = pygame.transform.scale(helpb, (700,222))
exitb = pygame.image.load('exit.png')
exitb = pygame.transform.scale(exitb, (700,222))
lvl1 = pygame.image.load('lvl1.png')
lvl1 = pygame.transform.scale(lvl1, (700,222))
lvl2 = pygame.image.load('lvl2.png')
lvl2 = pygame.transform.scale(lvl2, (700,222))
lvl3 = pygame.image.load('lvl3.png')
lvl3 = pygame.transform.scale(lvl3, (700,222))
invplayb = pygame.image.load('invplay.png')
invplayb = pygame.transform.scale(invplayb, (700,222))
invhelpb = pygame.image.load('invhelp.png')
invhelpb = pygame.transform.scale(invhelpb, (700,222))
invexitb = pygame.image.load('invexit.png')
invexitb = pygame.transform.scale(invexitb, (700,222))
invlvl1 = pygame.image.load('invlvl1.png')
invlvl1 = pygame.transform.scale(invlvl1, (700,222))
invlvl2 = pygame.image.load('invlvl2.png')
invlvl2 = pygame.transform.scale(invlvl2, (700,222))
invlvl3 = pygame.image.load('invlvl3.png')
invlvl3 = pygame.transform.scale(invlvl3, (700,222))

#JSON
with open('explanation.json', 'r') as file:
    data = json.load(file)
# Background Music
mixer.music.load('backgroundmsc.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Recycle It or Not!")
icon = pygame.image.load('logo.png')
pygame.display.set_icon(icon)

# Score
points_value = 0
largeText = pygame.font.Font('Bubblegum.ttf', 100)   #Large text, ideal for headings
mediumLargeText = pygame.font.Font('Bubblegum.ttf', 80)
mediumText = pygame.font.Font('Bubblegum.ttf', 48)   #Medium text, ideal for subheadings
mediumText2 = pygame.font.Font('Bubblegum.ttf', 24)
smallText =  pygame.font.Font('Bubblegum.ttf', 16)   #Small text, ideal for small buttons
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
darker_red = (200, 0, 0)
green = (0, 255, 0)
darker_green = (0, 200, 0)
blue = (50, 89, 250)
darker_blue = (35, 67, 250)
font = pygame.font.Font('Bubblegum.ttf', 32)
textX = 10
textY = 10

# Number of enemies and good objects at any given time
num_of_each = 5

# Player + Starting Coordinates
playerImg = pygame.image.load('character_bin.png')
playerX = window[0]/2
playerY = 3*window[1]/4
playerX_change = 0

# enemy -- non-recyclables


# timer + level
clock = pygame.time.Clock()
seconds = 0
milliseconds = 0

level = 0

class Button:
    def __init__ (self, ac, ic, rectVals):
        self.ac = ac #Active color of button
        self.ic = ic #Inactive color of button
        self.rectAttrs = rectVals #(x, y, w, h) of button

    def generate(self):
        x, y, w, h = self.rectAttrs
        mouse = pygame.mouse.get_pos()

        #Check if mouse is on button
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            screen.blit(self.ac, (self.rectAttrs[0], self.rectAttrs[1]))

        #Else just show darker button
        else:
            screen.blit(self.ic, (self.rectAttrs[0], self.rectAttrs[1]))




        pygame.display.update()



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


def show_score(pts, x, y):
    score = font.render("Score: " + str(pts), True, (0, 0, 0))
    screen.blit(score, (x, y))


# Checking Collision by using distance formula between objects
# parameter is named var because function can be used by enemies and good objects
def isCollision(varX, varY, playerX, playerY):
    distance = math.sqrt((math.pow(varX - playerX, 2)) + (math.pow(varY - playerY, 2)))
    if distance < 27:
        return True
    else:
        return False


def game_over(pts):
    if level == 0:
        if pts >= 600:
            game_won(pts)
        else:
            game_lost(pts)
    if level == 1:
        if pts >= 800:
            game_won(pts)
        else:
            game_lost(pts)
    if level == 2:
        if pts >= 1000:
            game_won(pts)
        else:
            game_lost(pts)


#threaded function
#set vertical = true for vertical movement (auto x = 90) false for opposite
def rotate_head(vertical, positions):
    global active_head
    print("---------------", flush=True)
    print("vertical: ", vertical, flush=True)
    print("positions: ", positions, flush=True)
    if active_head == 0:
        active_head +=1
        current_pos = 90
        for x in positions:
            print("x: ", x, flush=True)
            if vertical == True:
                controller.head_update([90, x])
            else:
                controller.head_update([x,90])
            print("servo update sent", flush=True)
            delay = float(abs(current_pos - x)) / 60. *.14*5
            print("delay: ", delay, flush=True)
            time.sleep(delay)
            current_pos = x
        active_head -= 1

#threaded function
#change face and then revert to normal after x time

def change_face(expression, delay):
    global active_face
    print("+++++++++++++++++++++++++++++++++=", flush=True)
    print ("expression: ", expression, flush=True)
    print("delay: ", delay, flush=True)
    #print("name: ", str(threading.current_thread().name))
    print("count: ", active_face)
    if active_face == 0:
        active_face += 1
        controller.face_update(expression)
        print("face update sent", flush=True)
        time.sleep(delay)
        controller.face_update(4)
        print("face reset sent", flush=True)
        active_face -= 1

def explanation_page():
    screen.fill((255, 255, 255))
    back = Button(Back_Arrow, Back_Arrow, (20, 20, 100, 70))
    titleSurf, titleRect = text_objects('Press an Item to Learn', mediumLargeText, black)
    titleRect.center = (window[0]/2, 130)
    screen.blit(titleSurf, titleRect)
    titleSurf2, titleRect2 = text_objects('More About It', mediumLargeText, black)
    titleRect2.center = (window[0]/2, 230)
    screen.blit(titleSurf2, titleRect2)
    #good/recyclable
    goodSurf, goodRect = text_objects('Recyclable Items', mediumText, black)
    goodRect.center = (window[0]/2, window[1]/6)
    screen.blit(goodSurf, goodRect)
    gBag = pygame.image.load('good_bag.png')
    gBag = pygame.transform.scale(gBag, (100, 100))
    gSoda = pygame.image.load('good_soda.png')
    gSoda = pygame.transform.scale(gSoda, (100, 100))
    plas1 = pygame.image.load('plastic1.png')
    plas1 = pygame.transform.scale(plas1, (100, 100))
    plas2 = pygame.image.load('plastic2.png')
    plas2 = pygame.transform.scale(plas2, (100, 100))
    gBagButton = Button(gBag, gBag, (1 * window[0]/5 - 50, window[1]/4 - 50, 100, 100))
    gSodaButton = Button(gSoda, gSoda, (2 * window[0]/5 - 50, window[1]/4 - 50, 100, 100))
    plas1Button = Button(plas1, plas1, (3 * window[0]/5 - 50, window[1]/4 - 50, 100, 100))
    plas2Button = Button(plas2, plas2, (4 * window[0]/5 - 50, window[1]/4 - 50, 100, 100))

    #bad/notrecyclable
    badSurf, badRect = text_objects('Not Recyclable Items', mediumText, black)
    badRect.center = (window[0]/2, 3 * window[1]/7)
    screen.blit(badSurf, badRect)
    bBanana = pygame.image.load('enemy_banana.png')
    bBanana = pygame.transform.scale(bBanana, (100, 100))
    bCore = pygame.image.load('enemy_core.png')
    bCore = pygame.transform.scale(bCore, (100, 100))
    bTrash = pygame.image.load('enemy_trash.png')
    bTrash = pygame.transform.scale(bTrash, (100, 100))
    plas6 = pygame.image.load('plastic6.png')
    plas6 = pygame.transform.scale(plas6, (100, 100))
    plas3 = pygame.image.load('plastic3.png')
    plas3 = pygame.transform.scale(plas3, (100, 100))
    bPizza = pygame.image.load('pizza.png')
    bPizza = pygame.transform.scale(bPizza, (100, 100))
    bBag = pygame.image.load('bag.png')
    bBag = pygame.transform.scale(bBag, (100, 100))
    bBananaButton = Button(bBanana, bBanana, (1 * window[0]/8 - 50, 43 * window[1]/84 - 50, 100, 100))
    bCoreButton = Button(bCore, bCore, (2 * window[0]/8 - 50, 43 * window[1]/84 - 50, 100, 100))
    bTrashButton = Button(bTrash, bTrash, (3 * window[0]/8 - 50, 43 * window[1]/84 - 50, 100, 100))
    plas3Button = Button(plas3, plas3, (4 * window[0]/8 - 50, 43 * window[1]/84 - 50, 100, 100))
    plas6Button = Button(plas6, plas6, (5 * window[0]/8 - 50, 43 * window[1]/84 - 50, 100, 100))
    bPizzaButton = Button(bPizza, bPizza, (6 * window[0]/8 - 50, 43 * window[1]/84 - 50, 100, 100))
    bBagButton = Button(bBag, bBag, (7 * window[0]/8 - 50, 43 * window[1]/84 - 50, 100, 100))


    #special recycling
    neutSurf, neutRect = text_objects('Special Collection Items (LVL 3 Only)', mediumText, black)
    neutRect.center = (window[0]/2, 29 * window[1]/42)
    screen.blit(neutSurf, neutRect)
    clothes = pygame.image.load('clothes.png')
    clothes = pygame.transform.scale(clothes, (100, 100))
    computer = pygame.image.load('computer.png')
    computer = pygame.transform.scale(computer, (100, 100))
    medicine = pygame.image.load('medicine.png')
    medicine = pygame.transform.scale(medicine, (100, 100))
    shreddedPaper = pygame.image.load('shreddedpaper.png')
    shreddedPaper = pygame.transform.scale(shreddedPaper, (100, 100))
    tire = pygame.image.load('tire.png')
    tire = pygame.transform.scale(tire, (100, 100))
    clothesButton = Button(clothes, clothes, (1 * window[0]/6 - 50, 65 * window[1]/84 - 50, 100, 100))
    computerButton = Button(computer, computer, (2 * window[0]/6 - 50, 65 * window[1]/84 - 50, 100, 100))
    medicineButton = Button(medicine, medicine, (3 * window[0]/6 - 50, 65 * window[1]/84 - 50, 100, 100))
    shreddedPaperButton = Button(shreddedPaper, shreddedPaper, (4 * window[0]/6 - 50, 65 * window[1]/84 - 50, 100, 100))
    tireButton = Button(tire, tire, (5 * window[0]/6 - 50, 65 * window[1]/84 - 50, 100, 100))
    loop = True
    while loop:

        gBagButton.generate()
        gSodaButton.generate()
        plas1Button.generate()
        plas2Button.generate()
        bBananaButton.generate()
        bCoreButton.generate()
        bTrashButton.generate()
        plas3Button.generate()
        plas6Button.generate()
        bPizzaButton.generate()
        bBagButton.generate()
        clothesButton.generate()
        computerButton.generate()
        medicineButton.generate()
        shreddedPaperButton.generate()
        tireButton.generate()
        back.generate()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                touch_status = True
                if gBagButton.is_pressed(touch_status):
                    explanation_template("Paper Bag")
                if gSodaButton.is_pressed(touch_status):
                    explanation_template("Soda Can")
                if plas1Button.is_pressed(touch_status):
                    explanation_template("Type 1 Plastic")
                if plas2Button.is_pressed(touch_status):
                    explanation_template("Type 2 Plastic")
                if bBananaButton.is_pressed(touch_status):
                    explanation_template("Banana Peel")
                if bCoreButton.is_pressed(touch_status):
                    explanation_template("Apple Core")
                if bTrashButton.is_pressed(touch_status):
                    explanation_template("Trash Bags")
                if plas3Button.is_pressed(touch_status):
                    explanation_template("Type 3 Plastic")
                if plas6Button.is_pressed(touch_status):
                    explanation_template("Type 6 Plastic")
                if bPizzaButton.is_pressed(touch_status):
                    explanation_template("Pizza Box")
                if bBagButton.is_pressed(touch_status):
                    explanation_template("Bag of Recyclables")
                if clothesButton.is_pressed(touch_status):
                    explanation_template("Clothes")
                if computerButton.is_pressed(touch_status):
                    explanation_template("Computers")
                if medicineButton.is_pressed(touch_status):
                    explanation_template("Medicine")
                if shreddedPaperButton.is_pressed(touch_status):
                    explanation_template("Shredded Paper")
                if tireButton.is_pressed(touch_status):
                    explanation_template("Tires")
                if(back.is_pressed(touch_status)):
                    intro()


def  explanation_template(item):
    back = Button(Back_Arrow, Back_Arrow, (20, 20, 100, 70))
    screen.fill(white)
    titleSurf, titleRect = text_objects(item, largeText, black)
    titleRect.center = (window[0]/2, 200)
    screen.blit(titleSurf, titleRect)
    image = pygame.image.load(data["images"][item])
    image = pygame.transform.scale(image, (400, 400))
    screen.blit(image, (window[0]/2 - 200, window[1]/5 * 2 - 200))
    explanation = data["explanations"][item]
    expSplit = explanation.split('||')
    textSurf, textRect = text_objects(expSplit[0], mediumText, black)
    textRect.center = (window[0]/2, window[1] * 2/3)
    if '||' in explanation:
        textSurf2, textRect2 = text_objects(expSplit[1], mediumText, black)
        textRect2.center = (window[0]/2, window[1] * 2/3 +50)
        screen.blit(textSurf2, textRect2)
    screen.blit(textSurf, textRect)
    loop = True
    pygame.display.update()
    while loop:
        back.generate()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                touch_status = True
                if(back.is_pressed(touch_status)):
                    explanation_page()

def game_won(pts):
    # face = random.randint(1, 3)  # HEEEEEEEEEEEEEEEEEERRRRRRRRRRRRRRRRRREEEEEEEEEEEEEE
    # controller.face_update(face)
    # # These commands won't over write themselves right? like if i say these three in a row
    # # it'll hit all of the positions before going back to [90,90]?
    # # controller.head_update([90, 45])
    # # controller.head_update([90, 135])
    # # controller.head_update([90, 90])
    # rotate=threading.Thread(target=rotate_head, args=(True, [45, 135, 90]))
    # rotate.start()
    mixer.music.load('game_won.wav')
    mixer.music.play()
    pause = True
    back = Button(Back_Arrow, Back_Arrow, (20, 20, 100, 70))

    while pause:
        screen.fill((255, 255, 255))

        screen.blit(game_wn, (50, window[1]/4))
        show_score(pts, window[0]/2 - 70, 2*window[1]/3)
        back.generate()
        pygame.display.update()
        for event in pygame.event.get():
            # Quitting the Game by X-ing out Window
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE or event.type == pygame.MOUSEBUTTONDOWN:
                    level_select(level)
                if event.key == pygame.K_SPACE:
                    pts = 0
                    game(playerX, points_value, playerX_change, milliseconds, seconds, level)
            if event.type == pygame.MOUSEBUTTONDOWN:
                touch_status = True
                if(back.is_pressed(touch_status)):
                    intro()




def game_lost(pts):
    # face = random.randint(5, 7)  # HHHHHHHHHHHHHHEEEEEEEEEEEEERRRRRRRRRRRREEEEEEEEEEEE
    # controller.face_update(face)
    #See game_won head update comments
    # controller.head_update([45, 90])
    # controller.head_update([135, 90])
    # controller.head_update([90, 90])
    # rotate=threading.Thread(target=rotate_head, args=(False, [45, 135, 90]))
    # rotate.start()

    back = Button(Back_Arrow, Back_Arrow, (20, 20, 100, 70))
    explanation = Button(lvl1, invlvl1, (window[0]/2 - 750/2, window[1] - 450, 750, 222))

    mixer.music.load('game_lose.wav')
    mixer.music.play()
    pause = True
    screen.fill((255, 255, 255))
    while pause:

        screen.blit(game_lst, (50, window[1]/4))
        show_score(pts, window[0]/2 - 70, 2*window[1]/3)
        explanation.generate()
        back.generate()

        pygame.display.update()
        for event in pygame.event.get():
            # Quitting the Game by X-ing out Window
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    level_select(level)
                if event.key == pygame.K_SPACE:
                    pts = 0
                    game(playerX, points_value, playerX_change, milliseconds, seconds, level)
            if event.type == pygame.MOUSEBUTTONDOWN:
                touch_status = True
                if(back.is_pressed(touch_status)):
                    intro()
                if(explanation.is_pressed(touch_status)):
                    explanation_page()

        pygame.display.update()


def intro():
    bmenu = True
    screen.fill((255, 255, 255))
    screen.blit(menu, (0, 0))
    screen.blit(menu, (0,window[1]/2))
    # controller.face_update(4)  # HEEEEEEEEEEEEEERRRREEEEEEEEEEEEE
    playbutton = Button(invplayb, playb, (window[0]/2 - 750/2, window[1]/4, 750, 222))
    helpbutton = Button(invhelpb, helpb, (window[0]/2 - 750/2,  window[1]/2, 750, 222))
    quitbutton = Button(invexitb, exitb, (window[0]/2 - 750/2,  3*window[1]/4, 750, 222))
    TextSurf, TextRect = text_objects("Recycle It!", largeText, blue)
    TextRect.center = (window[0]/2,190)
    screen.blit(TextSurf,TextRect)
    while bmenu:

        playbutton.generate()
        helpbutton.generate()
        quitbutton.generate()
        for event in pygame.event.get():
            # Quitting the Game by X-ing out Window
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            touch_status = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                touch_status = True
                if(playbutton.is_pressed(touch_status)):
                    level_select(level)
                if(helpbutton.is_pressed(touch_status)):
                    help_screen()
                if(quitbutton.is_pressed(touch_status)):
                    pygame.quit()
                    quit()



        # print(click)




        pygame.display.update()


def ready():
    message = ["Ready ", "Ready. ", "Ready.. ", "Ready... ", "Set ", "Set. ", "Set.. ", "Set... ", "GO! " ]
    for i in range(9):
        screen.fill((255, 255, 255))
        screen.blit(background, (-50, window[1]/4))
        ready = font.render(message[i], True, (0, 0, 0))
        screen.blit(ready, (window[0]/2 - 50, window[1]/2))
        pygame.display.update()
        pygame.time.delay(750)





def help_screen():

    bhelp = True
    back = Button(Back_Arrow, Back_Arrow, (20, 20, 100, 70))
    while bhelp:
        screen.fill((255, 255, 255))
        screen.blit(menuForHelps, (0,0))
        screen.blit(helps, (0, 590))
        screen.blit(menuForHelps, (0,1330))
        back.generate()
        for event in pygame.event.get():
            # Quitting the Game by X-ing out Window
            if event.type == pygame.MOUSEBUTTONDOWN:
                touch_status = True
                if(back.is_pressed(touch_status)):
                    intro()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # keystroke check (right/left) and changing val of playerX_change to +/- based on keypress
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    intro()
        pygame.display.update()


def level_select(lvl):
    pygame.time.delay(750)
    bmenu = True
    screen.fill((255, 255, 255))
    screen.blit(menu, (0, 0))
    screen.blit(menu, (0,window[1]/2))
    lvl1b = Button(invlvl1, lvl1, (window[0]/2 - 750/2, window[1]/4, 700, 222))
    lvl2b = Button(invlvl2, lvl2, (window[0]/2 - 750/2, window[1]/2, 700, 222))
    lvl3b = Button(invlvl3, lvl3, (window[0]/2 - 750/2, 3*window[1]/4, 700, 222))
    back = Button(Back_Arrow, Back_Arrow, (20, 20, 100, 70))
    TextSurf, TextRect = text_objects("Select a Level", largeText, blue)
    TextRect.center = (window[0]/2,190)
    screen.blit(TextSurf,TextRect)
    while bmenu:
        lvl1b.generate()
        lvl2b.generate()
        lvl3b.generate()
        back.generate()
        for event in pygame.event.get():
            # Quitting the Game by X-ing out Window
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    intro()
            if event.type == pygame.MOUSEBUTTONDOWN:
                touch_status = True
                if(lvl1b.is_pressed(touch_status)):
                    ready()
                    game(playerX, points_value, playerX_change, milliseconds, seconds, 0)
                if(lvl2b.is_pressed(touch_status)):
                    ready()
                    game(playerX, points_value, playerX_change, milliseconds, seconds, 1)
                if(lvl3b.is_pressed(touch_status)):
                    ready()
                    game(playerX, points_value, playerX_change, milliseconds, seconds, 2)
                if(back.is_pressed(touch_status)):
                    intro()

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()


        pygame.display.update()









# Game Loop
def game(playerX, pts, playerX_change, milliseconds, seconds, lvl):
    old = 0
    seconds = 0
    milliseconds = 0
    lMove = Button(empty, empty, (0,0, window[0]/2, window[1]))
    rMove = Button(empty, empty, (window[0]/2,0, window[0]/2, window[1]))
    back = Button(Back_Arrow, Back_Arrow, (20, 20, 100, 70))
    mixer.music.load('backgroundmsc.wav')
    mixer.music.play(-1)

    if(lvl == 1):
        fallspeed = 8
    else:
        fallspeed = 7
    bgame = True
    num_of_each = 3
    if(lvl == 2):
        num_of_each = 2
    goodX = []
    goodY = []
    goodY_change = []
    goodImg = []
    neutX = []
    neutY = []
    neutY_change = []
    neutImg = []
    enemyImg = []
    enemyX = []
    enemyY = []
    enemyY_change = []
    lMove.generate()
    rMove.generate()
    move_speed = 10
    screen.fill((255, 255, 255))
    clock.tick_busy_loop(60)
    while bgame:
        # RGB Screen Fill - Red, Green, Blue

        back.generate()

        screen.fill((255, 255, 255))
        show_score(pts, textX, 100)
        # setting background
        screen.blit(background, (-50, window[1]/4))

        # Checking for events (keypress)
        #for event in pygame.event.get():
            # Quitting the Game by X-ing out Window

            # keystroke check (right/left) and changing val of playerX_change to +/- based on keypress

        # changes X position of player character

        #listEvents = pygame.event.get()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            keys_pressed = pygame.key.get_pressed()
            mousepos = pygame.mouse.get_pos()
            if keys_pressed[pygame.K_LEFT] and keys_pressed[pygame.K_RIGHT]:
                playerX_change = 0
            elif keys_pressed[pygame.K_LEFT] :
                playerX_change = -move_speed
            elif keys_pressed[pygame.K_RIGHT]:
                playerX_change = move_speed
        #    elif event.type != pygame.MOUSEBUTTONDOWN:
        #        playerX_change = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                touch_status = True
                if(back.is_pressed(touch_status)):
                    level_select(level)



                if (lMove.is_pressed(touch_status)):
                    playerX_change = -move_speed
                elif (rMove.is_pressed(touch_status)):
                    playerX_change = move_speed
            if event.type == pygame.MOUSEBUTTONUP:
                playerX_change = 0



        if keys_pressed[pygame.K_ESCAPE]:
                level_select(level)

        playerX += playerX_change
        caphold = 76
        cap = caphold
        randol = random.randint(1, cap)
        if(len(goodImg) <= num_of_each and randol == 1):
            # choosing which good object to show
            goodSelect = random.randint(1, 4)
            if goodSelect == 1:
                goodImg.append(pygame.image.load('good_bag.png'))
            if goodSelect == 2:
                goodImg.append(pygame.image.load('good_soda.png'))
            if goodSelect == 3:
                goodImg.append(pygame.image.load('plastic1.png'))
            if goodSelect == 4:
                goodImg.append(pygame.image.load('plastic2.png'))
            # random spawn of good object
            goodX.append(random.randint(0, window[0] - 64))
            goodY.append(random.randint(0, 200) - 300)
            # speed of fall
            goodY_change.append(fallspeed)
            cap = caphold

        elif(len(enemyImg) <= num_of_each and randol == 2):
            # choosing which enemy to show
            enemySelect = random.randint(1, 7)
            if enemySelect == 1:
                enemyImg.append(pygame.image.load('enemy_banana.png'))
            if enemySelect == 2:
                enemyImg.append(pygame.image.load('enemy_core.png'))
            if enemySelect == 3:
                enemyImg.append(pygame.image.load('enemy_trash.png'))
            if enemySelect == 4:
                enemyImg.append(pygame.image.load('plastic6.png'))
            if enemySelect == 5:
                enemyImg.append(pygame.image.load('plastic3.png'))
            if enemySelect == 6:
                enemyImg.append(pygame.image.load('pizza.png'))
            if enemySelect == 7:
                enemyImg.append(pygame.image.load('bag.png'))
            # random spawn location of enemy
            enemyX.append(random.randint(0, window[0] - 64))
            enemyY.append(random.randint(0, 200) - 300)
            # speed of fall
            enemyY_change.append(fallspeed)
            cap = caphold
        else:
            cap -= 5


        if(lvl == 2):
            if(len(neutImg) <= num_of_each and randol == 3):
                # choosing which neut object to show
                goodSelect = random.randint(1, 6)
                if goodSelect == 1:
                    neutImg.append(pygame.image.load('clothes.png'))
                if goodSelect == 2:
                    neutImg.append(pygame.image.load('computer.png'))
                if goodSelect == 3:
                    neutImg.append(pygame.image.load('medicine.png'))
                if goodSelect == 4:
                    neutImg.append(pygame.image.load('shreddedpaper.png'))
                if goodSelect == 5:
                    neutImg.append(pygame.image.load('plasticbag.png'))
                if goodSelect == 6:
                    neutImg.append(pygame.image.load('tire.png'))
                # random spawn of good object
                neutX.append(random.randint(0, window[0] - 64))
                neutY.append(random.randint(0, 200) - 300)
                # speed of fall
                neutY_change.append(fallspeed)






        # Changes y position of enemies and good objects
        for i in range(len(goodImg)):
            if(i >= len(goodImg)):
                break
            goodY[i] += goodY_change[i]


            # Checking for collision

            goodCollision = isCollision(goodX[i], goodY[i], playerX, playerY)

            # Adding points to score
            if goodCollision:
                good_catch = mixer.Sound('good_catch.wav')
                #good_catch.play()
                # face = random.randint(1, 3)  # HHHHHEEEEEEEEEEEEEEERRRRRRRRRRRRREEEEEEEEEEEEE
                # good_face = threading.Thread(target=change_face, args=(face, 0.5,))
                # good_face.daemon=True
                # good_face.start()
                # controller.face_update(face)
                # # should i delay here? cuz it's gonna delay the entire program or is that on ur end?
                # # either way i'll include and u can play around
                # # time.sleep(2)
                # controller.face_update(4)
                pts += 100
                print(pts)
                # Sending good object to top of screen in a New location
                del goodX[i]
                del goodY[i]
                del goodY_change[i]
                del goodImg[i]
                i -= 1
            elif goodY[i] > 3*window[1]/4 + 50:
                del goodX[i]
                del goodY[i]
                del goodY_change[i]
                del goodImg[i]
                i -= 1
            else:
                screen.blit(goodImg[i], (goodX[i], goodY[i]))

        for i in range(len(enemyImg)):
            if(i >= len(enemyImg)):
                break
            enemyY[i] += enemyY_change[i]
            badCollision = isCollision(enemyX[i], enemyY[i], playerX, playerY)
            if badCollision:
                bad_catch = mixer.Sound('bad_catch.wav')
                # DISPLAY THE SURPRISED FACE HERE FOR 1 SECOND AND REVERT BACK TO NEUTRAL
                #bad_catch.play()
                # face = random.randint(5, 7)  # HHHHHHHEEEEEEEEEEEEEERRRRRRRRRRRRREEEEEEEEEEEE
                # controller.face_update(face)
                # # should i delay here? cuz it's gonna delay the entire program or is that on ur end?
                # # either way i'll include and u can play around
                # # time.sleep(2)
                # controller.face_update(4)
                # bad_face = threading.Thread(target=change_face, args=(face, 0.5,))
                # bad_face.start()
                pts -= 50
                print(pts)
                # Sending bad object to top of screen in a new location
                del enemyX[i]
                del enemyY[i]
                del enemyY_change[i]
                del enemyImg[i]
                i -= 1

            elif enemyY[i]> 3*window[1]/4 + 50:
                del enemyX[i]
                del enemyY[i]
                del enemyY_change[i]
                del enemyImg[i]
                i -= 1

            else:

                screen.blit(enemyImg[i], (enemyX[i], enemyY[i]))
        if(lvl == 2):
            for i in range(len(neutImg)):
                if(i >= len(neutImg)):
                    break
                neutY[i] += neutY_change[i]
                neutCollision = isCollision(neutX[i], neutY[i], playerX, playerY)
                if neutCollision:

                    # DISPLAY THE SURPRISED FACE HERE FOR 1 SECOND AND REVERT BACK TO NEUTRAL
                    #bad_catch.play()
                    # face = random.randint(5, 7)  # HHHHHHHEEEEEEEEEEEEEERRRRRRRRRRRRREEEEEEEEEEEE
                    # controller.face_update(face)
                    # # should i delay here? cuz it's gonna delay the entire program or is that on ur end?
                    # # either way i'll include and u can play around
                    # # time.sleep(2)
                    # controller.face_update(4)
                    # bad_face = threading.Thread(target=change_face, args=(face, 0.5,))
                    # bad_face.start()
                    pts -= 0
                    print(pts)
                    # Sending bad object to top of screen in a new location
                    del neutX[i]
                    del neutY[i]
                    del neutY_change[i]
                    del neutImg[i]
                    i -= 1

                elif neutY[i] > 3*window[1]/4 + 50:
                    del neutX[i]
                    del neutY[i]
                    del neutY_change[i]
                    del neutImg[i]
                    i -= 1

                else:

                    screen.blit(neutImg[i], (neutX[i], neutY[i]))

        # Setting Boundaries for Recycle Bin --> Doesn't go out of game window
        if playerX <= 0:
            playerX = 0
        elif playerX >= window[0] - 64:
            playerX = window[0] - 64

        # Creating Player Object
        screen.blit(playerImg, (playerX, playerY))
        back.generate()
        # Show Score Function
        show_score(pts, textX, 100)

        # Timer


        # Updating display
        pygame.display.update()
        if milliseconds > 1000:
            seconds += 1
            milliseconds -= 1000
        if seconds == 60:
            game_over(pts)

        print(seconds)
        #print(clock.tick_busy_loop(40))
        #if(clock.tick_busy_loop(40) > 1000):
        #    milliseconds += 50
        #else:
        #clock.tick_busy_loop(60)
        milliseconds += clock.tick_busy_loop(60)
        new = pygame.time.get_ticks()
        dif = new - old
        #print(dif)
        old = pygame.time.get_ticks()

intro()
