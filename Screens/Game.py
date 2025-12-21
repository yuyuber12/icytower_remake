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
        self.background_image_game = pygame.image.load("Game_images/Game_BG.jpg")
        self.background_image_game  = pygame.transform.scale(self.background_image_game , (Config.WIDTH , Config.HEIGHT))

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
        self.gravity = 0.8
        self.velocity_y = 0.0
        self.jump_speed_gravity = -16
        self.fall_line = 100
        self.scroll_line = 100

        #Platforms settings:
        self. platform_width = 120
        self.platform_height = 20
        self.platform_border_radius = 2
        self.platform_x = 0
        self.platform_y = Config.HEIGHT- 19
        #x_ = random.randint(0, 140)
        #y_ = random.randint(200, 400)

        # -------------------------------------------ללמוד אתזה---------------------
        # Pause items
        # self.pause_items = [
        #     {"text": "RESUME", "rect": self.resume_rect, "action": "resume"},
        #     {"text": "BACK TO MENU", "rect": self.back_to_menu_rect, "action": "back_to_menu"}
        # ]

        self.selected_index = 0  # הכפתור הנבחר כרגע
        # -------------------------------------------ללמוד אתזה---------------------
        #Objects:
        self.m_player: Player = Player((Config.WIDTH / 2), (Config.HEIGHT / 2), self.m_width, self.m_height, (60, 170, 220), self.m_border_radius)
        self.m_platform: Platforms = Platforms (random.randint(0, 140)  ,random.randint(200, 400)  , self.platform_width ,self.platform_height , (60, 170, 220), self.platform_border_radius )
        # self.m_platform_rect = pygame.Rect((random.randint(0 , 240)),(random.randint(200, 400)), self.platform_height, 16)
        # self.m_player_rect = pygame.Rect((Config.WIDTH / 2), (Config.HEIGHT / 2), self.m_width, self.m_height)
        self.first_platform: Platforms = Platforms(self.platform_x, self.platform_y, Config.WIDTH,self.platform_height, (200, 130, 190), self.platform_border_radius)
        # self.platforms = None

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
                # -------------------------------------------ללמוד אתזה---------------------

                # -------------------------------------------ללמוד אתזה---------------------

            # # -------------------תנועה לפי מקשים----------------
            # if self.keys[pygame.K_LEFT]:
            #     self.m_step_x -= self.m_speed
            # if self.keys[pygame.K_RIGHT]:
            #     self.m_step_x += self.m_speed
            #
            # self.platforms = [
            #     self.m_platform_rect,
            #     self.m_platform_rect,
            #     self.m_platform_rect
            #
            #
            # ]
            # self.m_player_rect.x = self.m_step_x
            #
            # for each_rect in self.platforms:
            #     if self.m_player_rect.colliderect(each_rect):
            #         if self.m_step_x > 0:
            #             self.m_player_rect.right = each_rect.left
            #         elif self.m_step_x < 0:
            #             self.m_player_rect.left = each_rect.right
            #
            # self.m_step_y += self.velocity_y
            # self.velocity_y += self.gravity
            # self.m_player_rect.y += self.m_step_y
            #
            # on_ground = False
            # for each_rect in self.platforms:
            #     if self.m_player_rect.colliderect(each_rect):
            #         if self.m_step_y > 0:
            #             self.m_player_rect.bottom = each_rect.top
            #             self.velocity_y = 0
            #             on_ground = True
            #         elif self.m_step_y < 0:
            #             self.m_player_rect.top = each_rect.bottom
            #             self.velocity_y = 0
            #
            # # קפיצה
            # if on_ground and self.keys[pygame.K_SPACE]:
            #     self.velocity_y = self.jump_speed_gravity
            #
            # # --------- גלילת נפילה (שומר על השחקן בפריים בזמן ירידה) ----------
            # if self.m_player_rect.bottom > self.fall_line and self.m_step_y > 0:
            #     scroll = self.m_player_rect.bottom - self.fall_line
            #     self.m_player_rect.bottom = self.fall_line
            #     for plat in self.platforms:
            #         plat.y -= scroll
            #
            # # --------- גלילת עלייה (כשעולים מעל קו הגלילה) ----------
            # if  self.m_player_rect.top < self.scroll_line and self.m_step_y < 0:
            #     scroll = self.scroll_line -  self.m_player_rect.top
            #     self.m_player_rect.top = self.scroll_line
            #     for each_rect in self.platforms:
            #         each_rect.y += scroll
            #
            # # סינון פלטפורמות שנפלו מתחת למסך (אופציונלי)
            # platforms_onthescreen = []
            # for each_rect in self.platforms:
            #     if each_rect.top < Config.HEIGHT:
            #         platforms_onthescreen.append(each_rect)
            # platforms = platforms_onthescreen
            #
            # # -------------------תיקון גבולות (רק X!)-------------------
            # if  self.m_player_rect.left < 0:
            #     self.m_player_rect.left = 0
            # if  self.m_player_rect.right > Config.WIDTH:
            #     self.m_player_rect.right = Config.WIDTH



            self.display_game()
            if self.is_paused:
                 self.display_pause_overlay()

            pygame.display.update()
            Config.CLOCK.tick(Config.FPS)
        return None

    def display_game(self):
        # Background Color
        # self.m_screen_two.fill("black")

        self.m_screen_two.blit(self.background_image_game, (0, 0))
        # Display Game Objects
        self.first_platform.draw(self.m_screen_two)
        # for each_rect in self.platforms:
        #     pygame.draw.rect(self.m_screen_two, (60, 170, 220), each_rect)
        self.m_player.draw(self.m_screen_two)


    def display_pause_overlay(self):

        self.m_screen_two.blit(self.overlay, (0, 0))
        self.m_screen_two.blit(self.pause_text, self.pause_rect)
        self.m_screen_two.blit(self.back_to_menu_text, self.back_to_menu_rect)
        self.m_screen_two.blit(self.resume_text, self.resume_rect)

        # for i, item in enumerate(self.pause_items):
        #     color = (200, 200, 200) if i == self.selected_index else Config.BLACK
        #     text_surface = self.game_font.render(item["text"], True, color)
        #     self.m_screen_two.blit(text_surface, item["rect"])



        # pg.quit()






