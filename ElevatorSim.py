# Boris Sergienko 781809
# Elevator Simulation Main FIle
# Cumulative Task

# https://github.com/BorisScotia/ElevatorSim


import sys

import pygame

import threading

from Elevator_Classes import ElevatorAssets, ElevatorButtons, Elevator

from settings import Settings, UIElement, GameState

#Constants
WHITE = (255, 255, 255)
BLUE = (173, 216, 230)
BLACK = (0, 0, 0)


def render_text(text, font_size, text_rgb, bg_rgb):
    """ Returns surface with text written on """
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()


class ElevatorSimulator:

    def __init__(self):
        """Initialize the game, and create resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.game_state = GameState.Title
        self.event = threading.Event()

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
                self.run_game()
            if self.game_state == GameState.Quit:
                sys.exit()

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
        self.quit_btn = UIElement(
            center_position=(600, 700),
            font_size=50,
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text="Quit",
            action=GameState.Quit,
        )

        buttons = pygame.sprite.RenderUpdates(start_btn, self.quit_btn)

        return self.game_loop(buttons)

    def game_loop(self, start_buttons):
        """ Handles game loop until an action is return by a button in the
            buttons sprite renderer.
        """
        while True:
            self.mouse_up = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouse_up = True
            self.screen.fill(BLUE)
            for button in start_buttons:
                ui_action = button.update(pygame.mouse.get_pos(), self.mouse_up)
                if ui_action is not None:
                    return ui_action

            start_buttons.draw(self.screen)
            pygame.display.flip()

    def check_events(self):
        """Handles Events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    for index, button in enumerate(self.elevator_buttons.buttons):
                        if index == 0:
                            if self.elevator_buttons.buttons[index].rect.collidepoint(pos):
                                self.service_elevator.floor_requests.append(1)
                                print(f"Service Elevator to service (1)")
                                if self.service_elevator.state != "Moving":
                                    self.moving_service_elevator(1)


                        if 0 < index < 7:
                            if self.elevator_buttons.buttons[index].rect.collidepoint(pos):
                                self.service_elevator.floor_requests.append(button.value)
                                #print(self.service_elevator.floor_requests)
                                print(f"Service Elevator to {button.value} ")
                                if self.service_elevator.state != "Moving":
                                    self.moving_service_elevator(self.service_elevator.floor_requests[0])

                        if index >= 7:
                            if self.elevator_buttons.buttons[index].rect.collidepoint(pos):
                                self.elevator.floor_requests.append(button.value)
                                print(self.elevator.floor_requests)
                                print(self.service_elevator.floor_requests)
                                print(f"Elevator to {button.value} ")
                                if self.elevator.state != "Moving":
                                    self.moving_elevator(self.elevator.floor_requests[0])
                    if self.quit_btn.rect.collidepoint(pos):
                        sys.exit()

    def draw_buttons(self):
        """Draws buttons"""
        # Elevator 1
        for index, button in enumerate(self.elevator_buttons.buttons[7::]):
            button.x = index * 100
            button.blitme()

        # Elevator 2
        for index, button in enumerate(self.elevator_buttons.buttons[:7]):
            button.x = index * 100
            button.y = 300
            button.blitme()

    def draw_elevator_text(self):
        """Renders text"""
        elevator_text = render_text(
            text=f"Elevator is on floor {self.elevator.floor}, the doors are {self.elevator.doors}",
            font_size= 30,
            text_rgb= BLACK,
            bg_rgb=BLUE
        )
        service_elevator_text = render_text(
            text=f"Service Elevator is on floor {self.service_elevator.floor}, the doors are {self.service_elevator.doors}",
            font_size=30,
            text_rgb=BLACK,
            bg_rgb=BLUE
        )
        elevator_basic_text = render_text(
            text= "Elevator",
            font_size= 40,
            text_rgb= BLACK,
            bg_rgb=BLUE
        )
        service_text = render_text(
            text= "Service Elevator",
            font_size= 40,
            text_rgb= BLACK,
            bg_rgb= BLUE
        )
        self.screen.blit(elevator_text, (5, 200))
        self.screen.blit(service_elevator_text, (15, 550))
        self.screen.blit(elevator_basic_text, (250, 120))
        self.screen.blit(service_text, (200, 420))

    def update_screen(self):
        """Draws everything to screen"""
        self.screen.fill(self.settings.bg_color)
        self.draw_buttons()
        self.draw_elevator_text()
        self.quit_btn.draw(self.screen)
        self.quit_btn.update(pygame.mouse.get_pos(), self.mouse_up)
        # Blit the elevators to the screen
        self.elevator.blitme()
        self.service_elevator.blitme()



        pygame.display.flip()

    def open_animation(self, elevator):
        elevator.doors = "Open"
        elevator.image = elevator.state_images[2]
        self.update_screen()
        self.event.wait(1)
        elevator.image = elevator.state_images[3]
        self.update_screen()
        self.event.wait(1)
        elevator.image = elevator.state_images[1]
        self.update_screen()

    def close_animation(self, elevator):
        elevator.image = self.elevator.state_images[3]
        self.update_screen()
        self.event.wait(1)
        elevator.image = self.elevator.state_images[2]
        self.update_screen()
        self.event.wait(1)
        elevator.image = self.elevator.state_images[0]
        self.update_screen()
        elevator.doors = "Closed"

    def moving_elevator(self, floor_request):
        del self.elevator.floor_requests[0]
        if self.elevator.floor != floor_request:
            for seconds in range(5):
                self.elevator.movement(floor_request)
                self.update_screen()
                self.event.wait(1)
        self.elevator.floor = floor_request
        # print(elevator.floor_requests)
        self.elevator.state = "Idle"
        # self.update_screen()

        self.open_animation(self.elevator)
        self.event.wait(1)
        self.close_animation(self.elevator)

    def moving_service_elevator(self, floor_request):
        del self.service_elevator.floor_requests[0]
        if self.service_elevator.floor != floor_request:
            for seconds in range(5):
                self.service_elevator.movement(floor_request)
                self.update_screen()
                self.event.wait(1)
        self.service_elevator.floor = floor_request

        self.service_elevator.state = "Idle"


        self.open_animation(self.service_elevator)
        self.event.wait(1)
        self.close_animation(self.service_elevator)


if __name__ == '__main__':
    """Runs the game"""
    elevator_game = ElevatorSimulator()
    elevator_game.run_game()
