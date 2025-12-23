import random
import pygame
from pygame import Surface

from DataModels.Platforms import Platforms
from DataModels.Player import Player
from settings import Config

pygame.init()

LARGE_FONT = pygame.font.SysFont('Corbel', 60, bold=True)

class Game:
    def __init__(self, i_screen: Surface , menu):
        self.keys = None
        self.m_screen_two: Surface = i_screen
        self.menu = menu
        self.m_is_game_running = True
        self.is_paused = False
        self.game_font = Config.CURRENT_FONT
        self.game_font_bigger = Config.CURRENT_FONT_BIGGER
        self.overlay = pygame.image.load("Menu_images/MenuBG.jpg")
        self.background_image_game = pygame.image.load("Game_images/Game_BG.jpg")
        self.background_image_game  = pygame.transform.scale(self.background_image_game , (Config.WIDTH , Config.HEIGHT))

        self.pause_text = self.game_font.render("PAUSED", True, Config.BLACK)
        self.pause_rect = self.pause_text.get_rect(center=(Config.WIDTH // 2, 50))
        self.back_to_menu_text = self.game_font.render("BACK TO MENU", True, Config.BLACK)
        self.back_to_menu_rect = self.back_to_menu_text.get_rect(center=(Config.WIDTH // 2 + 5, 250))
        self.resume_text = self.game_font.render("RESUME", True, Config.BLACK)
        self.resume_rect = self.resume_text.get_rect(center=(Config.WIDTH // 2 , 355))

        self.game_over = False
        self.game_over_text = self.game_font_bigger.render("GAME OVER", True, (255, 0, 0))
        self.game_over_rect = self.game_over_text.get_rect(center=(Config.WIDTH // 2, 100))

        self.retry_text = self.game_font.render("RETRY", True, (255, 255, 255))
        self.retry_rect = self.retry_text.get_rect(center=(Config.WIDTH // 2, 250))

        self.back_to_menu_text_go = self.game_font.render("BACK TO MENU", True, (255, 255, 255))
        self.back_to_menu_rect_go = self.back_to_menu_text_go.get_rect(center=(Config.WIDTH // 2, 350))

        # Player settings
        self.m_width = 50
        self.m_height = 50
        self.m_border_radius = 5
        self.m_border_color = (255,255,255)
        self.m_speed = 5
        self.x = + 20
        self.y = Config.HEIGHT - 69
        self.gravity = 0.8
        self.velocity_y = 0.0
        self.jump_speed_gravity = -18
        self.fall_line = 100
        self.scroll_line = 100

        # Platforms settings
        self.platform_width = 80
        self.platform_height = 40
        self.platform_border_radius = 2
        self.platform_x = 0
        self.platform_y = Config.HEIGHT- 19
        self.selected_index = 0  # הכפתור הנבחר כרגע
        # self.level_done = False
        # Objects
        self.m_player: Player = Player(self.x, self.y, self.m_width, self.m_height, (60, 170, 220), self.m_border_radius)
        self.m_platform: Platforms = Platforms(random.randint(0, 140), random.randint(200, 400), self.platform_width, self.platform_height, (60, 170, 220), self.platform_border_radius)
        self.m_platform_rect = pygame.Rect(0,0, self.platform_width, 16)
        self.first_platform: Platforms = Platforms(self.platform_x, self.platform_y, Config.WIDTH, self.platform_height, (200, 130, 190), self.platform_border_radius)
        self.platforms = []
        self.level_number = 0
        self.init_platforms(self.level_number)
        self.game_speed = 5  # מתחילים בקצב נמוך
        self.game_over = False
        self.on_ground = False
        self.total_fallen_platforms = 0


        player_bottom = self.y + self.m_height
        platform_top = self.first_platform.platform_rect.top
        if player_bottom >= platform_top and self.x + self.m_width > self.first_platform.platform_rect.left and self.x < self.first_platform.platform_rect.right:
            self.y = platform_top - self.m_height  # מקם את השחקן על הפלטפורמה
            self.velocity_y = 0
            self.on_ground = True

    def run(self):

        while self.m_is_game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.m_is_game_running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.is_paused = not self.is_paused
                    # elif event.key == pygame.K_r:  # R לאיפוס המשחק
                    #     self.__init__(self.m_screen_two, self.menu)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.is_paused and event.button == 1:
                        if self.retry_rect.collidepoint(pygame.mouse.get_pos()):
                            # אתחול המשחק מחדש
                            self.__init__(self.m_screen_two, self.menu)
                        elif self.back_to_menu_rect_go.collidepoint(pygame.mouse.get_pos()):
                            return "back_to_menu"
                        if self.back_to_menu_rect.collidepoint(pygame.mouse.get_pos()):
                            return "back_to_menu"
                        if self.resume_rect.collidepoint(pygame.mouse.get_pos()):
                            self.is_paused = not self.is_paused

                if not self.game_over:
                    self.keys = pygame.key.get_pressed()

            if self.game_over:
                # הצגת המשחק והרקע לפני game over
                self.display_game()
                self.display_game_over()
                pygame.display.update()

                # מחכים לאינטרקציה בלי לולאת while חדשה
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.m_is_game_running = False
                    elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.retry_rect.collidepoint(mouse_pos):
                            self.__init__(self.m_screen_two, self.menu)
                        elif self.back_to_menu_rect_go.collidepoint(mouse_pos):
                            return "back_to_menu"
                continue  # מחזירים את הלולאה הראשית כדי לא להריץ עוד עדכון

            mouse_pos = pygame.mouse.get_pos()  # מקבל את מיקום העכבר

            # בדיקה אם העכבר מעל הכפתור
            if self.retry_rect.collidepoint(mouse_pos):
                color = (255, 100, 100)  # אדום בהיר יותר
            else:
                color = (255, 255, 255)  # צבע רגיל

            # יוצרים מחדש את הטקסט עם הצבע החדש
            retry_text = self.game_font.render("RETRY", True, color)
            self.m_screen_two.blit(retry_text, self.retry_rect)

            # -----------------x-----------------
            self.keys = pygame.key.get_pressed()
            if self.keys[pygame.K_LEFT]:
                self.x -= self.m_speed
            if self.keys[pygame.K_RIGHT]:
                self.x += self.m_speed
            # -----------------x-----------------
            # --------- Screen bounds (לא יוצא מהמסך) ----------
            if self.x < 0:
                self.x = 0
            elif self.x + self.m_width > Config.WIDTH:
                self.x = Config.WIDTH - self.m_width

            # עדכון אנכי עם כבידה
            self.velocity_y += self.gravity
            next_y = self.y + self.velocity_y

            # נניח שהשחקן לא על הקרקע
            self.on_ground = False

            # בדיקה לכל הפלטפורמות (כולל הראשונה)
            for plat in self.platforms + [self.first_platform]:
                player_bottom = next_y + self.m_height
                platform_top = plat.platform_rect.top
                if self.velocity_y > 0 and self.y + self.m_height <= platform_top and player_bottom >= platform_top \
                        and self.x + self.m_width > plat.platform_rect.left and self.x < plat.platform_rect.right:
                    next_y = platform_top - self.m_height
                    self.velocity_y = 0
                    self.on_ground = True

            #  מעדכנים את המיקום של השחקן
            self.y = next_y

            # יצירת פלטפורמות חדשות אם השחקן מתקרב לראש המסך
            if self.platforms:
                highest_y = min([plat.platform_rect.top for plat in self.platforms])
                if highest_y > 50:  # אם הפלטפורמה הגבוהה ביותר רחוקה מדי מהראש
                    new_width = random.randint(50, self.platform_width)
                    new_height = 20
                    color = (200, 130, 190)
                    border_radius = 5
                    x = random.randint(0, Config.WIDTH - new_width)
                    y = highest_y - random.randint(50, 150)
                    new_platform = Platforms(x, y, new_width, new_height, color, border_radius)
                    self.platforms.append(new_platform)

            if self.y > Config.HEIGHT:  # ממש מתחת למסך
                self.game_over = True

            # קפיצה – רק אם השחקן על הקרקע
            if self.on_ground and self.keys[pygame.K_SPACE]:
                self.velocity_y = self.jump_speed_gravity

            # גלילה למעלה כשעולה מעל קו מסויים
            if self.y < self.scroll_line:
                scroll = self.scroll_line - self.y
                self.y = self.scroll_line
                for plat in self.platforms + [self.first_platform]:
                    plat.platform_rect.top += scroll

            # # גלילה למטה כשנופל מתחת לקו
            # elif self.y + self.m_height > Config.HEIGHT - self.fall_line:
            #     scroll = (self.y + self.m_height) - (Config.HEIGHT - self.fall_line)
            #     self.y -= scroll
            #     for plat in self.platforms + [self.first_platform]:
            #         plat.platform_rect.top -= scroll

            self.update_rect()

            if self.y <= 0:  # הגיע לראש המסך
                self.next_level()

            self.display_game()

            if self.is_paused:
                self.display_pause_overlay()

            pygame.display.update()
            Config.CLOCK.tick(Config.FPS)

        return None


        # לעבור על זה-----------------------------------------------------------

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
            # platforms = pla


                # self.velocity_y += self.gravity
                # next_y = self.y + self.velocity_y

                # platform_top = each_rect.top
                # player_bottom = next_y + self.m_height

                # if self.velocity_y > 0 and player_bottom >= platform_top and self.y + self.m_height <= platform_top:
                #     # תקן את השחקן על הפלטפורמה
                #     self.y = platform_top - self.m_height
                #     self.velocity_y = 0
                #     self.on_ground = True
                # else:
                #     self.y = next_y
                #     self.on_ground = False
                #
                # # קפיצה
                # if self.on_ground and self.keys[pygame.K_SPACE]:
                #     self.velocity_y = self.jump_speed_gravity


            # self.update_rect()
            #
            # if self.y <= 0:  # הגיע לראש המסך
            #     self.next_level()
            #
            # self.display_game()
            #
            # if self.is_paused:
            #      self.display_pause_overlay()
            #
            # if self.game_over:
            #     self.display_game_over()
            #     pygame.display.update()
            #     continue  # דילוג על שאר הקוד, עד שהשחקן ילחץ על Retry או Back
            #
            # pygame.display.update()
            # Config.CLOCK.tick(Config.FPS)

    def next_level(self):
        self.level_number += 1
        self.init_platforms(self.level_number)

    def init_platforms(self, level_number):
        self.platforms = []

        platform_width = 300
        platform_height = 20
        color = (200, 130, 190)
        border_radius = 5
        num_platforms = 3  # למשל 3 פלטפורמות לכל שלב

        # הפלטפורמה הראשונה תמיד על הקרקע
        first_y = Config.HEIGHT - 50
        self.first_platform = Platforms(0, first_y, Config.WIDTH, platform_height + 20, color, border_radius)

        prev_y = first_y

        for i in range(num_platforms):
            min_jump = 80
            max_jump = 200

            # נוודא שהפלטפורמה החדשה לא חופפת לזו הקודמת
            gap = random.randint(min_jump, max_jump)
            y = prev_y - gap
            x = random.randint(0,  platform_width)

            # אם הפלטפורמה החדשה גבוהה מדי או חופפת לשעבר, נדחוף אותה עוד קצת למעלה
            if self.platforms and y >= self.platforms[-1].platform_rect.bottom:
                y = self.platforms[-1].platform_rect.top - platform_height - 10  # רווח מינימלי של 10 פיקסלים

            plat = Platforms(x, y,random.randint(60, platform_width -10), platform_height, color, border_radius)
            self.platforms.append(plat)
            prev_y = y

    def check_level_done(self):
        # נניח שהשלב נגמר כשהשחקן הגיע מעל הפלטפורמה הכי גבוהה
        highest_platform = min([plat.platform_rect.top for plat in self.platforms])
        if self.y <= highest_platform:
            return True
        return False

    def display_game_over(self):
        overlay = pygame.Surface((Config.WIDTH, Config.HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))

        self.m_screen_two.blit(overlay, (0, 0))
        mouse_pos = pygame.mouse.get_pos()  # מקבלים את מיקום העכבר

        # Game Over
        self.m_screen_two.blit(self.game_over_text, self.game_over_rect)

        # Retry
        retry_color = (255, 100, 100) if self.retry_rect.collidepoint(mouse_pos) else (255, 255, 255)
        retry_text = self.game_font.render("RETRY", True, retry_color)
        self.m_screen_two.blit(retry_text, self.retry_rect)

        # Back to menu
        back_color = (255, 100, 100) if self.back_to_menu_rect_go.collidepoint(mouse_pos) else (255, 255, 255)
        back_text = self.game_font.render("BACK TO MENU", True, back_color)
        self.m_screen_two.blit(back_text, self.back_to_menu_rect_go)

    def display_game(self):
        self.m_screen_two.blit(self.background_image_game, (0, 0))
        self.first_platform.draw(self.m_screen_two)
        for plat in self.platforms:
            plat.draw(self.m_screen_two)
        self.m_player.draw(self.m_screen_two)

    def update_rect(self):
        self.m_player.player_rect.topleft = (self.x , self.y)


    def display_pause_overlay(self):
        self.m_screen_two.blit(self.overlay, (0, 0))
        self.m_screen_two.blit(self.pause_text, self.pause_rect)
        self.m_screen_two.blit(self.back_to_menu_text, self.back_to_menu_rect)
        self.m_screen_two.blit(self.resume_text, self.resume_rect)

