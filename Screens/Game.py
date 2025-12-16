import random

import pygame
from pygame import Surface

from DataModels.Platforms import Platforms
from DataModels.Player import Player
from settings import Config



pygame.init()

# END_GAME = Menu.m_is_menu_runnin ???


LARGE_FONT = pygame.font.SysFont('Corbel', 60, bold=True)

class Game:
    def __init__(self, i_screen: Surface , menu):
        self.m_screen_two: Surface = i_screen
        self.menu = menu
        self.keys = pygame.key.get_pressed()
        self.m_is_game_running = True
        self.is_paused = False
        self.game_font = Config.CURRENT_FONT
        self.overlay = pygame.image.load("Menu_images/MenuBG.jpg")
        self.pause_text = self.game_font.render("PAUSED", True, Config.BLACK)

        self.pause_rect = self.pause_text.get_rect(center=(Config.WIDTH // 2, 50))

        self.back_to_menu_text = self.game_font.render("BACK TO MENU", True, Config.BLACK)

        self.back_to_menu_rect = self.back_to_menu_text.get_rect(center=(Config.WIDTH // 2 + 5, 250))

        self.resume_text = self.game_font.render("RESUME", True, Config.BLACK)

        self.resume_rect = self.resume_text.get_rect(center=(Config.WIDTH // 2 , 355))

        #Player settings:
        self.m_width = 50
        self.m_height = 50
        self.m_border_radius = 5
        self.m_border_color = (255,255,255)
        self.m_speed = 5
        self.m_step_x = 0
        self.m_step_y = 0

        #Platforms settings:
        self.platform_width = 120
        self.platform_height = 16
        self.platform_border_radius = 2
        self.platform_x = random.randint(0, 140)
        self.platform_y = random.randint(200, 400)



        #Objects:
        self.m_player: Player = Player((Config.WIDTH / 2), (Config.HEIGHT / 2), self.m_width, self.m_height, (60, 170, 220), self.m_border_radius)
        self.m_platform: Platforms = Platforms (self.platform_x  ,self.platform_y  , self.platform_width ,self.platform_height , (60, 170, 220), self.platform_border_radius )
    def run(self):

        while self.m_is_game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.m_is_game_running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.is_paused = not self.is_paused
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.is_paused and event.button == 1:
                        if self.back_to_menu_rect.collidepoint(pygame.mouse.get_pos()):
                            return "back_to_menu"  # ← מחזיר ערך
                        if self.resume_rect.collidepoint(pygame.mouse.get_pos()):
                           self.is_paused = not self.is_paused


            # if not self.is_paused:
            #     pass

            # -------------------תנועה לפי מקשים----------------
            if self.keys[pygame.K_LEFT]:
                self.m_step_x -= self.m_speed
            if self.keys[pygame.K_RIGHT]:
                self.m_step_x += self.m_speed

            self.display_game()
            if self.is_paused:
                self.display_pause_overlay()

            pygame.display.update()
            Config.CLOCK.tick(Config.FPS)
        return None

    def display_game(self):
        # Background Color
        (self.m_screen_two.fill("black"))

        # Display Game Objects
        self.m_player.draw(self.m_screen_two)
        self.m_platform.draw(self.m_screen_two)

    def display_pause_overlay(self):

        self.m_screen_two.blit(self.overlay, (0, 0))
        self.m_screen_two.blit(self.pause_text, self.pause_rect)
        self.m_screen_two.blit(self.back_to_menu_text, self.back_to_menu_rect)
        self.m_screen_two.blit(self.resume_text, self.resume_rect)



        # pg.quit()






