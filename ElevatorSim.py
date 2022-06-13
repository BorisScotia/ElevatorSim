# Boris Sergienko 781809
# Elevator Simulation Main FIle
# Cumulative Task

# https://ehmatthes.github.io/pcc_2e/beyond_pcc/pygame_sprite_sheets/
# https://github.com/BorisScotia/ElevatorSim


import sys

import pygame

import time

from Elevator_Classes import ElevatorAssets, ElevatorButtons, Elevator

from settings import Settings

#from copy import deepcopy


class ElevatorSimulator:

    def __init__(self):
        """Initialize the game, and create resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Elevator Simulator")

        self.elevator_buttons = ElevatorButtons(self)
        self.elevator_images = ElevatorAssets(self)
        self.elevator = Elevator(self)
        self.service_elevator = Elevator(self)

        # Add Elevator states
        #------------MAKE SPRITE GROUP-----------------
        for image in self.elevator_images.elevators:
            image = pygame.transform.scale(image, (100, 100))
            self.elevator.state_images.append(image)
            self.service_elevator.state_images.append(image)

        self.elevator.image = self.service_elevator.image = self.elevator.state_images[0]
        # self.service_elevator = deepcopy(self.elevator)

        self.elevator.x = 800
        self.elevator.y = 400

        self.service_elevator.x = 1000
        self.service_elevator.y = 400


    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self.intro()
            self.update_screen()
            self.check_events()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    for index, button in enumerate(self.elevator_buttons.buttons):
                        if index == 0:
                            if self.elevator_buttons.buttons[index].rect.collidepoint(pos):

                                self.service_elevator.floor_requests.append(1)
                                print(self.elevator.floor_requests)
                                print(self.service_elevator.floor_requests)
                                print(f"Service Elevator to service (1)")
                                if self.service_elevator.state != "Moving":
                                    self.moving_service_elevator(1)


                        if 0 < index < 7:
                            if self.elevator_buttons.buttons[index].rect.collidepoint(pos):
                                self.service_elevator.floor_requests.append(button.value)
                                print(self.service_elevator.floor_requests)
                                print(f"Service Elevator to {button.value} ")
                                if self.service_elevator.state != "Moving":
                                    self.moving_service_elevator(self.service_elevator.floor_requests[0])


                        elif index >= 7:
                            if self.elevator_buttons.buttons[index].rect.collidepoint(pos):
                                self.elevator.floor_requests.append(button.value)
                                print(self.elevator.floor_requests)
                                print(self.service_elevator.floor_requests)
                                print(f"Elevator to {button.value} ")
                                if self.elevator.state != "Moving":
                                    self.moving_elevator(self.elevator.floor_requests[0])
    #https://programmingpixels.com/handling-a-title-screen-game-flow-and-buttons-in-pygame.html
    #Watch this for title screen
    #Make Sprite Groups for elevator and buttons 
    '''def intro(self):
        # white color 
        color = (255,255,255) 
        
        # light shade of the button 
        color_light = (170,170,170) 
        
        # dark shade of the button 
        color_dark = (100,100,100) 
        
        
        # defining a font 
        smallfont = pygame.font.SysFont('Corbel',35) 
        
        # rendering a text written in 
        # this font 
        text = smallfont.render('quit' , True , color) 
        
        while True: 
            
            for ev in pygame.event.get(): 
                
                if ev.type == pygame.QUIT: 
                    pygame.quit() 
                    
                #checks if a mouse is clicked 
                if ev.type == pygame.MOUSEBUTTONDOWN: 
                    
                    #if the mouse is clicked on the 
                    # button the game is terminated 
                    if self.settings.screen_width/2 <= mouse[0] <= self.settings.screen_width/2+140 and self.settings.screen_height/2 <= mouse[1] <= self.settings.screen_height/2+40: 
                        pygame.quit() 
                        
            # fills the screen with a color 
            self.screen.fill((60,25,60)) 
            
            # stores the (x,y) coordinates into 
            # the variable as a tuple 
            mouse = pygame.mouse.get_pos() 
            
            # if mouse is hovered on a button it 
            # changes to lighter shade 
            if self.settings.screen_width/2 <= mouse[0] <= self.settings.screen_width/2+140 and self.settings.screen_height/2 <= mouse[1] <= self.settings.screen_height/2+40: 
                pygame.draw.rect(self.screen,color_light,[self.settings.screen_width/2,self.settings.screen_height/2,140,40]) 
                
            else: 
                pygame.draw.rect(self.screen,color_dark,[self.settings.screen_width/2,self.settings.screen_height/2,140,40]) 
            
            # superimposing the text onto our button 
            self.screen.blit(text , (self.settings.screen_width/2+50,self.settings.screen_height/2))''' 

    def draw_buttons(self):
        # Elevator 1
        for index, button in enumerate(self.elevator_buttons.buttons[7::]):
            button.x = index * 100
            button.blitme()

        # Elevator 2
        for index, button in enumerate(self.elevator_buttons.buttons[:7]):
            button.x = index * 100
            button.y = 300
            button.blitme()

    def update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.draw_buttons()

        # Blit the elevators to the screen
        self.elevator.blitme()
        self.service_elevator.blitme()

        pygame.display.flip()

    def open_animation(self, elevator):
        elevator.image = elevator.state_images[2]
        self.update_screen()
        time.sleep(1)
        elevator.image = elevator.state_images[3]
        self.update_screen()
        time.sleep(1)
        elevator.image = elevator.state_images[1]
        self.update_screen()
        elevator.doors = "Open"

    def close_animation(self, elevator):
        elevator.image = self.elevator.state_images[3]
        self.update_screen()
        time.sleep(1)
        elevator.image = self.elevator.state_images[2]
        self.update_screen()
        time.sleep(1)
        elevator.image = self.elevator.state_images[0]
        self.update_screen()
        elevator.doors = "Closed"

    def moving_elevator(self, floor_request):
        del self.elevator.floor_requests[0]
        if self.elevator.floor != floor_request:
            for seconds in range(5):
                self.elevator.movement(floor_request)
                self.update_screen()
                time.sleep(1)
        self.elevator.floor = floor_request
        # print(elevator.floor_requests)
        self.elevator.state = "Idle"
        #self.update_screen()

        self.open_animation(self.elevator)
        time.sleep(1)
        self.close_animation(self.elevator)

    def moving_service_elevator(self, floor_request):
        del self.service_elevator.floor_requests[0]
        if self.service_elevator.floor != floor_request:
            for seconds in range(5):
                self.service_elevator.movement(floor_request)
                self.update_screen()
                time.sleep(1)
        self.service_elevator.floor = floor_request
        # print(elevator.floor_requests)
        self.service_elevator.state = "Idle"
        #self.update_screen()

        self.open_animation(self.service_elevator)
        time.sleep(1)
        self.close_animation(self.service_elevator)



if __name__ == '__main__':
    elevator_game = ElevatorSimulator()
    elevator_game.run_game()
