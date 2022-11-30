import pygame
from pygame import mixer
import time
import sys
import random
import threading
sys.path.append("../")
import error

class Button:
    def __init__ (self, ac, ic, rectVals):
        self.ac = ac #Active color of button
        self.ic = ic #Inactive color of button
        self.rectAttrs = rectVals #(x, y, w, h) of button
    def generate(self, screen):
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

class Level:
    def __init__(self, window_size):
        self.window_size = window_size
        self.font = pygame.font.Font('Bubblegum.ttf', 32)
        self.game_screen_vshift = (self.window_size[1]-634)/2
        self.game_screen_hshift = (self.window_size[0]-926)/2
        self.background = None
        self.objs = []
        self.flipped = []
        self.hints = []
        self.isTimer = False
        self.timer = 0

    def setBackground(self, bg):
        self.background = bg

    def setTimer(self, timer):
        self.isTimer = True
        self.timer = timer

    def addObj(self, obj, flippedobj, x_pos, y_pos, x_off, y_off, hint):
        x_pos += self.game_screen_hshift
        y_pos += self.game_screen_vshift
        xuplimit = x_pos + x_off
        xlowlimit = x_pos - 10
        yuplimit = y_pos + y_off
        ylowlimit = y_pos - 10

        self.objs.append([obj,flippedobj, x_pos, y_pos, xuplimit, xlowlimit, yuplimit, ylowlimit])
        self.hints.append(hint)
        self.flipped.append(0)

    def run(self, screen, menu, Back_Arrow, hintp):

        start_tick = pygame.time.get_ticks()
        self.flipped = [0 for _ in self.objs]
        hint = self.font.render(" ", True, (0, 0, 0))
        mixer.music.load('backgroundmsc.wav')
        mixer.music.play(-1)
        screen.fill((255, 255, 255))
        screen.blit(menu, (0, 0))
        screen.blit(menu, (0,self.window_size[1]/2))
        back = Button(Back_Arrow, Back_Arrow, (10, 10, 100, 80))

        back.generate(screen)

        pygame.display.update()

        while True:
            screen.blit(self.background, (self.game_screen_hshift, self.game_screen_vshift))
            screen.blit(Back_Arrow, (10, 10))
            screen.blit(hint, (50+self.game_screen_hshift,85+self.game_screen_vshift))
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            print(mouse)

            for event in pygame.event.get():
                # Quitting the Game by X-ing out Window
                if event.type == pygame.QUIT:
                    endGame()
                    pygame.quit()
                    quit()
                # keystroke check (right/left) and changing val of playerX_change to +/- based on keypress
                #if event.type == pygame.KEYDOWN:
                #    if event.key == pygame.K_ESCAPE:
                #        level_select()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back.is_pressed(True):
                        return "Back"

            for num, object in enumerate(self.objs):
                screen.blit(object[0 + self.flipped[num]], (object[2], object[3]))
                if object[-4] > mouse[0] > object[-3] and object[-2] > mouse[1] > object[-1] and click[0] == 1:
                    #screen.blit(self.background, (0, 0))
                    #back.generate()
                    pygame.display.update(pygame.Rect(object[-3], object[-1], object[-4]-object[-3], object[-2]-object[-1]))
                    self.flipped[num] = 1

            else:
                screen.blit(hintp, (815+self.game_screen_hshift, 25+self.game_screen_vshift))
                if 900+self.game_screen_hshift > mouse[0] > 815+self.game_screen_hshift and 100+self.game_screen_vshift > mouse[1] > 25+self.game_screen_vshift:
                    screen.blit(hintp, (815+self.game_screen_hshift, 25+self.game_screen_vshift))
                    if click[0] == 1:
                        for objnum, flip in enumerate(self.flipped):
                            if not flip:
                                hint = self.font.render(self.hints[objnum], True, (0, 0, 0))
                                break
                else:
                    screen.blit(hintp, (815+self.game_screen_hshift, 25+self.game_screen_vshift))


            if self.isTimer:
                    time = self.timer
                    seconds_elapsed = (pygame.time.get_ticks()-start_tick)//1000
                    time_left = time-seconds_elapsed
                    time_text = self.font.render(str(time_left), True, (0, 0, 0))
                    screen.blit(time_text, (5+self.game_screen_hshift, 85+self.game_screen_vshift))
                    if time_left <= 0:
                        return "Loss"

            if all(flip == 1 for flip in self.flipped):
                return "Win"
            pygame.display.update()


class WhatsWrong:
    def __init__(self, ros_controller):
        pygame.init()
        self.window_size = (1080, 1920)
        self.screen = pygame.display.set_mode(self.window_size)

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
        self.ros_controller = ros_controller
        self.largeText = pygame.font.Font('FreeSansBold.ttf', 70)   #Large text, ideal for headings (normally 64)
        self.mediumText = pygame.font.Font('FreeSansBold.ttf', 48)   #Medium text, ideal for subheadings
        self.smallText =  pygame.font.Font('FreeSansBold.ttf', 14)   #Small text, ideal for small buttons

        # backgrounds
        self.Back_Arrow = pygame.image.load('Back_Arrow.png')
        self.Back_Arrow = pygame.transform.scale(self.Back_Arrow, (100,70))
        self.classroomlvl = pygame.image.load('classroomlvl.png')
        self.kitchenlvl = pygame.image.load('kitchenlvl.png')
        self.bedroomlvl = pygame.image.load('bedroomlvl.png')
        self.menu = pygame.image.load('menubkg.png')
        self.menu = pygame.transform.scale(self.menu, (self.window_size[0], self.window_size[1]//2))
        self.helps = pygame.image.load('helpback.png')
        self.helpbkg = pygame.image.load('helpbkglegit.png')
        self.helpbkg = pygame.transform.scale(self.helpbkg, self.window_size)
        self.helps = pygame.transform.scale(self.helps, (926, 634))
        self.gamewon = pygame.image.load('winner.png')
        self.gamelost = pygame.image.load('loser.png')

        # Background Music
        mixer.music.load('backgroundmsc.wav')

        # kitchen level items
        self.can = pygame.image.load('can.png')
        self.looseplant = pygame.image.load('loose_plant.png')
        self.papertowel = pygame.image.load('paper_towel.png')
        self.pottedplant = pygame.image.load('potted_plant.png')
        #recyclingarrow = pygame.image.load('recycling_arrow.png')
        self.recyclingarrow = pygame.image.load('paper_towel_recycling.png')
        self.runningfaucet = pygame.image.load('running_faucet.png')
        self.towels = pygame.image.load('towels.png')
        self.tick = pygame.image.load('tick.png')

        # Buttons
        self.playb = pygame.image.load('playbtn.png')
        self.playb = pygame.transform.scale(self.playb, (750,222))
        self.helpb = pygame.image.load('helpbtn.png')
        self.helpb = pygame.transform.scale(self.helpb, (750,222))
        self.exitb = pygame.image.load('quitbtn.png')
        self.exitb = pygame.transform.scale(self.exitb, (750,222))
        self.lvl1 = pygame.image.load('lvl1.png')
        self.lvl1 = pygame.transform.scale(self.lvl1, (750,222))
        self.lvl2 = pygame.image.load('lvl2.png')
        self.lvl2 = pygame.transform.scale(self.lvl2, (750,222))
        self.lvl3 = pygame.image.load('lvl3.png')
        self.lvl3 = pygame.transform.scale(self.lvl3, (750,222))
        self.invplayb = pygame.image.load('invplayb.png')
        self.invplayb = pygame.transform.scale(self.invplayb, (750,222))
        self.invhelpb = pygame.image.load('invhelpb.png')
        self.invhelpb = pygame.transform.scale(self.invhelpb, (750,222))
        self.invexitb = pygame.image.load('invquitb.png')
        self.invexitb = pygame.transform.scale(self.invexitb, (750,222))
        self.invlvl1 = pygame.image.load('invlvl1.png')
        self.invlvl1 = pygame.transform.scale(self.invlvl1, (750,222))
        self.invlvl2 = pygame.image.load('invlvl2.png')
        self.invlvl2 = pygame.transform.scale(self.invlvl2, (750,222))
        self.invlvl3 = pygame.image.load('invlvl3.png')
        self.invlvl3 = pygame.transform.scale(self.invlvl3, (750,222))

        self.hintp = pygame.image.load('hint.png')
        self.blank = pygame.image.load('blank.png')

        # classroom level items
        self.closedcurtains = pygame.image.load('cosed_curtains.png')
        self.opencurtains = pygame.image.load('open_curtains.png')
        self.trash = pygame.image.load('trash.png')
        self.compost = pygame.image.load('compost.png')
        self.laptopoff = pygame.image.load('laptop_off.png')
        self.laptopon = pygame.image.load('laptop_on.png')
        self.papertrash = pygame.image.load('paper_trash.png')
        self.paperrecycling = pygame.image.load('paper_recycling.png')

        # bedroom level items
        self.openwindow = pygame.image.load('open_window.png')
        self.closedwindow = pygame.image.load('closed_window.png')
        self.loosepaper = pygame.image.load('loose_paper.png')
        self.whiteboard = pygame.image.load('whiteboard.png')
        self.waterbottle = pygame.image.load('waterbottle.png')
        self.reusablewb = pygame.image.load('reusable_water_bottle.png')
        self.ipad = pygame.image.load('ipad.png')
        self.lighton = pygame.image.load('light_on.png')
        self.lightoff = pygame.image.load('light_off.png')

        pygame.display.set_caption("What's Wrong With The Room?")
        self.icon = pygame.image.load('logo.png')
        pygame.display.set_icon(self.icon)

        self.font = pygame.font.Font('Bubblegum.ttf', 32)

        self.level1 = Level(self.window_size)
        self.level1.setBackground(self.classroomlvl)
        self.level1.addObj(self.closedcurtains, self.opencurtains, 750, 100, 100, 130,"Hint: Always try to use Natural Sunlight")
        self.level1.addObj(self.papertrash, self.paperrecycling, 280, 320, 100, 130, "Hint: Always Recycle Paper")
        self.level1.addObj(self.trash, self.compost, 58, 265, 107, 145, "Hint: Turn food waste into Compost")
        self.level1.addObj(self.laptopon, self.laptopoff, 440, 315, 110, 65,"Hint: Turn off things you aren't using")

        self.level2 = Level(self.window_size)
        self.level2.setBackground(self.bedroomlvl)
        self.level2.addObj(self.blank, self.ipad, 540, 370, 55, 55, "Hint: Turn off things you aren't using")
        self.level2.addObj(self.loosepaper,self.whiteboard, 240, 365, 80, 45, "Hint: Recycle Paper as much as Possible")
        self.level2.addObj(self.waterbottle, self.reusablewb, 20, 420, 40, 80, "Hint: Use Very Little Plastic (Bottles, Bags, etc.) ")
        self.level2.addObj(self.openwindow, self.closedwindow,650, 120, 170, 170, "Hint: Close Windows to Keep Your House Warm/Cold")
        self.level2.addObj(self.lighton, self.lightoff, 290, 240, 55, 50, "Hint: Turn off things you aren't using")

        self.level3 = Level(self.window_size)
        self.level3.setBackground(self.kitchenlvl)
        self.level3.setTimer(90)
        self.level3.addObj(self.papertowel, self.recyclingarrow, 550, 540, 75, 65, "Hint: Use Things made from Recycled Materials")
        self.level3.addObj(self.papertowel, self.towels, 375, 325, 75, 55, "Hint: Avoid Using Paper as much as you can")
        self.level3.addObj(self.can, self.pottedplant, 640, 305, 40, 65, "Hint: Create your own projects with recyclables ")
        self.level3.addObj(self.runningfaucet, self.blank, 265, 300, 75, 55, "Hint: Don't leave the water running")
        self.level3.addObj(self.blank, self.tick, 5, 345, 155, 190, "Hint: Turn off/Close things you aren't using")



    def text_objects(self, text, font, color=(0,0,0)):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()



    def intro(self):

        mixer.music.load('backgroundmsc.wav')
        mixer.music.play(-1)
        #controller.face_update(4)  # HHHHHHHHHHHHHHEEEEEEEEEEEEEEERRRRRRRRRRRRRRRREEEEEEEEEEEEEE
    #    controller.head_update([90,90])
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.menu, (0, 0))
        self.screen.blit(self.menu, (0,self.window_size[1]/2))
        playbutton = Button(self.invplayb, self.playb, (self.window_size[0]/2 - 750/2, self.window_size[1]/4, 750, 222))
        helpbutton = Button(self.invhelpb, self.helpb, (self.window_size[0]/2 - 750/2,  self.window_size[1]/2, 750, 222))
        quitbutton = Button(self.invexitb, self.exitb, (self.window_size[0]/2 - 750/2,  3*self.window_size[1]/4, 750, 222))
        TextSurf, TextRect = self.text_objects("What's Wrong with the Room?", self.largeText, self.black)
        TextRect.center = (self.window_size[0]/2,190)
        self.screen.blit(TextSurf,TextRect)
        bmenu = True
        while bmenu:

            playbutton.generate(self.screen)
            helpbutton.generate(self.screen)
            quitbutton.generate(self.screen)
            for event in pygame.event.get():
                # Quitting the Game by X-ing out Window
                if event.type == pygame.QUIT:
                    endGame()
                    pygame.quit()
                    quit()

                # if event.type == pygame.MOUSEBUTTONUP:
                #     if 360 + 220 > mouse[0] > 360 and 80 + 70 > mouse[1] > 80:
                #         level_select()
                #     elif 360 + 220 > mouse[0] > 360 and 170 + 70 > mouse[1] > 170:
                #         help_screen()
                #     elif 360 + 220 > mouse[0] > 360 and 260 + 70 > mouse[1] > 260:
                #         pygame.quit()
                #         quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    touch_status = True
                    if(playbutton.is_pressed(touch_status)):
                        self.level_select(self.screen)
                    if(helpbutton.is_pressed(touch_status)):
                        self.help_screen(self.screen)
                    if(quitbutton.is_pressed(touch_status)):
                        endGame()
                        pygame.quit()
                        quit()



            # mouse = pygame.mouse.get_pos()
            # click = pygame.mouse.get_pressed()
            # print(click)
            # if 360 + 220 > mouse[0] > 360 and 80 + 70 > mouse[1] > 80:
            #     screen.blit(invplayb, (360, 80))
            # else:
            #     screen.blit(playb, (360, 80))
            #
            # if 360 + 220 > mouse[0] > 360 and 170 + 70 > mouse[1] > 170:
            #     screen.blit(invhelpb, (360, 170))
            # else:
            #     screen.blit(helpb, (360, 170))
            #
            # if 360 + 220 > mouse[0] > 360 and 260 + 70 > mouse[1] > 260:
            #     screen.blit(invexitb, (360, 260))
            #
            # else:
            #     screen.blit(exitb, (360, 260))

            pygame.display.update()


    def help_screen(self, screen):
        mixer.music.load('backgroundmsc.wav')
        mixer.music.play(-1)
        bhelp = True
        back = Button(self.Back_Arrow, self.Back_Arrow, (10, 10, 100, 80))
        while bhelp:

            screen.fill((255, 255, 255))
            screen.blit(self.helpbkg, (0,0))
            #screen.blit(help_message, (0, 0))
            back.generate(screen)
            pygame.display.update()

            for event in pygame.event.get():
                # Quitting the Game by X-ing out Window
                if event.type == pygame.QUIT:
                    endGame()
                    pygame.quit()
                    quit()
                # keystroke check (right/left) and changing val of playerX_change to +/- based on keypress
                if event.type == pygame.MOUSEBUTTONDOWN:
                    touch_status = True
                    if(back.is_pressed(touch_status)):
                        self.intro()
            pygame.display.update()


    def level_select(self, screen):
        #pygame.time.delay(720)
        bmenu = True
        mixer.music.load('backgroundmsc.wav')
        mixer.music.play(-1)
        screen.fill((255, 255, 255))
        screen.blit(self.menu, (0, 0))
        screen.blit(self.menu, (0,self.window_size[1]/2))
        back = Button(self.Back_Arrow, self.Back_Arrow, (10, 10, 100, 80))
        lvl1b = Button(self.invlvl1, self.lvl1, (self.window_size[0]/2 - 750/2, self.window_size[1]/4, 750, 222))
        lvl2b = Button(self.invlvl2, self.lvl2, (self.window_size[0]/2 - 750/2, self.window_size[1]/2, 750, 222))
        lvl3b = Button(self.invlvl3, self.lvl3, (self.window_size[0]/2 - 750/2, 3*self.window_size[1]/4, 750, 222))
        back.generate(screen)
        pygame.display.update()
        while bmenu:
            # screen.fill((255, 255, 255))
            # screen.blit(menu, (0, 0))
            for event in pygame.event.get():

                lvl1b.generate(screen)
                lvl2b.generate(screen)
                lvl3b.generate(screen)
                back.generate(screen)

                # Quitting the Game by X-ing out Window
                if event.type == pygame.QUIT:
                    endGame()
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back.is_pressed(True):
                        self.intro()

                if event.type == pygame.MOUSEBUTTONUP:
                    touch_status = True
                    state = None
                    if(lvl1b.is_pressed(touch_status)):
                        state = self.level1.run(screen, self.menu, self.Back_Arrow, self.hintp)
                    if(lvl2b.is_pressed(touch_status)):
                        state = self.level2.run(screen, self.menu, self.Back_Arrow, self.hintp)
                    if(lvl3b.is_pressed(touch_status)):
                        state = self.level3.run(screen, self.menu, self.Back_Arrow, self.hintp)

                    if (state == "Back"):
                        self.intro()
                    elif (state == "Win"):
                        self.gamewin(screen)
                    elif (state == "Back"):
                        self.gamelose(screen)




                pygame.display.update()


    def gamewin(self, screen):
        #face = random.randint(1, 3)  # HEEEEEEEEEEEEEEEEEERRRRRRRRRRRRRRRRRREEEEEEEEEEEEEE
        #controller.face_update(face)
        # These commands won't over write themselves right? like if i say these three in a row
        # it'll hit all of the positions before going back to [90,90]?
        # controller.head_update([90, 45])
        # controller.head_update([90, 135])
        # controller.head_update([90, 90])
        #rotate=threading.Thread(target=rotate_head, args=(True, [45, 135, 90]))
        #rotate.start()
        bgame = True
        mixer.music.load('game_won.wav')
        mixer.music.play()
        back = Button(self.Back_Arrow, self.Back_Arrow, (10, 10, 100, 80))
        game_screen_vshift = (self.window_size[1]-634)/2
        game_screen_hshift = (self.window_size[0]-926)/2

        pygame.display.update()
        while bgame:
            #pygame.time.delay(60)
            screen.fill((255, 255, 255))
            screen.blit(self.gamewon, (game_screen_hshift, game_screen_vshift))
            back.generate(screen)
            for event in pygame.event.get():
                # Quitting the Game by X-ing out Window
                if event.type == pygame.QUIT:
                    endGame()
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back.is_pressed(True):
                        self.level_select(screen)
                #if event.type == pygame.KEYDOWN:
                #    if event.key == pygame.K_ESCAPE:
                #        level_select()
            pygame.display.update()
            #test

    def gamelose(self, screen):

        bgame = True
        mixer.music.load('game_lose.wav')
        mixer.music.play()
        back = Button(self.Back_Arrow, self.Back_Arrow, (10, 10, 100, 80))
        game_screen_vshift = (self.window_size[1]-634)/2
        game_screen_hshift = (self.window_size[0]-926)/2
        while bgame:
            screen.fill((255, 255, 255))
            screen.blit(self.gamelost, (game_screen_hshift, 50+game_screen_vshift))
            back.generate(screen)
            for event in pygame.event.get():
                # Quitting the Game by X-ing out Window
                if event.type == pygame.QUIT:
                    endGame()
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back.is_pressed(True):
                        self.level_select(screen)
                #if event.type == pygame.KEYDOWN:
                #    if event.key == pygame.K_ESCAPE:
                #        level_select()
            pygame.display.update()

if __name__ == '__main__':
    game = WhatsWrong()
    game.intro()
    pygame.quit()
    quit()
