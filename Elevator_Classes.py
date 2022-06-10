# Boris Sergienko 781809
# Classes for Elevators

import pygame
import time
from spritesheet import SpriteSheet

pygame.init()


class Elevator:
    """Represents an elevator"""

    def __init__(self, elevator_game):
        self.image = None
        self.state = "Idle"
        self.doors = "Closed"
        self.screen = elevator_game.screen
        self.floor = 1
        self.floor_requests = []
        self.state_images = []

        self.x, self.y = 0, 0

    def blitme(self):
        """Draw the piece at its current location."""
        #self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.x, self.y
        self.screen.blit(self.image, self.rect)

    def movement(self, floor_request):
        if floor_request == None and floor_request == self.floor:
            pass


        elif floor_request == 0 and self.floor != 0 and self.doors == "Closed":
            self.state = "Moving"
            while self.y != 400:
                self.y += 10

        elif floor_request > self.floor and self.doors == "Closed":
            self.state = "Moving"
            self.y -= 10 * floor_request // self.floor


        elif floor_request < self.floor and self.doors == "Closed":
            self.state = "Moving"
            self.y += 10 * (self.floor // floor_request)



class ElevatorAssets:
    def __init__(self, elevator_game):
        self.elevator_game = elevator_game
        self.elevators = []
        self.arrows = []
        self.load_arrows()
        self.load_elevators()

    def load_arrows(self):
        arrow_sprite = SpriteSheet("images/Elevator_Buttons.png")

        #arrow_images = arrow_sprite.load_grid_images()
        pass

    def load_elevators(self):
        elevator_sprite = SpriteSheet("images/Elevators.png")

        elevator_images = elevator_sprite.load_grid_images(4, 1, x_margin=4, x_padding=2, y_margin=2, y_padding=6)

        for image in elevator_images:
            self.elevators.append(image)




class ElevatorButton:
    """Represents one button."""

    def __init__(self, elevator_game):
        self.image = None
        self.value = None
        self.screen = elevator_game.screen

        self.x, self.y = 0, 0

    def blitme(self):
        """Draw the button at its current location."""
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.x, self.y
        self.screen.blit(self.image, self.rect)


class ElevatorButtons:
    def __init__(self, elevator_game):
        self.elevator_game = elevator_game
        self.buttons = []
        self._load_buttons()

    def _load_buttons(self):
        # import sprites
        elevator1_button = SpriteSheet("images/0to6numbers.png")
        elevator2_button = SpriteSheet("images/1to6numbers.png")

        button1_images = elevator1_button.load_grid_images(1, 7, x_margin=1, x_padding=1, y_margin=2, y_padding=11)
        button2_images = elevator2_button.load_grid_images(1, 6, x_margin=1, x_padding=1, y_margin=2, y_padding=11)

        for num in range(7):
            button = ElevatorButton(self.elevator_game)
            button.value = num
            button.image = button1_images[num]
            self.buttons.append(button)

        for num in range(1, 7):
            button = ElevatorButton(self.elevator_game)
            button.value = num
            button.image = button2_images[num - 1]
            self.buttons.append(button)
