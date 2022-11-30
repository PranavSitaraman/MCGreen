#!/usr/bin/python3
import pygame
from pygame import mixer
import random
import time
import math
import sys
import json
import threading
sys.path.append("../")
import error
#from game_interface import Game_Interface

class Recycle_IT:
    def __init__ (self, ros_controller):
        # sys.path.append("../")
        # from head_controller import Head_comm
        #
        # controller = Head_comm("Recycle It")
        # Initialize pygame
        pygame.init()

        #self.ros_controller = ros_controller

        #threading trackers
        #active_head = 0
        #active_face = 0

        # Screen Size (x,y)
        self.window = (1080, 1920)
        self.screen = pygame.display.set_mode(self.window)

        # Background
        self.background = pygame.image.load('gamebkg.png')
        self.background = pygame.transform.scale(self.background, (self.window[0], self.window[1]//2))




        self.menu = pygame.image.load('menubkg.png')
        self.menu = pygame.transform.scale(self.menu, (self.window[0], self.window[1]//2))



        # Buttons
        self.Back_Arrow = pygame.image.load('Back_Arrow.png')
        self.Back_Arrow = pygame.transform.scale(self.Back_Arrow, (100,70))
        self.empty = pygame.image.load('Empty.png')



        #JSON
        with open('explanation.json', 'r') as file:
            self.data = json.load(file)
        # Background Music
        mixer.music.load('backgroundmsc.wav')
    #    mixer.music.play(-1)

        # Title and Icon
        pygame.display.set_caption("Recycle It or Not!")
        icon = pygame.image.load('logo.png')
        pygame.display.set_icon(icon)

        # Score
        self.points_value = 0
        self.largeText = pygame.font.Font('Bubblegum.ttf', 100)   #Large text, ideal for headings
        self.mediumLargeText = pygame.font.Font('Bubblegum.ttf', 80)
        self.mediumText = pygame.font.Font('Bubblegum.ttf', 48)   #Medium text, ideal for subheadings
        self.mediumText2 = pygame.font.Font('Bubblegum.ttf', 24)
        self.smallText =  pygame.font.Font('Bubblegum.ttf', 16)   #Small text, ideal for small buttons
        self.font = pygame.font.Font('Bubblegum.ttf', 32)
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.darker_red = (200, 0, 0)
        self.green = (0, 255, 0)
        self.darker_green = (0, 200, 0)
        self.blue = (50, 89, 250)
        self.darker_blue = (35, 67, 250)
        self.font = pygame.font.Font('Bubblegum.ttf', 32)
        self.textX = 10
        self.textY = 10

        # Number of enemies and good objects at any given time
        self.num_of_each = 5


        # enemy -- non-recyclables


        # timer + level
        self.clock = pygame.time.Clock()


        self.level = 0
    def text_objects(self,text, font, color=(0,0,0)):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()


    def show_score(self, pts, x, y):
        score = self.font.render("Score: " + str(pts), True, (0, 0, 0))
        self.screen.blit(score, (x, y))


    # Checking Collision by using distance formula between objects
    # parameter is named var because function can be used by enemies and good objects
    def isCollision(self, varX, varY, playerX, playerY):
        distance = math.sqrt((math.pow(varX - playerX, 2)) + (math.pow(varY - playerY, 2)))
        if distance < 27:
            return True
        else:
            return False


    def game_over(self, pts):
        if self.level == 0:
            if pts >= 600:
                self.game_won(pts)
            else:
                self.game_lost(pts)
        if self.level == 1:
            if pts >= 800:
                self.game_won(pts)
            else:
                self.game_lost(pts)
        if self.level == 2:
            if pts >= 1000:
                self.game_won(pts)
            else:
                self.game_lost(pts)


    #threaded function
    #set vertical = true for vertical movement (auto x = 90) false for opposite
    '''
    def rotate_head(self, vertical, positions):
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

    def change_face(self, expression, delay):
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

'''
    def explanation_page(self):
        #self.ros_controller.face_update(1)
        self.screen.fill((255, 255, 255))
        back = Button(self.Back_Arrow, self.Back_Arrow, (20, 20, 100, 70))
        titleSurf, titleRect = self.text_objects('Press an Item to Learn', self.mediumLargeText, self.black)
        titleRect.center = (self.window[0]/2, 130)
        self.screen.blit(titleSurf, titleRect)
        titleSurf2, titleRect2 = self.text_objects('More About It', self.mediumLargeText, self.black)
        titleRect2.center = (self.window[0]/2, 230)
        self.screen.blit(titleSurf2, titleRect2)
        #good/recyclable
        goodSurf, goodRect = self.text_objects('Recyclable Items', self.mediumText, self.black)
        goodRect.center = (self.window[0]/2, self.window[1]/6)
        self.screen.blit(goodSurf, goodRect)
        gBag = pygame.image.load('good_bag.png')
        gBag = pygame.transform.scale(gBag, (100, 100))
        gSoda = pygame.image.load('good_soda.png')
        gSoda = pygame.transform.scale(gSoda, (100, 100))
        plas1 = pygame.image.load('plastic1.png')
        plas1 = pygame.transform.scale(plas1, (100, 100))
        plas2 = pygame.image.load('plastic2.png')
        plas2 = pygame.transform.scale(plas2, (100, 100))
        gBagButton = Button(gBag, gBag, (1 * self.window[0]/5 - 50, self.window[1]/4 - 50, 100, 100))
        gSodaButton = Button(gSoda, gSoda, (2 * self.window[0]/5 - 50, self.window[1]/4 - 50, 100, 100))
        plas1Button = Button(plas1, plas1, (3 * self.window[0]/5 - 50, self.window[1]/4 - 50, 100, 100))
        plas2Button = Button(plas2, plas2, (4 * self.window[0]/5 - 50, self.window[1]/4 - 50, 100, 100))

        #bad/notrecyclable
        badSurf, badRect = self.text_objects('Not Recyclable Items', self.mediumText, self.black)
        badRect.center = (self.window[0]/2, 3 * self.window[1]/7)
        self.screen.blit(badSurf, badRect)
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
        bBananaButton = Button(bBanana, bBanana, (1 * self.window[0]/8 - 50, 43 * self.window[1]/84 - 50, 100, 100))
        bCoreButton = Button(bCore, bCore, (2 * self.window[0]/8 - 50, 43 * self.window[1]/84 - 50, 100, 100))
        bTrashButton = Button(bTrash, bTrash, (3 * self.window[0]/8 - 50, 43 * self.window[1]/84 - 50, 100, 100))
        plas3Button = Button(plas3, plas3, (4 * self.window[0]/8 - 50, 43 * self.window[1]/84 - 50, 100, 100))
        plas6Button = Button(plas6, plas6, (5 * self.window[0]/8 - 50, 43 * self.window[1]/84 - 50, 100, 100))
        bPizzaButton = Button(bPizza, bPizza, (6 * self.window[0]/8 - 50, 43 * self.window[1]/84 - 50, 100, 100))
        bBagButton = Button(bBag, bBag, (7 * self.window[0]/8 - 50, 43 * self.window[1]/84 - 50, 100, 100))


        #special recycling
        neutSurf, neutRect = self.text_objects('Special Collection Items (LVL 3 Only)', self.mediumText, self.black)
        neutRect.center = (self.window[0]/2, 29 * self.window[1]/42)
        self.screen.blit(neutSurf, neutRect)
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
        clothesButton = Button(clothes, clothes, (1 * self.window[0]/6 - 50, 65 * self.window[1]/84 - 50, 100, 100))
        computerButton = Button(computer, computer, (2 * self.window[0]/6 - 50, 65 * self.window[1]/84 - 50, 100, 100))
        medicineButton = Button(medicine, medicine, (3 * self.window[0]/6 - 50, 65 * self.window[1]/84 - 50, 100, 100))
        shreddedPaperButton = Button(shreddedPaper, shreddedPaper, (4 * self.window[0]/6 - 50, 65 * self.window[1]/84 - 50, 100, 100))
        tireButton = Button(tire, tire, (5 * self.window[0]/6 - 50, 65 * self.window[1]/84 - 50, 100, 100))
        loop = True
        while loop:

            gBagButton.generate(self)
            gSodaButton.generate(self)
            plas1Button.generate(self)
            plas2Button.generate(self)
            bBananaButton.generate(self)
            bCoreButton.generate(self)
            bTrashButton.generate(self)
            plas3Button.generate(self)
            plas6Button.generate(self)
            bPizzaButton.generate(self)
            bBagButton.generate(self)
            clothesButton.generate(self)
            computerButton.generate(self)
            medicineButton.generate(self)
            shreddedPaperButton.generate(self)
            tireButton.generate(self)
            back.generate(self)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.screen.fill(self.white)
                    endGame()
                    return
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    touch_status = True
                    if gBagButton.is_pressed(touch_status):
                        self.explanation_template("Paper Bag")
                    if gSodaButton.is_pressed(touch_status):
                        self.explanation_template("Soda Can")
                    if plas1Button.is_pressed(touch_status):
                        self.explanation_template("Type 1 Plastic")
                    if plas2Button.is_pressed(touch_status):
                        self.explanation_template("Type 2 Plastic")
                    if bBananaButton.is_pressed(touch_status):
                        self.explanation_template("Banana Peel")
                    if bCoreButton.is_pressed(touch_status):
                        self.explanation_template("Apple Core")
                    if bTrashButton.is_pressed(touch_status):
                        self.explanation_template("Trash Bags")
                    if plas3Button.is_pressed(touch_status):
                        self.explanation_template("Type 3 Plastic")
                    if plas6Button.is_pressed(touch_status):
                        self.explanation_template("Type 6 Plastic")
                    if bPizzaButton.is_pressed(touch_status):
                        self.explanation_template("Pizza Box")
                    if bBagButton.is_pressed(touch_status):
                        self.explanation_template("Bag of Recyclables")
                    if clothesButton.is_pressed(touch_status):
                        self.explanation_template("Clothes")
                    if computerButton.is_pressed(touch_status):
                        self.explanation_template("Computers")
                    if medicineButton.is_pressed(touch_status):
                        self.explanation_template("Medicine")
                    if shreddedPaperButton.is_pressed(touch_status):
                        self.explanation_template("Shredded Paper")
                    if tireButton.is_pressed(touch_status):
                        self.explanation_template("Tires")
                    if(back.is_pressed(touch_status)):
                        self.intro()


    def  explanation_template(self, item):
        #self.ros_controller.face_update(1)
        back = Button(self.Back_Arrow, self.Back_Arrow, (20, 20, 100, 70))
        self.screen.fill(self.white)
        titleSurf, titleRect = self.text_objects(item, self.largeText, self.black)
        titleRect.center = (self.window[0]/2, 200)
        self.screen.blit(titleSurf, titleRect)
        image = pygame.image.load(self.data["images"][item])
        image = pygame.transform.scale(image, (400, 400))
        self.screen.blit(image, (self.window[0]/2 - 200, self.window[1]/5 * 2 - 200))
        explanation = self.data["explanations"][item]
        expSplit = explanation.split('||')
        textSurf, textRect = self.text_objects(expSplit[0], self.mediumText, self.black)
        textRect.center = (self.window[0]/2, self.window[1] * 2/3)
        if '||' in explanation:
            textSurf2, textRect2 = self.text_objects(expSplit[1], self.mediumText, self.black)
            textRect2.center = (self.window[0]/2, self.window[1] * 2/3 +50)
            self.screen.blit(textSurf2, textRect2)
        self.screen.blit(textSurf, textRect)
        loop = True
        pygame.display.update()
        while loop:
            back.generate(self)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.screen.fill(self.white)
                    endGame()
                    return
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    touch_status = True
                    if(back.is_pressed(touch_status)):
                        self.explanation_page()

    def game_won(self, pts):
        #self.ros_controller.face_update(5)

        game_wn = pygame.image.load('gameWonBkg.png')
        mixer.music.load('game_won.wav')
        #mixer.music.play()
        pause = True
        back = Button(self.Back_Arrow, self.Back_Arrow, (20, 20, 100, 70))

        while pause:
            self.screen.fill((255, 255, 255))

            self.screen.blit(game_wn, (50, self.window[1]/4))
            self.show_score(pts, self.window[0]/2 - 70, 2*self.window[1]/3)
            back.generate(self)
            pygame.display.update()
            for event in pygame.event.get():
                # Quitting the Game by X-ing out self.window
                if event.type == pygame.QUIT:
                    self.screen.fill(self.white)
                    endGame()
                    return
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE or event.type == pygame.MOUSEBUTTONDOWN:
                        self.level_select(self.level)
                    if event.key == pygame.K_SPACE:
                        pts = 0
                        self.game(self.level)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    touch_status = True
                    if(back.is_pressed(touch_status)):
                        self.intro()




    def game_lost(self, pts):
        #self.ros_controller.face_update(3)

        game_lst = pygame.image.load('gameLostBkg.png')
        back = Button(self.Back_Arrow, self.Back_Arrow, (20, 20, 100, 70))
        expImage = pygame.image.load("Explanations.png")
        invexpImage = pygame.image.load("invExplanation.png")
        expImage = pygame.transform.scale(expImage, (750, 222))
        invexpImage = pygame.transform.scale(invexpImage, (750, 222))
        explanation = Button(invexpImage, expImage, (self.window[0]/2 - 750/2, self.window[1] - 450, 750, 222))

        mixer.music.load('game_lose.wav')
        #mixer.music.play()
        pause = True
        self.screen.fill((255, 255, 255))
        while pause:

            self.screen.blit(game_lst, (50, self.window[1]/4))
            self.show_score(pts, self.window[0]/2 - 70, 2*self.window[1]/3)
            explanation.generate(self)
            back.generate(self)

            pygame.display.update()
            for event in pygame.event.get():
                # Quitting the Game by X-ing out self.window
                if event.type == pygame.QUIT:
                    self.screen.fill(self.white)
                    endGame()
                    return
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        self.level_select(self.level)
                    if event.key == pygame.K_SPACE:
                        pts = 0
                        self.game( self.level)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    touch_status = True
                    if(back.is_pressed(touch_status)):
                        self.intro()
                    if(explanation.is_pressed(touch_status)):
                        self.explanation_page()

            pygame.display.update()


    def intro(self):

    #    self.ros_controller.face_update(1)
    #    self.ros_controller.head_update(0)

        playb = pygame.image.load('play.png')
        playb = pygame.transform.scale(playb, (750,222))
        helpb = pygame.image.load('help.png')
        helpb = pygame.transform.scale(helpb, (750,222))
        exitb = pygame.image.load('exit.png')
        exitb = pygame.transform.scale(exitb, (750,222))
        invplayb = pygame.image.load('invplay.png')
        invplayb = pygame.transform.scale(invplayb, (750,222))
        invhelpb = pygame.image.load('invhelp.png')
        invhelpb = pygame.transform.scale(invhelpb, (750,222))
        invexitb = pygame.image.load('invexit.png')
        invexitb = pygame.transform.scale(invexitb, (750,222))
        bmenu = True
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.menu, (0, 0))
        self.screen.blit(self.menu, (0,self.window[1]/2))
        # controller.face_update(4)  # HEEEEEEEEEEEEEERRRREEEEEEEEEEEEE
        playbutton = Button(invplayb, playb, (self.window[0]/2 - 750/2, self.window[1]/4, 750, 222))
        helpbutton = Button(invhelpb, helpb, (self.window[0]/2 - 750/2,  self.window[1]/2, 750, 222))
        quitbutton = Button(invexitb, exitb, (self.window[0]/2 - 750/2,  3*self.window[1]/4, 750, 222))
        TextSurf, TextRect = self.text_objects("Recycle It!", self.largeText, self.blue)
        TextRect.center = (self.window[0]/2,190)
        self.screen.blit(TextSurf,TextRect)
        while bmenu:

            playbutton.generate(self)
            helpbutton.generate(self)
            quitbutton.generate(self)
            for event in pygame.event.get():
                # Quitting the Game by X-ing out self.window
                if event.type == pygame.QUIT:
                    self.screen.fill(self.white)
                    endGame()
                    return
                    pygame.quit()
                    quit()
                touch_status = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    touch_status = True
                    if(playbutton.is_pressed(touch_status)):
                        self.level_select(self.level)
                    if(helpbutton.is_pressed(touch_status)):
                        self.help_screen()
                    if(quitbutton.is_pressed(touch_status)):
                        self.screen.fill(self.white)
                        endGame()
                        return
                        pygame.quit()
                        quit()



            # print(click)




            pygame.display.update()


    def ready(self):
        #self.ros_controller.face_update(2)
        message = ["Ready ", "Ready. ", "Ready.. ", "Ready... ", "Set ", "Set. ", "Set.. ", "Set... ", "GO! " ]
        for i in range(9):
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (-50, self.window[1]/4))
            ready = self.font.render(message[i], True, (0, 0, 0))
            self.screen.blit(ready, (self.window[0]/2 - 50, self.window[1]/2))
            pygame.display.update()
            pygame.time.delay(750)





    def help_screen(self):
        #self.ros_controller.face_update(1)
        helps = pygame.image.load('newhelpbkg.png')
        helps = pygame.transform.scale(helps, (1080, 740))
        menuForHelps = pygame.transform.scale(self.menu, (1080,590))
        bhelp = True
        back = Button(self.Back_Arrow, self.Back_Arrow, (20, 20, 100, 70))
        while bhelp:
            self.screen.fill((255, 255, 255))
            self.screen.blit(menuForHelps, (0,0))
            self.screen.blit(helps, (0, 590))
            self.screen.blit(menuForHelps, (0,1330))
            back.generate(self)
            for event in pygame.event.get():
                # Quitting the Game by X-ing out self.window
                if event.type == pygame.MOUSEBUTTONDOWN:
                    touch_status = True
                    if(back.is_pressed(touch_status)):
                        self.intro()
                if event.type == pygame.QUIT:
                    self.screen.fill(self.white)
                    endGame()
                    return
                    pygame.quit()
                    quit()
                # keystroke check (right/left) and changing val of playerX_change to +/- based on keypress
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.intro()
            pygame.display.update()


    def level_select(self, lvl):
        #self.ros_controller.face_update(1)
        lvl1 = pygame.image.load('lvl1.png')
        lvl1 = pygame.transform.scale(lvl1, (700,222))
        lvl2 = pygame.image.load('lvl2.png')
        lvl2 = pygame.transform.scale(lvl2, (700,222))
        lvl3 = pygame.image.load('lvl3.png')
        lvl3 = pygame.transform.scale(lvl3, (700,222))

        invlvl1 = pygame.image.load('invlvl1.png')
        invlvl1 = pygame.transform.scale(invlvl1, (700,222))
        invlvl2 = pygame.image.load('invlvl2.png')
        invlvl2 = pygame.transform.scale(invlvl2, (700,222))
        invlvl3 = pygame.image.load('invlvl3.png')
        invlvl3 = pygame.transform.scale(invlvl3, (700,222))
        pygame.time.delay(750)
        bmenu = True
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.menu, (0, 0))
        self.screen.blit(self.menu, (0,self.window[1]/2))
        lvl1b = Button(invlvl1, lvl1, (self.window[0]/2 - 750/2, self.window[1]/4, 700, 222))
        lvl2b = Button(invlvl2, lvl2, (self.window[0]/2 - 750/2, self.window[1]/2, 700, 222))
        lvl3b = Button(invlvl3, lvl3, (self.window[0]/2 - 750/2, 3*self.window[1]/4, 700, 222))
        back = Button(self.Back_Arrow, self.Back_Arrow, (20, 20, 100, 70))
        TextSurf, TextRect = self.text_objects("Select a Level", self.largeText, self.blue)
        TextRect.center = (self.window[0]/2,190)
        self.screen.blit(TextSurf,TextRect)
        while bmenu:
            lvl1b.generate(self)
            lvl2b.generate(self)
            lvl3b.generate(self)
            back.generate(self)
            for event in pygame.event.get():
                # Quitting the Game by X-ing out self.window
                if event.type == pygame.QUIT:
                    self.screen.fill(self.white)
                    endGame()
                    return
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.intro()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    touch_status = True
                    if(lvl1b.is_pressed(touch_status)):
                        self.ready()
                        self.game( 0)
                    if(lvl2b.is_pressed(touch_status)):
                        self.ready()
                        self.game(1)
                    if(lvl3b.is_pressed(touch_status)):
                        self.ready()
                        self.game( 2)
                    if(back.is_pressed(touch_status)):
                        self.intro()

            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()


            pygame.display.update()









    # Game Loop
    def game(self, lvl):
        #self.ros_controller.face_update(2)
        # Player + Starting Coordinates
        playerImg = pygame.image.load('character_bin.png')
        playerX = self.window[0]/2
        playerY = 3*self.window[1]/4
        playerX_change = 0
        pts = 0
        old = 0
        seconds = 0
        milliseconds = 0
        lMove = Button(self.empty, self.empty, (0,0, self.window[0]/2, self.window[1]))
        rMove = Button(self.empty, self.empty, (self.window[0]/2,0, self.window[0]/2, self.window[1]))
        back = Button(self.Back_Arrow, self.Back_Arrow, (20, 20, 100, 70))
        mixer.music.load('backgroundmsc.wav')
        #mixer.music.play(-1)

        if(lvl == 1):
            fallspeed = 8
        else:
            fallspeed = 7
        bgame = True
        self.num_of_each = 3
        if(lvl == 2):
            self.num_of_each = 2
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
        lMove.generate(self)
        rMove.generate(self)
        move_speed = 10
        self.screen.fill((255, 255, 255))
        self.clock.tick_busy_loop(60)
        while bgame:
            # RGB Screen Fill - Red, Green, Blue

            back.generate(self)

            self.screen.fill((255, 255, 255))
            self.show_score(pts, self.textX, 100)
            # setting background
            self.screen.blit(self.background, (-50, self.window[1]/4))

            # Checking for events (keypress)
            #for event in pygame.event.get():
                # Quitting the Game by X-ing out self.window

                # keystroke check (right/left) and changing val of playerX_change to +/- based on keypress

            # changes X position of player character

            #listEvents = pygame.event.get()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.screen.fill(self.white)
                    endGame()
                    return
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
                        self.level_select(self.level)



                    if (lMove.is_pressed(touch_status)):
                        playerX_change = -move_speed
                    elif (rMove.is_pressed(touch_status)):
                        playerX_change = move_speed
                if event.type == pygame.MOUSEBUTTONUP:
                    playerX_change = 0



            if keys_pressed[pygame.K_ESCAPE]:
                    self.level_select(self.level)

            playerX += playerX_change
            caphold = 76
            cap = caphold
            randol = random.randint(1, cap)
            if(len(goodImg) <= self.num_of_each and randol == 1):
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
                goodX.append(random.randint(0, self.window[0] - 64))
                goodY.append(random.randint(0, 200) - 300)
                # speed of fall
                goodY_change.append(fallspeed)
                cap = caphold

            elif(len(enemyImg) <= self.num_of_each and randol == 2):
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
                enemyX.append(random.randint(0, self.window[0] - 64))
                enemyY.append(random.randint(0, 200) - 300)
                # speed of fall
                enemyY_change.append(fallspeed)
                cap = caphold
            else:
                cap -= 5


            if(lvl == 2):
                if(len(neutImg) <= self.num_of_each and randol == 3):
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
                    neutX.append(random.randint(0, self.window[0] - 64))
                    neutY.append(random.randint(0, 200) - 300)
                    # speed of fall
                    neutY_change.append(fallspeed)






            # Changes y position of enemies and good objects
            for i in range(len(goodImg)):
                if(i >= len(goodImg)):
                    break
                goodY[i] += goodY_change[i]


                # Checking for collision

                goodCollision = self.isCollision(goodX[i], goodY[i], playerX, playerY)

                # Adding points to score
                if goodCollision:
                    #self.ros_controller.face_update(1)
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
                elif goodY[i] > 3*self.window[1]/4 + 50:
                    del goodX[i]
                    del goodY[i]
                    del goodY_change[i]
                    del goodImg[i]
                    i -= 1
                else:
                    self.screen.blit(goodImg[i], (goodX[i], goodY[i]))

            for i in range(len(enemyImg)):
                if(i >= len(enemyImg)):
                    break
                enemyY[i] += enemyY_change[i]
                badCollision = self.isCollision(enemyX[i], enemyY[i], playerX, playerY)
                if badCollision:
                    #self.ros_controller.face_update(3)
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

                elif enemyY[i]> 3*self.window[1]/4 + 50:
                    del enemyX[i]
                    del enemyY[i]
                    del enemyY_change[i]
                    del enemyImg[i]
                    i -= 1

                else:

                    self.screen.blit(enemyImg[i], (enemyX[i], enemyY[i]))
            if(lvl == 2):
                for i in range(len(neutImg)):
                    if(i >= len(neutImg)):
                        break
                    neutY[i] += neutY_change[i]
                    neutCollision = self.isCollision(neutX[i], neutY[i], playerX, playerY)
                    if neutCollision:
                        #self.ros_controller.face_update(4)
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

                    elif neutY[i] > 3*self.window[1]/4 + 50:
                        del neutX[i]
                        del neutY[i]
                        del neutY_change[i]
                        del neutImg[i]
                        i -= 1

                    else:

                        self.screen.blit(neutImg[i], (neutX[i], neutY[i]))

            # Setting Boundaries for Recycle Bin --> Doesn't go out of game self.window
            if playerX <= 0:
                playerX = 0
            elif playerX >= self.window[0] - 64:
                playerX = self.window[0] - 64

            # Creating Player Object
            self.screen.blit(playerImg, (playerX, playerY))
            back.generate(self)
            # Show Score Function
            self.show_score(pts, self.textX, 100)

            # Timer


            # Updating display
            pygame.display.update()
            if milliseconds > 1000:
                seconds += 1
                milliseconds -= 1000
            if seconds == 6:
                self.game_over(pts)

            print(seconds)
            #print(clock.tick_busy_loop(40))
            #if(clock.tick_busy_loop(40) > 1000):
            #    milliseconds += 50
            #else:
            #clock.tick_busy_loop(60)
            milliseconds += self.clock.tick_busy_loop(60)
            new = pygame.time.get_ticks()
            dif = new - old
            #print(dif)
            old = pygame.time.get_ticks()


class Button:
    def __init__ (self, ac, ic, rectVals):
        self.ac = ac #Active color of button
        self.ic = ic #Inactive color of button
        self.rectAttrs = rectVals #(x, y, w, h) of button

    def generate(self, game):
        x, y, w, h = self.rectAttrs
        mouse = pygame.mouse.get_pos()

        #Check if mouse is on button
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            game.screen.blit(self.ac, (self.rectAttrs[0], self.rectAttrs[1]))

        #Else just show darker button
        else:
            game.screen.blit(self.ic, (self.rectAttrs[0], self.rectAttrs[1]))




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
if __name__ == '__main__':
    game = Recycle_IT()
    game.intro()
    pygame.quit()
    quit()
