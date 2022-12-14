import pygame
from PIL import Image
import threading
import random
class Appliance:
    def __init__(self, attrDict):
        valid_keys = ['img_src',        
                      'img_resize',     
                      'coordinates',    
                      'name',           
                      'sliderQuestion1',
                      'sliderQuestion2', 
                      'units',          
                      'unitRate',       
                      'usageRange']     
        for key in valid_keys:
            setattr(self, key, attrDict.get(key)) 
        self.unitAmt = 0  
        self.gallonsUsed = 0 
        self.window_size = (1080, 1920)
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.darker_red = (200, 0, 0)
        self.green = (0, 255, 0)
        self.darker_green = (0, 200, 0)
        self.blue = (50, 89, 250)
        self.darker_blue = (35, 67, 250)
        self.largeText = pygame.font.Font('FreeSansBold.ttf', 100)   
        self.kindalargeText = pygame.font.Font('FreeSansBold.ttf', 70)
        self.mediumText = pygame.font.Font('FreeSansBold.ttf', 48)   
        self.mediumText2 = pygame.font.Font('FreeSansBold.ttf', 24)
        self.smallText =  pygame.font.Font('FreeSansBold.ttf', 16)   
        self.background = pygame.image.load('background.jpg')
        self.background = pygame.transform.scale(self.background, self.window_size)
        self.backgroundRect = self.background.get_rect()
        self.clock = pygame.time.Clock()
        self.FPS = 30
    def generate_img(self, screen, img_dims):
        img = Image.open(self.img_src)
        img_resized = img.resize((img_dims[2], img_dims[3]))
        mode = img_resized.mode
        size = img_resized.size
        data = img_resized.tobytes()
        appliance_img = pygame.image.fromstring(data, size, mode).convert_alpha()
        screen.blit(appliance_img, (img_dims[0], img_dims[1]))
    def generate_usage(self, surface, x, y, font, color=(0,0,0)):
        TextSurf, TextRect = Text().text_objects(self.name + ': ' + '{0:.0f}'.format(self.gallonsUsed) + ' gallons', font, color)
        TextRect.center = (x, y)
        surface.blit(TextSurf, TextRect)
    def menu(self, screen):
        button_w = 100 / 2; button_h = 125 / 2
        button_x = 0.5 * self.window_size[0] - 0.5 * button_w
        up_button_y = 0.5 * self.window_size[1] - .5 * button_h
        down_button_y = up_button_y + (3 * button_h)
        screen.fill(self.white)
        up_button = Button(screen, self.darker_green, self.green, (button_x, up_button_y, button_w, button_h), u'\u2191', self.mediumText)
        down_button = Button(screen, self.darker_red, self.red, (button_x, down_button_y, button_w, button_h), u'\u2193', self.mediumText)
        okay_button = Button(screen, self.darker_blue, self.blue, ((self.window_size[0] - 750)/2, 0.75 * self.window_size[1], 750, 250), 'OK', self.mediumText)
        QuestionSurf1, QuestionRect1 = Text().text_objects(self.sliderQuestion1, self.kindalargeText, self.white)
        QuestionSurf2, QuestionRect2 = Text().text_objects(self.sliderQuestion2, self.kindalargeText, self.white)
        QuestionRect1.center = ((self.window_size[0] / 2), (self.window_size[1] / 8))
        QuestionRect2.center = ((self.window_size[0] / 2), (self.window_size[1] / 8) + 120)
        screen.blit(self.background, self.backgroundRect)
        screen.blit(QuestionSurf1, QuestionRect1)
        screen.blit(QuestionSurf2, QuestionRect2)
        self.generate_img(screen, self.coordinates + self.img_resize)
        pygame.display.update()
        UnitRect = pygame.rect.Rect(0,0,0,0)
        running = True
        while running:
            for event in pygame.event.get():
                print(event)
                if event.type == pygame.QUIT:
                    endGame()
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    touch_status = True
                    if up_button.is_pressed(touch_status):
                        if self.unitAmt < self.usageRange[1]:
                            self.unitAmt += 1
                            self.gallonsUsed = self.unitAmt * self.unitRate
                    if down_button.is_pressed(touch_status):
                        if self.unitAmt > self.usageRange[0]:
                            self.unitAmt -= 1
                            self.gallonsUsed = self.unitAmt * self.unitRate
                    if okay_button.is_pressed(touch_status):
                        return
                else:
                    touch_status = False
            screen.blit(self.background, dest=UnitRect, area=UnitRect)
            UnitSurf, UnitRect = Text().text_objects(str(self.unitAmt) + ' ' + self.units, self.mediumText, self.white)
            UnitRect.topleft = (button_x, up_button_y + 1.5 * button_h)
            screen.blit(UnitSurf, UnitRect)
            up_button.generate()
            down_button.generate()
            okay_button.generate()
            pygame.display.update()
            self.clock.tick(self.FPS)
class Text:
    def __init__(self):
        pass
    def text_objects(self, text, font, color=(0,0,0)):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()
class Button:
    def __init__ (self, surfaceName, ac, ic, rectVals, text, font):
        self.ac = ac 
        self.ic = ic 
        self.rectAttrs = rectVals 
        self.surfaceName = surfaceName
        self.text = text
        self.font = font
    def generate(self):
        x, y, w, h = self.rectAttrs
        mouse = pygame.mouse.get_pos()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self.surfaceName, self.ac, self.rectAttrs)
        else:
            pygame.draw.rect(self.surfaceName, self.ic, self.rectAttrs)
        textSurf, textRect = Text().text_objects(self.text, self.font)
        textRect.center = (x + (w / 2), y + (h / 2))
        self.surfaceName.blit(textSurf, textRect)
    def get_rect(self):
        x, y, w, h = self.rectAttrs
        return pygame.rect.Rect(x, y, w, h)
    def is_pressed(self, touch_status):
        x, y, w, h = self.rectAttrs
        mouse = pygame.mouse.get_pos()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            if touch_status == True:
                return True
            elif touch_status == False:
                return False
        else:
            return False
class WaterCalc:
    def __init__(self, ros_controller):
        pygame.init() 
        self.window_size = (1080, 1920)
        self.FPS = 30
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.darker_red = (200, 0, 0)
        self.green = (0, 255, 0)
        self.darker_green = (0, 200, 0)
        self.blue = (50, 89, 250)
        self.darker_blue = (35, 67, 250)
        self.ros_controller = ros_controller
        self.largeText = pygame.font.Font('FreeSansBold.ttf', 100)   
        self.kindalargeText = pygame.font.Font('FreeSansBold.ttf', 70)
        self.mediumText = pygame.font.Font('FreeSansBold.ttf', 48)   
        self.mediumText2 = pygame.font.Font('FreeSansBold.ttf', 24)
        self.smallText =  pygame.font.Font('FreeSansBold.ttf', 16)   
        self.background = pygame.image.load('background.jpg')
        self.background = pygame.transform.scale(self.background, self.window_size)
        self.backgroundRect = self.background.get_rect()
        self.gameDisplay = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption('Water Calculator')
        self.clock = pygame.time.Clock()
        self.dishwasher_info = {'img_src': 'dishwasher.png', 'img_resize': (256,256), 'coordinates': (self.window_size[0] / 2 - 256/2, self.window_size[1] / 4),
                           'name': 'Dishwasher', 'sliderQuestion1': 'How Often Do You Use the', 'sliderQuestion2' : 'Dishwasher in a Week?',
                           'units': 'times', 'unitRate': 6, 'usageRange':(0, 10)}
        self.washing_machine_info = {'img_src': 'washing_machine.png', 'img_resize': (300,400), 'coordinates': (self.window_size[0] / 2 - 150, self.window_size[1] / 4),
                           'name': 'Washing Machine', 'sliderQuestion1': 'How Often Do You Use the', 'sliderQuestion2' : 'Washing Machine in a Week?',
                           'units': 'times', 'unitRate': 40, 'usageRange':(0, 10)}
        self.shower_info = {'img_src': 'shower.png', 'img_resize': (512 // 2,512 // 2), 'coordinates': (self.window_size[0] / 2 - 512/4, self.window_size[1] / 4),
                           'name': 'Shower',  'sliderQuestion1': 'How Often Do You Use the', 'sliderQuestion2' : 'Shower in a Week?',
                           'units': 'times', 'unitRate': 17.2, 'usageRange':(0, 20)}
        self.toilet_info = {'img_src': 'toilet.png', 'img_resize': (312 // 2,512  // 2), 'coordinates': (self.window_size[0] / 2 - 312/4, self.window_size[1] / 4),
                           'name': 'Toilet',  'sliderQuestion1': 'How Often Do You Use the', 'sliderQuestion2' : 'Toilet in a Week?',
                           'units': 'times', 'unitRate': 1.6, 'usageRange':(0, 30)}
        self.sink_info = {'img_src': 'sink.png', 'img_resize': (728 // 2 ,512 // 2), 'coordinates': (self.window_size[0] / 2 - 728/4, self.window_size[1] / 4),
                           'name': 'Sink',  'sliderQuestion1': 'How many Hours Do You Use', 'sliderQuestion2' : 'the Kitchen Sink in a Week?',
                           'units': 'hours', 'unitRate': 2.2*60, 'usageRange':(0, 168)}
        self.faucet_info = {'img_src': 'faucet.png', 'img_resize': (333 // 2 ,512 // 2), 'coordinates': (self.window_size[0] / 2 - 333//4, self.window_size[1] / 4),
                           'name': 'Faucet', 'sliderQuestion1': 'How many Hours Do You Use ', 'sliderQuestion2' : 'the Faucet in a Week?',
                           'units': 'hours', 'unitRate': 1.5*60, 'usageRange':(0, 168)}
        self.dishwasher = Appliance(self.dishwasher_info)
        self.washing_machine = Appliance(self.washing_machine_info)
        self.shower = Appliance(self.shower_info)
        self.toilet = Appliance(self.toilet_info)
        self.sink = Appliance(self.sink_info)
        self.faucet = Appliance(self.faucet_info)
    def game_intro(self):
        self.ros_controller.face_update(1)
        surface = self.gameDisplay
        button_w = 1.3*750/2; button_h = 1.3*250/2
        button_x = (self.window_size[0] - button_w)/2; help_button_y = 3/6*self.window_size[1]
        button_spacing = 237 / 2   
        play_button_y = 2/6*self.window_size[1]
        quit_button_y = 4/6*self.window_size[1]
        help_button = Button(surface, self.blue, self.darker_blue, (button_x, help_button_y, button_w, button_h), 'Help', self.mediumText)
        play_button = Button(surface, self.green, self.darker_green, (button_x, play_button_y, button_w, button_h), 'Play', self.mediumText)
        quit_button = Button(surface, self.red, self.darker_red, (button_x, quit_button_y, button_w, button_h), 'Quit', self.mediumText)
        help_button_rect = help_button.get_rect()
        play_button_rect = play_button.get_rect()
        quit_button_rect = quit_button.get_rect()
        updateList = [help_button_rect, play_button_rect, quit_button_rect]
        TextSurf, TextRect = Text().text_objects('How Much Water Do', self.largeText, self.white)
        TextSurf2, TextRect2 = Text().text_objects('You Use At Home?', self.largeText, self.white)
        TextRect.center = ((self.window_size[0] / 2), (self.window_size[1] / 6))
        TextRect2.center = ((self.window_size[0] / 2), (self.window_size[1] / 6) + 120 )
        surface.fill(self.white)
        surface.blit(self.background, self.backgroundRect)
        surface.blit(TextSurf, TextRect)
        surface.blit(TextSurf2, TextRect2)
        pygame.display.update()
        touch_status = False 
        running = True
        while running:
            for event in pygame.event.get():
                print(event)
                if event.type == pygame.QUIT:
                    endGame()
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    touch_status = True
                    if quit_button.is_pressed(touch_status):    
                        endGame()
                        pygame.quit()
                        quit()
                    if play_button.is_pressed(touch_status):    
                        self.game_menu(surface)
                    if help_button.is_pressed(touch_status):    
                        self.game_help(surface)
                else:
                    touch_status = False
            help_button.generate()
            play_button.generate()
            quit_button.generate()
            pygame.display.update(updateList)
            self.clock.tick(self.FPS)
    def game_help(self, surface):
        self.ros_controller.face_update(1)
        surface.fill(self.white)
        back_button = Button(surface, self.darker_green, self.green, ((self.window_size[0] - 750) / 2 , 0.75 * self.window_size[1], 750  , 250), 'Back', self.mediumText)
        back_button_rect = back_button.get_rect()
        updateList = [back_button_rect]
        TextSurf, TextRect = Text().text_objects('How to Play:', self.largeText, self.white)
        TextRect.center = ((self.window_size[0] / 2), (self.window_size[1] / 6))
        line_spacing = 75   
        Line1Surf, Line1Rect = Text().text_objects('1.) Select a button under an appliance to', self.mediumText, self.white)
        Line1Rect.center = ((self.window_size[0] / 2), (self.window_size[1] / 4) + 150)
        Line12Surf, Line12Rect = Text().text_objects('set how many times you use it', self.mediumText, self.white)
        Line12Rect.center = ((self.window_size[0] / 2), (self.window_size[1] / 4) + 200)
        Line3Surf, Line3Rect = Text().text_objects('2.) Hit tips to see how you can improve', self.mediumText, self.white)
        Line3Rect.center = ((self.window_size[0] / 2), (self.window_size[1] / 4) + 150 + (2 * line_spacing))
        Line32Surf, Line32Rect = Text().text_objects('your water usage', self.mediumText, self.white)
        Line32Rect.center = ((self.window_size[0] / 2), (self.window_size[1] / 4) + 150 + (2 * line_spacing) + 50)
        Line2Surf, Line2Rect = Text().text_objects('3.) After you are done, tap the \'Back\'', self.mediumText, self.white)
        Line2Rect.center = ((self.window_size[0] / 2), (self.window_size[1] / 4) + 150 + (4 * line_spacing))
        Line22Surf, Line22Rect = Text().text_objects('button to return to the main screen', self.mediumText, self.white)
        Line22Rect.center = ((self.window_size[0] / 2), (self.window_size[1] / 4) + 150 + (4 * line_spacing) + 50)
        surface.fill(self.white)
        surface.blit(self.background, self.backgroundRect)
        surface.blit(TextSurf, TextRect)
        surface.blit(Line1Surf, Line1Rect)
        surface.blit(Line12Surf, Line12Rect)
        surface.blit(Line3Surf, Line3Rect)
        surface.blit(Line32Surf, Line32Rect)
        surface.blit(Line2Surf, Line2Rect)
        surface.blit(Line22Surf, Line22Rect)
        pygame.display.update()
        running = True
        while running:
            for event in pygame.event.get():
                print(event)
                if event.type == pygame.QUIT:
                    endGame()
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    touch_status = True
                    if back_button.is_pressed(touch_status):
                        self.game_intro()
                else:
                    touch_status = False
            back_button.generate()
            pygame.display.update(updateList)
            self.clock.tick(self.FPS)
    def game_tips(self, surface):
        self.ros_controller.face_update(1)
        back_button = Button(surface, self.darker_green, self.green, (0.5 * self.window_size[0] - 150 , 0.80 * self.window_size[1], 750 / 2, 250 / 2), 'Back', self.mediumText)
        back_button_rect = back_button.get_rect()
        updateList = [back_button_rect]
        surface.fill(self.white)
        surface.blit(self.background, self.backgroundRect)
        TextSurf, TextRect = Text().text_objects('Ways to reduce your', self.largeText, self.white)
        TextSurf2, TextRect2 = Text().text_objects('water consumption:', self.largeText, self.white)
        TextRect.center = ((self.window_size[0] / 2), (self.window_size[1] / 6))
        TextRect2.center = ((self.window_size[0] / 2), (self.window_size[1] / 6) + 120)
        surface.blit(TextSurf, TextRect)
        surface.blit(TextSurf2, TextRect2)
        line_spacing = 50   
        limits = [self.dishwasher.unitAmt > 7, self.washing_machine.unitAmt > 3, self.shower.unitAmt > 14,
                  self.toilet.unitAmt > 14, self.sink.unitAmt > 5, self.faucet.unitAmt > 3]
        advice = ['Use the dishwasher less often, settle for | washing with your hands',
                  'Use the washing machine less often, or | invest in a water-efficient one',
                  'Try investing in a water-efficient shower | head',
                  'Try investing in a water-efficient toilet',
                  'Turn off the sink when you finish using it',
                  'Turn off the faucet when you finish using it']
        x, y = self.window_size[0] / 2, (self.window_size[1] / 4) + 150
        count = 1
        if not any(limits):
            self.ros_controller.face_update(5)
            LineSurf, LineRect = Text().text_objects(str(count) + '.) Good Job for using water efficiently!', self.mediumText, self.white)
            LineRect.center = (x, y)
            surface.blit(LineSurf, LineRect)
        else:
            self.ros_controller.face_update(4)
            for i in range(len(limits)):
                flag = limits[i]
                if flag:
                    if '|' not in advice[i]:
                        LineSurf, LineRect = Text().text_objects(str(count) + '.) ' + advice[i], self.mediumText, self.white)
                        LineRect.center = (x, y)
                        surface.blit(LineSurf, LineRect)
                        y += 1.5 * line_spacing
                        count += 1
                    else:
                        LineSurf1, LineRect1 = Text().text_objects(str(count) + '.) ' + advice[i].split('|')[0], self.mediumText, self.white)
                        LineSurf2, LineRect2 = Text().text_objects(advice[i].split('|')[1], self.mediumText, self.white)
                        LineRect1.center = (x, y)
                        LineRect2.center = (x, y + 50)
                        surface.blit(LineSurf1, LineRect1)
                        surface.blit(LineSurf2, LineRect2)
                        y += 2.5 * line_spacing
                        count += 1
        pygame.display.update()
        running = True
        while running:
            for event in pygame.event.get():
                print(event)
                if event.type == pygame.QUIT:
                    endGame()
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    touch_status = True
                    if back_button.is_pressed(touch_status):
                        self.game_menu(surface)
                else:
                    touch_status = False
            back_button.generate()
            pygame.display.update(updateList)
            self.clock.tick(self.FPS)
    def game_menu(self, surface):
        button_w = 325 / 2; button_h = 125 / 2
        row_spacing = button_w + 150
        column_spacing = button_h + 300
        ref_x = 0.125 * self.window_size[0]; ref_y = 0.45 * self.window_size[1]
        dish_dims =   (ref_x, ref_y, button_w, button_h)
        wash_dims =   (ref_x + row_spacing, ref_y, button_w, button_h)
        shower_dims = (ref_x + 2 * row_spacing, ref_y, button_w, button_h)
        toilet_dims = (ref_x, ref_y + column_spacing, button_w, button_h)
        sink_dims =   (ref_x + row_spacing, ref_y + column_spacing, button_w, button_h)
        faucet_dims = (ref_x + 2 * row_spacing, ref_y + column_spacing, button_w, button_h)
        back_dims = (0.575 * self.window_size[0], 0.75 * self.window_size[1], button_w, button_h)
        tips_dims = (0.575 * self.window_size[0] + (row_spacing - 60), 0.75 * self.window_size[1], button_w, button_h)
        quit_dims = (0.575 * self.window_size[0] + 2.0 * (row_spacing - 60), 0.75 * self.window_size[1], button_w, button_h)
        reset_dims = (0.575 * self.window_size[0] + (row_spacing - 60), 0.75 * self.window_size[1] + 1.5 * button_h, button_w, button_h)
        dish_button =   Button(surface, self.green, self.darker_green, dish_dims, self.dishwasher.name, self.smallText)
        wash_button =   Button(surface, self.green, self.darker_green, wash_dims, self.washing_machine.name, self.smallText)
        shower_button = Button(surface, self.green, self.darker_green, shower_dims, self.shower.name, self.smallText)
        toilet_button = Button(surface, self.green, self.darker_green, toilet_dims, self.toilet.name, self.smallText)
        sink_button =   Button(surface, self.green, self.darker_green, sink_dims, self.sink.name, self.smallText)
        faucet_button = Button(surface, self.green, self.darker_green, faucet_dims, self.faucet.name, self.smallText)
        back_button =   Button(surface, self.blue, self.darker_blue, back_dims, 'Back', self.mediumText)
        quit_button =   Button(surface, self.red, self.darker_red, quit_dims, 'Quit', self.mediumText)
        tips_button =   Button(surface, self.green, self.darker_green, tips_dims, 'Tips', self.mediumText)
        reset_button =  Button(surface, self.green, self.darker_green, reset_dims, 'Reset', self.mediumText)
        dish_rect = dish_button.get_rect()
        wash_rect = wash_button.get_rect()
        shower_rect = shower_button.get_rect()
        toilet_rect = toilet_button.get_rect()
        sink_rect = sink_button.get_rect()
        faucet_rect = faucet_button.get_rect()
        back_rect = back_button.get_rect()
        quit_rect = quit_button.get_rect()
        tips_rect = tips_button.get_rect()
        reset_rect = reset_button.get_rect()
        updateList = [dish_rect, wash_rect, shower_rect, toilet_rect,
                      sink_rect, faucet_rect, back_rect, quit_rect, tips_rect, reset_rect]
        TextSurf, TextRect = Text().text_objects('How Much Water Do', self.largeText, self.white)
        TextRect.center = ((self.window_size[0] / 2), (self.window_size[1] / 9))
        TextSurf2, TextRect2 = Text().text_objects('You Use At Home?', self.largeText, self.white)
        TextRect2.center = ((self.window_size[0] / 2), (self.window_size[1] / 9) + 120)
        TotalSurf, TotalRect = Text().text_objects('Total Water Usage:', self.mediumText, self.white)
        TotalRect.center = ((1/4 * self.window_size[0]), (5/7 *self.window_size[1] ))
        gallon_sum = self.dishwasher.gallonsUsed + self.washing_machine.gallonsUsed + self.shower.gallonsUsed + self.toilet.gallonsUsed + self.sink.gallonsUsed + self.faucet.gallonsUsed
        SumSurf, SumRect = Text().text_objects('Total: ' + '{0:.0f}'.format(gallon_sum) + ' gallons per week', self.mediumText, self.white)
        SumRect.center = ((1/4 * self.window_size[0]) + 80, (5/7 *self.window_size[1]  + 450))
        surface.fill(self.white)
        surface.blit(self.background, self.backgroundRect)
        surface.blit(TextSurf, TextRect)
        surface.blit(TextSurf2, TextRect2)
        surface.blit(TotalSurf, TotalRect)
        surface.blit(SumSurf, SumRect)
        self.dishwasher.generate_usage(surface, (1/4 * self.window_size[0]), (5/7 *self.window_size[1]  + 100), self.mediumText2, self.white)
        self.washing_machine.generate_usage(surface, (1/4 * self.window_size[0]), (5/7 *self.window_size[1]  + 150), self.mediumText2, self.white)
        self.shower.generate_usage(surface, (1/4 * self.window_size[0]), (5/7 *self.window_size[1]  + 200), self.mediumText2, self.white)
        self.toilet.generate_usage(surface,(1/4 * self.window_size[0]), (5/7 *self.window_size[1]  + 250), self.mediumText2, self.white)
        self.sink.generate_usage(surface, (1/4 * self.window_size[0]), (5/7 *self.window_size[1]  + 300), self.mediumText2, self.white)
        self.faucet.generate_usage(surface, (1/4 * self.window_size[0]), (5/7 *self.window_size[1] + 350), self.mediumText2, self.white)
        self.dishwasher.generate_img(surface, (ref_x - 20, ref_y - 225, 200, 200))
        self.washing_machine.generate_img(surface, (ref_x + row_spacing + 5, ref_y - 225, 150, 200))
        self.shower.generate_img(surface, (ref_x + 2 * row_spacing + 20, ref_y - 225, 200, 200))
        self.toilet.generate_img(surface, (ref_x + 20, ref_y + column_spacing - 225, 120, 200))
        self.sink.generate_img(surface, (ref_x + row_spacing - 30, ref_y + column_spacing - 225, 280, 200))
        self.faucet.generate_img(surface, (ref_x + 2 * row_spacing + 20, ref_y + column_spacing - 225, 120, 200))
        pygame.display.update()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    endGame()
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    touch_status = True
                    if dish_button.is_pressed(touch_status):
                        self.dishwasher.menu(surface)
                        self.game_menu(surface)
                    if wash_button.is_pressed(touch_status):
                        self.washing_machine.menu(surface)
                        self.game_menu(surface)
                    if shower_button.is_pressed(touch_status):
                        self.shower.menu(surface)
                        self.game_menu(surface)
                    if toilet_button.is_pressed(touch_status):
                        self.toilet.menu(surface)
                        self.game_menu(surface)
                    if sink_button.is_pressed(touch_status):
                        self.sink.menu(surface)
                        self.game_menu(surface)
                    if faucet_button.is_pressed(touch_status):
                        self.faucet.menu(surface)
                        self.game_menu(surface)
                    if back_button.is_pressed(touch_status):
                        self.game_intro()
                    if tips_button.is_pressed(touch_status):
                        self.game_tips(surface)
                    if reset_button.is_pressed(touch_status):
                        self.dishwasher.gallonsUsed = 0
                        self.washing_machine.gallonsUsed = 0
                        self.shower.gallonsUsed = 0
                        self.toilet.gallonsUsed = 0
                        self.sink.gallonsUsed = 0
                        self.faucet.gallonsUsed = 0
                        self.dishwasher.unitAmt = 0
                        self.washing_machine.unitAmt = 0
                        self.shower.unitAmt = 0
                        self.toilet.unitAmt = 0
                        self.sink.unitAmt = 0
                        self.faucet.unitAmt = 0
                        self.game_menu(surface)
                    if quit_button.is_pressed(touch_status):
                        endGame()
                        pygame.quit()
                        quit()
            dish_button.generate()
            wash_button.generate()
            shower_button.generate()
            toilet_button.generate()
            sink_button.generate()
            faucet_button.generate()
            back_button.generate()
            quit_button.generate()
            tips_button.generate()
            reset_button.generate()
            pygame.display.update(updateList)
if __name__ == '__main__':
    pygame.quit()
    wc = WaterCalc()
    wc.game_intro()
    quit()
    main()