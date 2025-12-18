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
        # self.logo_image = pygame.image.load("Menu_images/LogoMenu.png")
        # self.logo_image = pygame.transform.scale(self.logo_image, ((Config.WIDTH // 2  + 50), (Config.HEIGHT // 2 + 100)))
        self.paper_image = pygame.image.load("Menu_images/paper.png")
        self.paper_image = pygame.transform.scale(self.paper_image, ((Config.WIDTH // 2 ) , (Config.HEIGHT// 2 + 30 )))
        self.instructions_image = pygame.image.load("Menu_images/SpaceBar.png")
        self.menu_font = Config.CURRENT_FONT

        self.play_game_text = self.menu_font.render("PLAY GAME", True, Config.BLACK)
        self.play_game_text_x = (self.m_screen_one.get_width() / 2 - 100) - (self.play_game_text.get_width() / 2 - 200)
        self.play_game_text_y = 75
        self.play_game_rect = self.play_game_text.get_rect(topleft=(self.play_game_text_x, self.play_game_text_y))

        self.instructions_text = self.menu_font.render("INSTRUCTIONS", True, Config.BLACK)
        self.instructions_text_x = (self.m_screen_one.get_width() / 2 - 100) - (self.instructions_text.get_width() / 2 - 220)
        self.instructions_text_y = 160
        self.instructions_rect = self.instructions_text.get_rect(topleft=(self.instructions_text_x ,self.instructions_text_y))

        self.exit_text = self.menu_font.render("EXIT", True, Config.BLACK)
        self.exit_text_x = (self.m_screen_one.get_width() / 2 - 100) - (self.exit_text.get_width()// 2  -150)
        self.exit_text_y = 240
        self.exit_rect = self.exit_text.get_rect(topleft=(self.exit_text_x, self.exit_text_y))

                                        # ^
                                        # |
        # Todo # self.play_game_rect לכתוב את כל המשתנים האלה מחדש ולפרק אותם כמו


        # Todo # self.play_game_rect לכתוב את כל המשתנים האלה מחדש ולפרק אותם כמו
        #TODO # להוסיף רקע למשחק
        #TODO # להויסף לחיצות לכפתורים`
        #TODO #
        #Finger x , y
        self.finger_x = self.play_game_rect.left - Config.FINGER_IMAGE.get_width()  - 10
        self.finger_y = self.play_game_rect.centery - Config.FINGER_IMAGE.get_height() // 2  + 10

    def run(self):
        while self.m_is_menu_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
                        if self.play_game_rect.collidepoint(pygame.mouse.get_pos()):
                            self.m_is_menu_running = False
                        if self.instructions_rect.collidepoint(pygame.mouse.get_pos()):
                            instructions = Instructions(self.m_screen_one)
                            instructions.run()
                        if self.exit_rect.collidepoint(pygame.mouse.get_pos()):
                            return "exit"


                  #TODO לשים את התמונה של האצבע עם חץ
                #if event.type == pygame.KEYDOWN:
                #   if event.key == pygame.K_DOWN:
                #      if self.play_game_rect.collidepoint(pygame.mouse.get_pos()):
                #keys = pygame.key.get_pressed()


                        # if self.m_screen_one.get_width() // 2 - self.play_game_text.get_width() // 2 <= mouse_pos_y <= 200:
                        #     self.m_is_menu_running = False
                        #TODO return "exit"

            self.display_menu()



            mouse_pos = pygame.mouse.get_pos()
            is_hover_on_play_game_rect = self.play_game_rect.collidepoint(mouse_pos)
            is_hover_on_instructions_rect = self.instructions_rect.collidepoint(mouse_pos)
            is_hover_on_exit_rect = self.exit_rect.collidepoint(mouse_pos)

            if is_hover_on_play_game_rect:
                self.finger_y = self.play_game_rect.centery - Config.FINGER_IMAGE.get_height() // 2  + 10
                self.m_screen_one.blit(Config.FINGER_IMAGE, (self.finger_x, self.finger_y))

            if is_hover_on_instructions_rect:
                self.finger_y = self.instructions_rect.centery - Config.FINGER_IMAGE.get_height()//2 + 10
                self.m_screen_one.blit(Config.FINGER_IMAGE, (self.finger_x, self.finger_y))

            if is_hover_on_exit_rect:
                self.finger_y = self.exit_rect.centery - Config.FINGER_IMAGE.get_height() // 2 + 10
                self.m_screen_one.blit(Config.FINGER_IMAGE, (self.finger_x, self.finger_y))

            pygame.display.update()

            Config.CLOCK.tick(Config.FPS)
        return None

    def display_menu(self):

        # Background Color
        # self.m_screen_one.fill((30, 30, 30))
        self.m_screen_one.blit(self.background_image, (0, 0))
        # self.m_screen_one.blit(self.logo_image, (5, 80))
        self.m_screen_one.blit(self.paper_image, (270, 55))

        self.m_screen_one.blit(self.play_game_text, self.play_game_rect)
        self.m_screen_one.blit(self.instructions_text,self.instructions_rect)
        self.m_screen_one.blit(self.exit_text,self.exit_rect)


