import pygame
from Screens import Game
from pygame import Surface
from settings import Config

# Initialize pygame for the instructions screen module.
pygame.init()


# Manage the instructions screen lifecycle and interactions.
class Instructions:
    # Prepare assets, text, and UI state for the instructions view.
    def __init__(self, i_screen: Surface):
        self.m_screen_three = i_screen
        self.m_is_instructions_running = True

        # Load visual assets and pre-render static instruction texts.
        self.game_font = Config.CURRENT_FONT
        self.background_image_on_instruction = pygame.image.load(
            "Menu_images/MenuBG.jpg")
        self.instructions_image = pygame.image.load(
            "Instructions_images/keys.png")
        self.instructions_image = pygame.transform.scale(
            self.instructions_image, (Config.WIDTH // 2 - 10, Config.HEIGHT // 2 - 10))
        self.instructions_text = self.game_font.render(
            "USE SPACEBAR AND ARROWS TO PLAY", True, Config.WHITE)
        self.back_to_menu_text = self.game_font.render(
            "BACK TO MENU", True, Config.BLACK)
        self.back_to_menu_rect = self.back_to_menu_text.get_rect(
            center=(Config.WIDTH // 2 + 5, 450))

    # Run the instructions loop and handle exit/back actions.
    def run(self):

        while self.m_is_instructions_running:
            # Process close, keyboard, and mouse input.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "back_to_menu_from_instructions"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.back_to_menu_rect.collidepoint(pygame.mouse.get_pos()):
                            return "back_to_menu_from_instructions"

            # Draw the current instructions frame.
            self.display_game()

            pygame.display.update()
            Config.CLOCK.tick(Config.FPS)

        return None

    # Render instructions screen elements.
    def display_game(self):
        # Draw background and instructional UI.
        self.m_screen_three.blit(self.background_image_on_instruction, (0, 0))
        self.m_screen_three.blit(self.instructions_image, (5, 270))
        self.m_screen_three.blit(self.instructions_text, (10, 300))
        self.m_screen_three.blit(
            self.back_to_menu_text, self.back_to_menu_rect)
