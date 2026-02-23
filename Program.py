# import Program2

# Import core modules and screen flows.
import pygame
from Screens.Game import Game
from Screens.Instructions import Instructions
from Screens.Menu import Menu
from settings import Config

# Create the main display surface once and reuse it across screens.
screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))

# Run the application loop and switch between menu and game states.
if __name__ == "__main__":
    # Keep looping so the user can return to the menu after a game session.
    while True:
        # Initialize and run the main menu screen.
        menu = Menu(screen)

        # Handle the menu outcome and exit if requested.
        result_Menu = menu.run()
        if result_Menu == "exit":
            # Exit the loop and close the application.
            break

        # Initialize and run the game screen after leaving the menu.
        game = Game(screen, menu)
        # Handle the game outcome and return to menu only when requested.
        result_Game = game.run()
        if result_Game != "back_to_menu":
            # Stop looping unless the game explicitly asks to return to menu.
            break

        # TODO: Re-check edge cases around exiting from menu/game transitions.
