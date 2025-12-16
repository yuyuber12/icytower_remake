import pygame
from Screens import Game
from pygame import Surface
from settings import Config


class Menu:
    def __init__(self, i_screen: Surface):
        self.m_screen_one = i_screen
        self.m_is_menu_running = True
        self.background_image = pygame.image.load("Menu_images/MenuBG.png")
        self.background_image = pygame.transform.scale(self.background_image, (Config.WIDTH, Config.HEIGHT))
        self.menu_font = Config.CURRENT_FONT
        self.play_game_text = self.menu_font.render("PLAY GAME", True, Config.BLACK)
        self.play_game_text_x = (self.m_screen_one.get_width() / 2 - 100) - (self.play_game_text.get_width() / 2 - 200)
        self.play_game_text_y = 75
        self.play_game_rect = self.play_game_text.get_rect(topleft=(self.play_game_text_x, self.play_game_text_y))

                                        # ^
                                        # |
        # Todo # self.play_game_rect לכתוב את כל המשתנים האלה מחדש ולפרק אותם כמו
        self.instructions_text = self.menu_font.render("INSTRUCTIONS", True, Config.BLACK)
        self.exit_text = self.menu_font.render("EXIT", True, Config.BLACK)
        # Todo # self.play_game_rect לכתוב את כל המשתנים האלה מחדש ולפרק אותם כמו
        #TODO # להוסיף רקע למשחק
        #TODO # להויסף לחיצות לכפתורים
        #TODO #


    def run(self):
        while self.m_is_menu_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
                        if self.play_game_rect.collidepoint(pygame.mouse.get_pos()):
                            self.m_is_menu_running = False
                        # if self.m_screen_one.get_width() // 2 - self.play_game_text.get_width() // 2 <= mouse_pos_y <= 200:
                        #     self.m_is_menu_running = False
                        #TODO return "exit"

            self.display_menu()
            pygame.display.update()
            Config.CLOCK.tick(Config.FPS)
        return None

    def display_menu(self):

        # Background Color
        # self.m_screen_one.fill((30, 30, 30))
        self.m_screen_one.blit(self.background_image, (0, 0))

        self.m_screen_one.blit(self.play_game_text, self.play_game_rect)
        self.m_screen_one.blit(self.instructions_text,
                               ((self.m_screen_one.get_width() / 2 - 100) - (self.play_game_text.get_width() / 2 - 200), 145))
        self.m_screen_one.blit(self.exit_text,
                               ((self.m_screen_one.get_width() / 2- 100) - (self.exit_text.get_width() / 2 - 120), 215))
        


