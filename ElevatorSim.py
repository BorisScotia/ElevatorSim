# Boris Sergienko 781809
# Elevator Simulation Main FIle
# Cumulative Task

# https://ehmatthes.github.io/pcc_2e/beyond_pcc/pygame_sprite_sheets/
# https://github.com/BorisScotia/ElevatorSim


import sys

import pygame

import time

from Elevator_Classes import ElevatorAssets, ElevatorButtons, Elevator

from settings import Settings, UIElement, GameState

WHITE = (255, 255, 255)
BLUE = (173, 216, 230)


class ElevatorSimulator:

    def __init__(self):
        """Initialize the game, and create resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.game_state = GameState.Title

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Elevator Simulator")

        self.elevator_buttons = ElevatorButtons(self)
        self.elevator_images = ElevatorAssets(self)
        self.elevator = Elevator(self)
        self.service_elevator = Elevator(self)

        # Add Elevator states
        # ------------MAKE SPRITE GROUP-----------------
        for image in self.elevator_images.elevators:
            image = pygame.transform.scale(image, (100, 100))
            self.elevator.state_images.append(image)
            self.service_elevator.state_images.append(image)

        self.elevator.image = self.service_elevator.image = self.elevator.state_images[0]

        self.elevator.x = 800
        self.elevator.y = 400

        self.service_elevator.x = 1000
        self.service_elevator.y = 400
        while True:
            if self.game_state == GameState.Title:
                self.game_state = self.title_screen()
            if self.game_state == GameState.NewGame:
                #Need to fix this------
                #self.game_state = self.play_game()
                self.run_game()
            if self.game_state == GameState.Quit:
                sys.exit()
                return

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self.update_screen()
            self.check_events()

    def title_screen(self):
        start_btn = UIElement(
            center_position=(600, 400),
            font_size=50,
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text="Start",
            action=GameState.NewGame,
        )
        quit_btn = UIElement(
            center_position=(600, 500),
            font_size=50,
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text="Quit",
            action=GameState.Quit,
        )

        buttons = pygame.sprite.RenderUpdates(start_btn, quit_btn)

        return self.game_loop(buttons)

    # def play_game(self):
    #     return_btn = UIElement(
    #         center_position=(150, 750),
    #         font_size=50,
    #         bg_rgb=BLUE,
    #         text_rgb=WHITE,
    #         text="Main Menu",
    #         action=GameState.Title,
    #     )
    #     button = pygame.sprite.RenderUpdates(return_btn)
    #
    #     return self.game_loop(button)

    def game_loop(self, start_buttons):
        """ Handles game loop until an action is return by a button in the
            buttons sprite renderer.
        """
        while True:
            mouse_up = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_up = True
            self.screen.fill(BLUE)
            for button in start_buttons:
                ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
                if ui_action is not None:
                    return ui_action

            start_buttons.draw(self.screen)
            pygame.display.flip()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
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

    # https://programmingpixels.com/handling-a-title-screen-game-flow-and-buttons-in-pygame.html
    # Watch this for title screen
    # Make Sprite Groups for elevator and buttons

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
        # self.update_screen()

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
        # self.update_screen()

        self.open_animation(self.service_elevator)
        time.sleep(1)
        self.close_animation(self.service_elevator)


if __name__ == '__main__':
    elevator_game = ElevatorSimulator()
    elevator_game.run_game()
