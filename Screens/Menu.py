import pygame
from Screens import Game
from pygame import Surface
from Screens.Instructions import Instructions
from settings import Config

pygame.init()

class Menu:
    def __init__(self, i_screen: Surface):
        self.m_screen_one = i_screen
        self.m_is_menu_running = True
        self.show_instructions = False
        self.background_image = pygame.image.load("Menu_images/MenuBG.jpg")
        self.background_image = pygame.transform.scale(self.background_image, (Config.WIDTH, Config.HEIGHT))
        self.paper_image = pygame.image.load("Menu_images/paper.png")
        self.paper_image = pygame.transform.scale(self.paper_image, ((Config.WIDTH // 2), (Config.HEIGHT // 2 + 30)))
        self.instructions_image = pygame.image.load("Menu_images/SpaceBar.png")
        self.menu_font = Config.CURRENT_FONT

        # Texts
        self.play_game_text = self.menu_font.render("PLAY GAME", True, Config.BLACK)
        self.play_game_text_x = (self.m_screen_one.get_width() / 2 - 100) - (self.play_game_text.get_width() / 2 - 200)
        self.play_game_text_y = 75
        self.play_game_rect = self.play_game_text.get_rect(topleft=(self.play_game_text_x, self.play_game_text_y))

        self.instructions_text = self.menu_font.render("INSTRUCTIONS", True, Config.BLACK)
        self.instructions_text_x = (self.m_screen_one.get_width() / 2 - 100) - (self.instructions_text.get_width() / 2 - 220)
        self.instructions_text_y = 160
        self.instructions_rect = self.instructions_text.get_rect(topleft=(self.instructions_text_x, self.instructions_text_y))

        self.exit_text = self.menu_font.render("EXIT", True, Config.BLACK)
        self.exit_text_x = (self.m_screen_one.get_width() / 2 - 100) - (self.exit_text.get_width() // 2 - 150)
        self.exit_text_y = 240
        self.exit_rect = self.exit_text.get_rect(topleft=(self.exit_text_x, self.exit_text_y))

        # Menu items
        self.menu_items = [
            {"text": self.play_game_text, "rect": self.play_game_rect, "action": "play"},
            {"text": self.instructions_text, "rect": self.instructions_rect, "action": "instructions"},
            {"text": self.exit_text, "rect": self.exit_rect, "action": "exit"}
        ]

        self.selected_index = 0  # הכפתור שנבחר כרגע
        self.using_keyboard = False  # False = עכבר, True = מקלדת

        # Pause items
        self.pause_items = [
            {"text": "RESUME", "action": "resume"},
            {"text": "MAIN MENU", "action": "menu"},
            {"text": "EXIT", "action": "exit"}
        ]

        # Finger position
        self.finger_x = self.play_game_rect.left - Config.FINGER_IMAGE.get_width() - 10
        self.finger_y = self.play_game_rect.centery - Config.FINGER_IMAGE.get_height() // 2 + 10

    def run(self):
        while self.m_is_menu_running:
            for event in pygame.event.get():
                # Switch to mouse mode
                if event.type in [pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN]:
                    self.using_keyboard = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        # -------------------------------------------ללמוד אתזה---------------------
                        for item in self.menu_items:
                            if item["rect"].collidepoint(mouse_pos):
                                action = item["action"]

                                if action == "play":
                                    self.m_is_menu_running = False
                                elif action == "instructions":
                                    instructions = Instructions(self.m_screen_one)
                                    instructions.run()
                                elif action == "exit":
                                    return "exit"
                        # -------------------------------------------ללמוד אתזה---------------------
                # Keyboard navigation
                # -------------------------------------------ללמוד אתזה---------------------
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_DOWN, pygame.K_UP]:
                        self.using_keyboard = True
                        if event.key == pygame.K_DOWN:
                            self.selected_index += 1
                            if self.selected_index >= len(self.menu_items):
                                self.selected_index = 0
                        elif event.key == pygame.K_UP:
                            self.selected_index -= 1
                            if self.selected_index < 0:
                                self.selected_index = len(self.menu_items) - 1
                    elif event.key == pygame.K_RETURN:
                        action = self.menu_items[self.selected_index]["action"]
                        if action == "play":
                            self.m_is_menu_running = False
                        elif action == "instructions":
                            instructions = Instructions(self.m_screen_one)
                            instructions.run()
                        elif action == "exit":
                            return "exit"

                if event.type == pygame.QUIT:
                    return "exit"
                # -------------------------------------------ללמוד אתזה---------------------

            self.display_menu()

            mouse_pos = pygame.mouse.get_pos()
            is_hover_on_play_game_rect = self.play_game_rect.collidepoint(mouse_pos)
            is_hover_on_instructions_rect = self.instructions_rect.collidepoint(mouse_pos)
            is_hover_on_exit_rect = self.exit_rect.collidepoint(mouse_pos)
            # -------------------------------------------ללמוד אתזה---------------------
            # הצגת האצבע לפי מצב קלט
            if self.using_keyboard:
                selected_rect = self.menu_items[self.selected_index]["rect"]
                self.finger_y = selected_rect.centery - Config.FINGER_IMAGE.get_height() // 2 + 10
                self.m_screen_one.blit(Config.FINGER_IMAGE, (self.finger_x, self.finger_y))
            else:
                if is_hover_on_play_game_rect:
                    self.finger_y = self.play_game_rect.centery - Config.FINGER_IMAGE.get_height() // 2 + 10
                    self.m_screen_one.blit(Config.FINGER_IMAGE, (self.finger_x, self.finger_y))
                elif is_hover_on_instructions_rect:
                    self.finger_y = self.instructions_rect.centery - Config.FINGER_IMAGE.get_height() // 2 + 10
                    self.m_screen_one.blit(Config.FINGER_IMAGE, (self.finger_x, self.finger_y))
                elif is_hover_on_exit_rect:
                    self.finger_y = self.exit_rect.centery - Config.FINGER_IMAGE.get_height() // 2 + 10
                    self.m_screen_one.blit(Config.FINGER_IMAGE, (self.finger_x, self.finger_y))
            # -------------------------------------------ללמוד אתזה---------------------
            pygame.display.update()
            Config.CLOCK.tick(Config.FPS)

        return None

    def display_menu(self):
        # Background
        self.m_screen_one.blit(self.background_image, (0, 0))
        self.m_screen_one.blit(self.paper_image, (270, 55))

        # Draw texts
        self.m_screen_one.blit(self.play_game_text, self.play_game_rect)
        self.m_screen_one.blit(self.instructions_text, self.instructions_rect)
        self.m_screen_one.blit(self.exit_text, self.exit_rect)
