import random
import pygame
from pygame import Surface

from DataModels.Platforms import Platforms
from DataModels.Player import Player
from settings import Config

# Initialize pygame objects for this module.
pygame.init()

# Define a shared large font used by the game screen.
LARGE_FONT = pygame.font.SysFont('Corbel', 60, bold=True)


# Manage gameplay loop, movement, camera, platforms, and score flow.
class Game:
    STAGE_PLATFORM_COUNT = 25
    STAGE_COLORS = [
        (155, 95, 215),
        (70, 165, 220),
        (230, 140, 75),
        (150, 200, 90),
        (180, 120, 220),
        (230, 110, 130),
        (100, 180, 170),
        (235, 190, 80),
        (120, 150, 240),
        (210, 120, 170),
        (120, 200, 130),
    ]

    # Initialize full gameplay state, resources, and UI elements.
    def __init__(self, i_screen: Surface, menu):
        # Configure base runtime references and state flags.
        self.keys = None
        self.m_screen_two: Surface = i_screen
        self.menu = menu
        self.m_is_game_running = True
        self.is_paused = False
        self.game_font = Config.CURRENT_FONT
        self.game_font_bigger = Config.CURRENT_FONT_BIGGER
        self.platform_marker_font = pygame.font.SysFont(
            'Corbel', 16, bold=True)
        self.overlay = pygame.image.load("Menu_images/MenuBG.jpg")
        self.background_image_game = pygame.image.load(
            "Game_images/Game_BG.jpg")
        self.background_image_game = pygame.transform.scale(
            self.background_image_game, (Config.WIDTH, Config.HEIGHT))
        self.background_offset_x = 0.0
        self.background_parallax_factor = 0.2

        # Build pause menu UI text surfaces.
        self.pause_text = self.game_font.render("PAUSED", True, Config.BLACK)
        self.pause_rect = self.pause_text.get_rect(
            center=(Config.WIDTH // 2, 50))
        self.back_to_menu_text = self.game_font.render(
            "BACK TO MENU", True, Config.BLACK)
        self.back_to_menu_rect = self.back_to_menu_text.get_rect(
            center=(Config.WIDTH // 2 + 5, 250))
        self.resume_text = self.game_font.render("RESUME", True, Config.BLACK)
        self.resume_rect = self.resume_text.get_rect(
            center=(Config.WIDTH // 2, 355))

        # Build game-over UI text surfaces.
        self.game_over = False
        self.game_over_text = self.game_font_bigger.render(
            "GAME OVER", True, (255, 0, 0))
        self.game_over_rect = self.game_over_text.get_rect(
            center=(Config.WIDTH // 2, 100))
        self.final_score_text = self.game_font.render(
            "SCORE 0", True, (255, 255, 255))
        self.final_score_rect = self.final_score_text.get_rect(
            center=(Config.WIDTH // 2, 170))

        self.retry_text = self.game_font.render("RETRY", True, (255, 255, 255))
        self.retry_rect = self.retry_text.get_rect(
            center=(Config.WIDTH // 2, 250))

        self.back_to_menu_text_go = self.game_font.render(
            "BACK TO MENU", True, (255, 255, 255))
        self.back_to_menu_rect_go = self.back_to_menu_text_go.get_rect(
            center=(Config.WIDTH // 2, 350))

        # Configure player size, motion, physics, and camera tuning values.
        self.m_width = 50
        self.m_height = 50
        self.m_border_radius = 5
        self.m_border_color = (255, 255, 255)
        self.m_speed = 5
        self.x = + 20
        self.y = Config.HEIGHT - 69
        self.player_x = float(self.x)
        self.player_y = float(self.y)
        self.gravity = 0.8
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.jump_speed_gravity = -16
        self.max_jump_boost = 12
        self.max_speed_boost = 4
        self.max_move_speed = 8.5
        self.acceleration_ground = 0.7
        self.acceleration_air = 0.28
        self.friction_ground = 1.25
        self.friction_air = 0.35
        self.runup_charge = 0.0
        self.base_gravity = 0.8
        self.base_max_move_speed = 8.5
        self.base_acceleration_ground = 0.7
        self.base_acceleration_air = 0.28
        self.base_max_speed_boost = 4
        self.base_scroll_line = 140
        self.scroll_speed_factor = 1.0
        self.idle_meter = 0.0
        self.camera_rise_base = 0.0
        self.camera_rise_max = 2.8
        self.camera_rise_stage_bonus = 0.12
        self.fall_line = Config.HEIGHT + 80
        self.scroll_line = self.base_scroll_line
        self.camera_bottom_line = Config.HEIGHT - 120
        self.fall_distance_tracked = 0.0
        self.max_fall_distance = Config.HEIGHT + 120
        self.total_climbed = 0
        self.score = 0
        self.level_height = 900
        self.crumble_delay_ms = 60000
        self.crumble_interval_ms = 900
        self.crumble_start_ticks = 0
        self.crumble_last_tick = 0
        self.crumble_started = False
        self.crumble_time_left_ms = self.crumble_delay_ms
        self.crumble_trigger_platforms = 6
        self.platforms_passed = 0
        self.counted_platform_ids = set()

        # Configure platform generation and stage progression settings.
        self.platform_width = 140
        self.platform_height = 16
        self.platform_border_radius = 2
        self.platform_x = 0
        self.platform_y = Config.HEIGHT - 20
        self.platform_min_width = 85
        self.platform_max_width = 210
        self.target_platforms = 12
        self.platform_counter = 2
        self.current_stage = 1
        self.selected_index = 0
        # self.level_done = False

        # Create gameplay objects and generate initial platforms.
        self.m_player: Player = Player(
            self.x, self.y, self.m_width, self.m_height, (60, 170, 220), self.m_border_radius)
        self.m_platform: Platforms = Platforms(random.randint(0, 140), random.randint(
            200, 400), self.platform_width, self.platform_height, (60, 170, 220), self.platform_border_radius)
        self.m_platform_rect = pygame.Rect(
            0, 0, self.platform_width, self.platform_height)
        self.first_platform: Platforms = Platforms(
            self.platform_x,
            self.platform_y,
            Config.WIDTH,
            self.platform_height,
            self.get_stage_color(1),
            self.platform_border_radius,
        )
        self.first_platform.stage_number = 1
        self.first_platform.platform_index = 1
        self.first_platform.is_stage_end = False
        self.level_number = 1
        self.game_speed = 5  # מתחילים בקצב נמוך
        self.game_over = False
        self.score_saved = False
        self.on_ground = False
        self.platforms = []
        self.init_platforms(self.level_number)
        # self.total_fallen_platforms = 0

    # Run the main game loop and handle pause/game-over/menu transitions.
    def run(self):

        while self.m_is_game_running:
            # Process window, keyboard, and mouse events.
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
                            # Restart current game state.
                            self.__init__(self.m_screen_two, self.menu)
                        elif self.back_to_menu_rect_go.collidepoint(pygame.mouse.get_pos()):
                            return "back_to_menu"
                        if self.back_to_menu_rect.collidepoint(pygame.mouse.get_pos()):
                            return "back_to_menu"
                        if self.resume_rect.collidepoint(pygame.mouse.get_pos()):
                            self.is_paused = not self.is_paused

                if not self.game_over:
                    self.keys = pygame.key.get_pressed()

            # Handle dedicated game-over interaction flow.
            if self.game_over:
                # Draw current frame state and then overlay game-over UI.
                self.display_game()
                self.display_game_over()
                pygame.display.update()

                # Wait for retry/menu input without creating a nested loop.
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.m_is_game_running = False
                    elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.retry_rect.collidepoint(mouse_pos):
                            self.__init__(self.m_screen_two, self.menu)
                        elif self.back_to_menu_rect_go.collidepoint(mouse_pos):
                            return "back_to_menu"
                continue

            # Update retry text color by current mouse hover.
            mouse_pos = pygame.mouse.get_pos()

            if self.retry_rect.collidepoint(mouse_pos):
                color = (255, 100, 100)
            else:
                color = (255, 255, 255)

            # Re-render retry text using the selected hover color.
            retry_text = self.game_font_bigger.render("RETRY", True, color)
            self.m_screen_two.blit(retry_text, self.retry_rect)

            # Pause update logic and show pause overlay when paused.
            if self.is_paused:
                self.display_game()
                self.display_pause_overlay()
                pygame.display.update()
                Config.CLOCK.tick(Config.FPS)
                continue

            # Read movement input and compute horizontal velocity.
            self.keys = pygame.key.get_pressed()
            player_rect = self.m_player.player_rect
            self.apply_stage_difficulty()
            move_dir = 0
            if self.keys[pygame.K_LEFT]:
                move_dir -= 1
            if self.keys[pygame.K_RIGHT]:
                move_dir += 1

            was_on_ground = self.on_ground
            if move_dir != 0:
                acceleration = self.acceleration_ground if was_on_ground else self.acceleration_air
                self.velocity_x += move_dir * acceleration
                max_speed = self.max_move_speed + self.runup_charge * self.max_speed_boost
                if self.velocity_x > max_speed:
                    self.velocity_x = max_speed
                elif self.velocity_x < -max_speed:
                    self.velocity_x = -max_speed
                if was_on_ground and abs(self.velocity_x) > self.m_speed * 0.8:
                    self.runup_charge = min(1.0, self.runup_charge + 0.02)
            else:
                friction = self.friction_ground if was_on_ground else self.friction_air
                if self.velocity_x > 0:
                    self.velocity_x = max(0.0, self.velocity_x - friction)
                elif self.velocity_x < 0:
                    self.velocity_x = min(0.0, self.velocity_x + friction)
                if was_on_ground:
                    self.runup_charge = max(0.0, self.runup_charge - 0.04)

            self.player_x += self.velocity_x
            player_rect.x = int(self.player_x)

            # Clamp player position to horizontal screen bounds.
            if player_rect.left < 0:
                player_rect.left = 0
                self.player_x = float(player_rect.x)
                self.velocity_x = 0.0
            elif player_rect.right > Config.WIDTH:
                player_rect.right = Config.WIDTH
                self.player_x = float(player_rect.x)
                self.velocity_x = 0.0

            # Apply gravity and move player vertically.
            self.velocity_y += self.gravity
            previous_top = player_rect.top
            previous_bottom = player_rect.bottom
            self.player_y += self.velocity_y
            player_rect.y = int(self.player_y)

            # Resolve landing collisions with platforms.
            self.on_ground = False
            landed_platform = None
            for platform in self.platforms:
                platform_rect = platform.platform_rect
                if not player_rect.colliderect(platform_rect):
                    continue

                if self.velocity_y > 0 and previous_bottom <= platform_rect.top + 3:
                    player_rect.bottom = platform_rect.top
                    self.player_y = float(player_rect.y)
                    self.velocity_y = 0
                    self.on_ground = True
                    landed_platform = platform
                    break

                    # Count unique landed platforms for stage progression.
            if landed_platform is not None and landed_platform is not self.first_platform:
                landed_id = id(landed_platform)
                if landed_id not in self.counted_platform_ids:
                    self.counted_platform_ids.add(landed_id)
                    self.platforms_passed += 1
                    self.current_stage = self.platforms_passed // self.STAGE_PLATFORM_COUNT + 1

            # Apply jump impulse with run-up and momentum bonuses.
            if self.on_ground and self.keys[pygame.K_SPACE]:
                momentum_factor = min(
                    1.0, abs(self.velocity_x) / self.max_move_speed)
                jump_bonus = self.max_jump_boost * \
                    (0.65 * self.runup_charge + 0.35 * momentum_factor)
                self.velocity_y = self.jump_speed_gravity - jump_bonus
                horizontal_boost = self.max_speed_boost * self.runup_charge
                if self.velocity_x > 0:
                    self.velocity_x += horizontal_boost
                elif self.velocity_x < 0:
                    self.velocity_x -= horizontal_boost
                self.runup_charge *= 0.35
                self.on_ground = False

            # Scroll world while ascending and generate platforms above.
            if player_rect.top < self.scroll_line and self.velocity_y < 0:
                scroll = self.scroll_line - player_rect.top
                scroll *= self.scroll_speed_factor
                player_rect.top = self.scroll_line
                self.player_y = float(player_rect.y)
                self.apply_world_scroll(scroll)
                self.ensure_platforms()
                self.fall_distance_tracked = 0.0

            # Scroll world while descending near the bottom camera line.
            if player_rect.bottom > self.camera_bottom_line and self.velocity_y > 0:
                down_scroll = player_rect.bottom - self.camera_bottom_line
                player_rect.bottom = self.camera_bottom_line
                self.player_y = float(player_rect.y)
                self.apply_world_scroll(-down_scroll)
                self.fall_distance_tracked += down_scroll

            if self.on_ground:
                self.fall_distance_tracked = 0.0

            # Apply camera pressure behavior for prolonged idle states.
            self.apply_camera_pressure(move_dir)

            # Keep only relevant platforms and update crumble timer.
            self.platforms = [
                plat for plat in self.platforms if -260 < plat.platform_rect.top < Config.HEIGHT + 220]
            self.crumble_time_left_ms = self.update_platform_collapse_timer()
            self.level_number = self.current_stage

            # Trigger game-over when player falls too far.
            if self.fall_distance_tracked > self.max_fall_distance or player_rect.top > self.fall_line:
                self.game_over = True
                if not self.score_saved:
                    self.save_score_to_menu()

            self.x = player_rect.x
            self.player_x = float(player_rect.x)
            self.y = self.player_y

            # Render the active gameplay frame.
            self.display_game()

            if self.is_paused:
                self.display_pause_overlay()

            pygame.display.update()
            Config.CLOCK.tick(Config.FPS)

        return None

    # Move to next logical level and ensure enough platforms exist.
    def next_level(self):
        self.level_number += 1
        self.ensure_platforms()

    # Reset and generate initial platform layout for a new game/level.
    def init_platforms(self, level_number):
        print(
            f"🎮 init_platforms: התחלה - platform_counter = {self.platform_counter}")
        self.platforms = [self.first_platform]
        print(
            f"   first_platform: index={self.first_platform.platform_index}, stage={self.first_platform.stage_number}")
        self.ensure_platforms()
        print(
            f"   אחרי ensure_platforms: יש {len(self.platforms)} פלטפורמות, counter={self.platform_counter}")
        for i, p in enumerate(self.platforms):
            idx = getattr(p, 'platform_index', '?')
            stage = getattr(p, 'stage_number', '?')
            print(
                f"      Platform #{i}: index={idx}, stage={stage}, y={p.platform_rect.top}")

    # Create one platform above a top anchor using stage-based difficulty values.
    def create_platform_above(self, top_anchor):
        # Estimate platform number based on progress and current world position.
        player_y = self.m_player.player_rect.top
        platforms_above_player = len(
            [p for p in self.platforms if p.platform_rect.top < player_y])
        estimated_plat_num = self.platforms_passed + platforms_above_player + 1
        stage_number = (estimated_plat_num -
                        1) // self.STAGE_PLATFORM_COUNT + 1
        difficulty = min(stage_number - 1, 12)
        gap_min = 75 + difficulty * 5
        gap_max = 125 + difficulty * 10
        platform_gap = random.randint(gap_min, gap_max)

        width_min = max(65, self.platform_min_width - difficulty * 4)
        width_max = max(
            width_min + 20, self.platform_max_width - difficulty * 7)
        platform_width = random.randint(width_min, width_max)
        platform_x = random.randint(0, Config.WIDTH - platform_width)
        platform_y = top_anchor - platform_gap
        platform_color = self.get_stage_color(stage_number)

        # Debug print for early platforms to verify stage/color transitions.
        if estimated_plat_num <= 60:
            print(
                f"Platform #{estimated_plat_num:3d} | Stage {stage_number:2d} | Color {platform_color} | passed={self.platforms_passed}")

        new_platform = Platforms(
            platform_x,
            platform_y,
            platform_width,
            self.platform_height,
            platform_color,
            self.platform_border_radius,
        )
        new_platform.stage_number = stage_number
        new_platform.platform_index = estimated_plat_num
        new_platform.is_stage_end = (
            estimated_plat_num % self.STAGE_PLATFORM_COUNT == 0)
        self.platform_counter += 1

        return new_platform

    # Ensure enough platforms are available above the current highest one.
    def ensure_platforms(self):
        if not self.platforms:
            self.platforms = [self.first_platform]

        highest_platform_top = min(
            plat.platform_rect.top for plat in self.platforms)
        while highest_platform_top > -200:
            new_platform = self.create_platform_above(highest_platform_top)
            self.platforms.append(new_platform)
            highest_platform_top = new_platform.platform_rect.top

    # Apply world scrolling to platforms and score-related progress.
    def apply_world_scroll(self, scroll, count_progress=True):
        if scroll == 0:
            return

        scroll_step = int(round(scroll))
        if scroll_step == 0:
            return

        for platform in self.platforms:
            platform.platform_rect.y += scroll_step

        if scroll_step > 0 and count_progress:
            self.total_climbed += scroll_step
            self.score = self.total_climbed // 10
            self.background_offset_x = (
                self.background_offset_x + scroll_step * self.background_parallax_factor
            ) % Config.WIDTH

    # Run collapse timer logic and periodically remove bottom platforms.
    def update_platform_collapse_timer(self):
        now_ticks = pygame.time.get_ticks()
        if self.platforms_passed < self.crumble_trigger_platforms:
            return 0

        if self.crumble_start_ticks == 0:
            self.crumble_start_ticks = now_ticks
            self.crumble_last_tick = now_ticks

        if not self.crumble_started:
            elapsed = now_ticks - self.crumble_start_ticks
            remaining = max(0, self.crumble_delay_ms - elapsed)
            if remaining == 0:
                self.crumble_started = True
                self.crumble_last_tick = now_ticks
            return remaining

        if now_ticks - self.crumble_last_tick >= self.crumble_interval_ms:
            self.crumble_last_tick = now_ticks
            self.collapse_next_bottom_platform()

        return 0

    # Remove the lowest safe platform that is not currently under the player.
    def collapse_next_bottom_platform(self):
        if len(self.platforms) <= 1:
            return

        player_rect = self.m_player.player_rect
        candidate_indexes = sorted(
            range(len(self.platforms)),
            key=lambda idx: self.platforms[idx].platform_rect.top,
            reverse=True,
        )

        for idx in candidate_indexes:
            platform_rect = self.platforms[idx].platform_rect
            if platform_rect.colliderect(player_rect):
                continue

            del self.platforms[idx]
            return

    # Check whether player has passed the highest platform (legacy helper).
    def check_level_done(self):
        # A level is considered complete once player is above the highest platform.
        highest_platform = min(
            [plat.platform_rect.top for plat in self.platforms])
        if self.y <= highest_platform:
            return True
        return False

    # Render the game-over overlay and interactive options.
    def display_game_over(self):
        overlay = pygame.Surface((Config.WIDTH, Config.HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))

        self.m_screen_two.blit(overlay, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        # Draw game-over title and score.
        self.m_screen_two.blit(self.game_over_text, self.game_over_rect)
        self.final_score_text = self.game_font.render(
            f"SCORE {int(self.score)}", True, (255, 255, 255))
        self.final_score_rect = self.final_score_text.get_rect(
            center=(Config.WIDTH // 2, 175))
        self.m_screen_two.blit(self.final_score_text, self.final_score_rect)

        # Draw retry action with hover feedback.
        retry_color = (255, 100, 100) if self.retry_rect.collidepoint(
            mouse_pos) else (255, 255, 255)
        retry_text = self.game_font.render("RETRY", True, retry_color)
        self.m_screen_two.blit(retry_text, self.retry_rect)

        # Draw back-to-menu action with hover feedback.
        back_color = (255, 100, 100) if self.back_to_menu_rect_go.collidepoint(
            mouse_pos) else (255, 255, 255)
        back_text = self.game_font.render("BACK TO MENU", True, back_color)
        self.m_screen_two.blit(back_text, self.back_to_menu_rect_go)

    # Render gameplay background, platforms, HUD, and player.
    def display_game(self):
        bg_x = int(self.background_offset_x) % Config.WIDTH
        self.m_screen_two.blit(self.background_image_game,
                               (bg_x - Config.WIDTH, 0))
        self.m_screen_two.blit(self.background_image_game, (bg_x, 0))
        for plat in self.platforms:
            platform_index = getattr(plat, "platform_index", 1)
            stage_number = (platform_index -
                            1) // self.STAGE_PLATFORM_COUNT + 1
            stage_color = self.get_stage_color(stage_number)
            plat._color = stage_color
            plat.stage_number = stage_number
            plat.draw(self.m_screen_two)
            if getattr(plat, "is_stage_end", False):
                marker_text = self.platform_marker_font.render(
                    f"{platform_index}", True, Config.BLACK)
                marker_rect = marker_text.get_rect(
                    center=(plat.platform_rect.centerx,
                            plat.platform_rect.centery)
                )
                self.m_screen_two.blit(marker_text, marker_rect)

        level_text = self.game_font.render(
            f"LEVEL {self.level_number}", True, Config.WHITE)
        score_text = self.game_font.render(
            f"SCORE {int(self.score)}", True, Config.WHITE)

        self.m_screen_two.blit(level_text, (20, 15))
        self.m_screen_two.blit(score_text, (20, 60))
        self.draw_hourglass((30, 115))

        if self.crumble_started:
            break_text = self.game_font.render("BREAK", True, (255, 150, 150))
            self.m_screen_two.blit(break_text, (75, 128))
        self.m_player.draw(self.m_screen_two)

    # Save final score through menu storage interface once per game-over state.
    def save_score_to_menu(self):
        if self.score_saved:
            return

        if hasattr(self.menu, "add_score"):
            self.menu.add_score(int(self.score))

        self.score_saved = True

    # Draw hourglass timer indicating time left before platform collapse starts.
    def draw_hourglass(self, position):
        x, y = position
        frame_color = (240, 240, 240)
        sand_color = (244, 196, 88)
        empty_color = (45, 45, 45)

        outer_rect = pygame.Rect(x, y, 34, 48)
        top_circle_rect = pygame.Rect(x + 3, y + 3, 28, 18)
        bottom_circle_rect = pygame.Rect(x + 3, y + 27, 28, 18)

        pygame.draw.rect(self.m_screen_two, frame_color,
                         outer_rect, 2, border_radius=12)
        pygame.draw.ellipse(self.m_screen_two, frame_color, top_circle_rect, 2)
        pygame.draw.ellipse(self.m_screen_two, frame_color,
                            bottom_circle_rect, 2)
        pygame.draw.line(self.m_screen_two, frame_color,
                         (x + 17, y + 21), (x + 17, y + 27), 2)

        if self.platforms_passed < self.crumble_trigger_platforms:
            ratio = 1.0
        elif self.crumble_started:
            ratio = 0.0
        else:
            ratio = max(
                0.0, min(1.0, self.crumble_time_left_ms / self.crumble_delay_ms))

        top_area = pygame.Rect(x + 5, y + 5, 24, 14)
        bottom_area = pygame.Rect(x + 5, y + 29, 24, 14)

        pygame.draw.ellipse(self.m_screen_two, empty_color, top_area, 0)
        pygame.draw.ellipse(self.m_screen_two, empty_color, bottom_area, 0)

        top_fill_height = max(0, int(top_area.height * ratio))
        bottom_fill_height = max(0, int(bottom_area.height * (1.0 - ratio)))

        if top_fill_height > 0:
            top_fill_rect = pygame.Rect(
                top_area.left,
                top_area.bottom - top_fill_height,
                top_area.width,
                top_fill_height,
            )
            pygame.draw.ellipse(self.m_screen_two,
                                sand_color, top_fill_rect, 0)

        if bottom_fill_height > 0:
            bottom_fill_rect = pygame.Rect(
                bottom_area.left,
                bottom_area.top,
                bottom_area.width,
                bottom_fill_height,
            )
            pygame.draw.ellipse(self.m_screen_two,
                                sand_color, bottom_fill_rect, 0)

        if ratio > 0 and ratio < 1:
            pygame.draw.line(self.m_screen_two, sand_color,
                             (x + 17, y + 21), (x + 17, y + 27), 2)

    # Resolve platform color by stage number.
    def get_stage_color(self, stage_number):
        """Resolve platform color by stage where each 25 platforms are one stage."""
        palette_index = (stage_number - 1) % len(self.STAGE_COLORS)
        color = self.STAGE_COLORS[palette_index]
        return color

    # Reset per-frame stage difficulty parameters.
    def apply_stage_difficulty(self):
        self.gravity = self.base_gravity
        self.max_move_speed = self.base_max_move_speed
        self.max_speed_boost = self.base_max_speed_boost
        self.acceleration_ground = self.base_acceleration_ground
        self.acceleration_air = self.base_acceleration_air
        self.scroll_line = self.base_scroll_line
        self.scroll_speed_factor = 1.0

    # Push camera upward if player remains idle for too long at higher stages.
    def apply_camera_pressure(self, move_dir):
        if self.current_stage <= 1 or self.platforms_passed < 1:
            self.idle_meter = 0.0
            return

        is_slow_horizontal = abs(self.velocity_x) < 1.0
        is_slow_vertical = abs(self.velocity_y) < 2.2
        is_idle = move_dir == 0 and is_slow_horizontal and is_slow_vertical

        if is_idle:
            self.idle_meter = min(1.0, self.idle_meter + 0.02)
        else:
            self.idle_meter = max(0.0, self.idle_meter - 0.05)

        stage_factor = min(1.0, (self.current_stage - 1)
                           * self.camera_rise_stage_bonus)

        rise_strength = self.camera_rise_base + \
            (0.6 + stage_factor * 1.5) * self.idle_meter
        rise_strength = min(self.camera_rise_max, rise_strength)

        if rise_strength > 0.12 and self.idle_meter > 0.25:
            self.apply_world_scroll(rise_strength, count_progress=False)

    # Sync external x/y values into the player's rect.
    def update_rect(self):
        self.m_player.player_rect.topleft = (self.x, self.y)

    # Draw the pause overlay and pause menu actions.
    def display_pause_overlay(self):
        self.m_screen_two.blit(self.overlay, (0, 0))
        self.m_screen_two.blit(self.pause_text, self.pause_rect)
        self.m_screen_two.blit(self.back_to_menu_text, self.back_to_menu_rect)
        self.m_screen_two.blit(self.resume_text, self.resume_rect)
