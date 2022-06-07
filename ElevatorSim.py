# Boris Sergienko 781809
# Elevator Simulation Main FIle
# Cumulative Task

# https://ehmatthes.github.io/pcc_2e/beyond_pcc/pygame_sprite_sheets/
# https://github.com/BorisScotia/ElevatorSim



import sys

import pygame

from Elevator_Classes import ElevatorAssets, ElevatorButtons, Elevator

from settings import Settings

from copy import copy

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

        #Add Elevator states
        for image in self.elevator_images.elevators:
            self.elevator.state_images.append(image)

    def run_game(self):
        """Start the main loop for the game."""
        while True:
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
                                print(f"Service Elevator to service (1)")
                                self.elevator.floor_requests.append(button.value)
                        if 0 < index < 7:
                            if self.elevator_buttons.buttons[index].rect.collidepoint(pos):
                                print(f"Service Elevator to {button.value} ")
                                self.elevator.floor_requests.append(button.value)
                        elif index >= 7:
                            if self.elevator_buttons.buttons[index].rect.collidepoint(pos):
                                print(f"Elevator to {button.value} ")
                                self.service_elevator.floor_requests.append(button.value)

                    if self.elevator.rect.collidepoint(pos):
                        print("Yes")
                        self.elevator.image = self.elevator.state_images[2]
                        self.elevator.blitme()


    def update_screen(self):
        self.screen.fill(self.settings.bg_color)

        # Elevator 1
        for index, button in enumerate(self.elevator_buttons.buttons[:7]):
            button.x = index * 100
            button.blitme()

        # Elevator 2
        for index, button in enumerate(self.elevator_buttons.buttons[7::]):
            button.x = index * 100
            button.y = 300
            button.blitme()

        # Elevator states test
        '''self.elevator = self.elevator_images.elevators[0]
        self.elevator.x = 800
        self.elevator.y = 400
        self.elevator.blitme()

        self.service_elevator = self.elevator_images.elevators[0]
        self.service_elevator.x = 1000
        self.service_elevator.y = 400
        self.service_elevator.blitme()'''

        

        if self.elevator.image != self.elevator.state_images[0]:
            self.elevator.image = self.elevator.state_images[0]

        self.service_elevator = copy(self.elevator)



        #Blit the elevators to the screen
        self.elevator.x = 800
        self.elevator.y = 400
        self.elevator.blitme()


        self.service_elevator.x = 1000
        self.service_elevator.y = 400
        self.service_elevator.blitme()

        self.elevator.movement()
        self.service_elevator.movement()
        pygame.display.flip()


if __name__ == '__main__':
    elevator_game = ElevatorSimulator()
    elevator_game.run_game()
