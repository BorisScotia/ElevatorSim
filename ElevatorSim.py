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

        # Add Elevator states
        for image in self.elevator_images.elevators:
            image = pygame.transform.scale(image, (100, 100))
            self.elevator.state_images.append(image)

        self.elevator.image = self.elevator.state_images[0]
        self.service_elevator = copy(self.elevator)

        self.elevator.x = 800
        self.elevator.y = 400

        self.service_elevator.x = 1000
        self.service_elevator.y = 400

        

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
                                self.service_elevator.floor_requests.append(1)
                                print(self.service_elevator.floor_requests)
                            self.moving_elevators(self.service_elevator)
                        if 0 < index < 7:
                            if self.elevator_buttons.buttons[index].rect.collidepoint(pos):
                                print(f"Service Elevator to {button.value} ")
                                self.service_elevator.floor_requests.append(button.value)
                                print(self.service_elevator.floor_requests)
                            self.moving_elevators(self.service_elevator)
                        elif index >= 7:
                            if self.elevator_buttons.buttons[index].rect.collidepoint(pos):
                                print(f"Elevator to {button.value} ")
                                self.elevator.floor_requests.append(button.value)
                                print(self.service_elevator.floor_requests)
                            self.moving_elevators(self.elevator)
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
        elevator.image = self.elevator.state_images[2]
        self.update_screen()
        time.sleep(1)
        elevator.image = self.elevator.state_images[3]
        self.update_screen()
        time.sleep(1)
        elevator.image = self.elevator.state_images[1]
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

    def moving_elevators(self, elevator):
        print(elevator.floor_requests)
        if len(elevator.floor_requests) > 0:
            if elevator.floor_requests[0] != elevator.floor:
                for seconds in range(5):
                    elevator.movement()
                    self.update_screen()
                    time.sleep(1)
                elevator.floor = elevator.floor_requests[0]
            del elevator.floor_requests[0]
        # print(elevator.floor_requests)
            elevator.state = "Idle"
            self.update_screen()

            self.open_animation(elevator)
            time.sleep(1)
            self.close_animation(elevator)


if __name__ == '__main__':
    elevator_game = ElevatorSimulator()
    elevator_game.run_game()
