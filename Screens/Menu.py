import pygame
import json
import os
from Screens import Game
from pygame import Surface
from Screens.Instructions import Instructions
from settings import Config

# Initialize pygame for the menu module.
pygame.init()


# Manage main menu navigation, instructions, and score display.
class Menu:
    # Initialize menu state, assets, and persistent score storage.
    def __init__(self, i_screen: Surface):
        # Define where score history is stored.
        self.scores_file_path = os.path.join("Notes", "scores.json")

        # Initialize shared static score fields once.
        if not hasattr(Menu, "scores_loaded"):
            Menu.scores_loaded = False
        if not hasattr(Menu, "score_history"):
            Menu.score_history = []
        if not hasattr(Menu, "last_score"):
            Menu.last_score = 0
        if not Menu.scores_loaded:
            self.load_scores_from_file()
            Menu.scores_loaded = True

        # Configure base menu flags and loaded images.
        self.m_screen_one = i_screen
        self.m_is_menu_running = True
        self.show_instructions = False
        self.show_scores = False
        self.background_image = pygame.image.load("Menu_images/MenuBG.jpg")
        self.background_image = pygame.transform.scale(
            self.background_image, (Config.WIDTH, Config.HEIGHT))
        self.paper_image = pygame.image.load("Menu_images/paper.png")
        self.paper_image = pygame.transform.scale(
            self.paper_image, (Config.WIDTH - 220, Config.HEIGHT - 130))
        self.paper_menu_pos = (110, 55)
        self.paper_scores_pos = (110, 45)
        self.instructions_image = pygame.image.load("Menu_images/SpaceBar.png")
        self.menu_font = Config.CURRENT_FONT
        self.menu_text_x = 300

        # Build all menu text surfaces and interaction rectangles.
        self.play_game_text = self.menu_font.render(
            "PLAY GAME", True, Config.BLACK)
        self.play_game_text_x = self.menu_text_x
        self.play_game_text_y = 75
        self.play_game_rect = self.play_game_text.get_rect(
            topleft=(self.play_game_text_x, self.play_game_text_y))

        self.instructions_text = self.menu_font.render(
            "INSTRUCTIONS", True, Config.BLACK)
        self.instructions_text_x = self.menu_text_x
        self.instructions_text_y = 160
        self.instructions_rect = self.instructions_text.get_rect(
            topleft=(self.instructions_text_x, self.instructions_text_y))

        self.scores_text = self.menu_font.render("SCORES", True, Config.BLACK)
        self.scores_text_x = self.menu_text_x
        self.scores_text_y = 250
        self.scores_rect = self.scores_text.get_rect(
            topleft=(self.scores_text_x, self.scores_text_y))

        self.exit_text = self.menu_font.render("EXIT", True, Config.BLACK)
        self.exit_text_x = self.menu_text_x
        self.exit_text_y = 330
        self.exit_rect = self.exit_text.get_rect(
            topleft=(self.exit_text_x, self.exit_text_y))

        self.scores_title = self.menu_font.render("SCORES", True, Config.BLACK)
        self.back_text = self.menu_font.render("BACK", True, Config.BLACK)
        self.back_rect = self.back_text.get_rect(
            center=(Config.WIDTH // 2, 390))

        # Register selectable menu actions.
        self.menu_items = [
            {"text": self.play_game_text,
                "rect": self.play_game_rect, "action": "play"},
            {"text": self.instructions_text,
                "rect": self.instructions_rect, "action": "instructions"},
            {"text": self.scores_text, "rect": self.scores_rect, "action": "scores"},
            {"text": self.exit_text, "rect": self.exit_rect, "action": "exit"}
        ]

        # Track current selection and active input mode.
        self.selected_index = 0
        self.using_keyboard = False

        # Initialize selector finger position and offsets.
        self.finger_x = self.play_game_rect.left - Config.FINGER_IMAGE.get_width() - 10
        self.finger_y = self.play_game_rect.centery - \
            Config.FINGER_IMAGE.get_height() // 2 + 10
        self.scores_finger_x_offset = 18
        self.scores_finger_y_offset = 16

    # Run the menu loop and route actions to the right screen.
    def run(self):
        while self.m_is_menu_running:
            # Process all incoming events for keyboard and mouse control.
            for event in pygame.event.get():
                # Switch to mouse mode on mouse activity.
                if event.type in [pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN]:
                    self.using_keyboard = False

                # Handle score-screen specific inputs.
                if self.show_scores:
                    if event.type == pygame.KEYDOWN and event.key in [pygame.K_ESCAPE, pygame.K_RETURN]:
                        self.show_scores = False
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.back_rect.collidepoint(mouse_pos):
                            self.show_scores = False
                    if event.type == pygame.QUIT:
                        return "exit"
                    continue

                # Handle mouse click actions on menu items.
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        for item in self.menu_items:
                            if item["rect"].collidepoint(mouse_pos):
                                action = item["action"]

                                if action == "play":
                                    self.m_is_menu_running = False
                                elif action == "instructions":
                                    instructions = Instructions(
                                        self.m_screen_one)
                                    instructions.run()
                                elif action == "scores":
                                    self.show_scores = True
                                elif action == "exit":
                                    return "exit"

                # Handle keyboard navigation and action selection.
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
                        elif action == "scores":
                            self.show_scores = True
                        elif action == "exit":
                            return "exit"

                # Handle direct window close.
                if event.type == pygame.QUIT:
                    return "exit"

            # Render scores screen while it is active.
            if self.show_scores:
                self.display_scores()
                pygame.display.update()
                Config.CLOCK.tick(Config.FPS)
                continue

            # Render standard menu view.
            self.display_menu()

            # Compute current hover state for menu options.
            mouse_pos = pygame.mouse.get_pos()
            is_hover_on_play_game_rect = self.play_game_rect.collidepoint(
                mouse_pos)
            is_hover_on_instructions_rect = self.instructions_rect.collidepoint(
                mouse_pos)
            is_hover_on_exit_rect = self.exit_rect.collidepoint(mouse_pos)
            is_hover_on_scores_rect = self.scores_rect.collidepoint(mouse_pos)

            # Draw selector finger according to keyboard or mouse mode.
            if self.using_keyboard:
                selected_rect = self.menu_items[self.selected_index]["rect"]
                selected_action = self.menu_items[self.selected_index]["action"]
                if selected_action == "scores":
                    self.finger_x = selected_rect.left - Config.FINGER_IMAGE.get_width() - \
                        self.scores_finger_x_offset
                    self.finger_y = selected_rect.centery - Config.FINGER_IMAGE.get_height() // 2 + \
                        self.scores_finger_y_offset
                else:
                    self.finger_x = selected_rect.left - Config.FINGER_IMAGE.get_width() - 10
                    self.finger_y = selected_rect.centery - \
                        Config.FINGER_IMAGE.get_height() // 2 + 10
                self.m_screen_one.blit(
                    Config.FINGER_IMAGE, (self.finger_x, self.finger_y))
            else:
                if is_hover_on_play_game_rect:
                    self.finger_x = self.play_game_rect.left - Config.FINGER_IMAGE.get_width() - 10
                    self.finger_y = self.play_game_rect.centery - \
                        Config.FINGER_IMAGE.get_height() // 2 + 10
                    self.m_screen_one.blit(
                        Config.FINGER_IMAGE, (self.finger_x, self.finger_y))
                elif is_hover_on_instructions_rect:
                    self.finger_x = self.instructions_rect.left - \
                        Config.FINGER_IMAGE.get_width() - 10
                    self.finger_y = self.instructions_rect.centery - \
                        Config.FINGER_IMAGE.get_height() // 2 + 10
                    self.m_screen_one.blit(
                        Config.FINGER_IMAGE, (self.finger_x, self.finger_y))
                elif is_hover_on_exit_rect:
                    self.finger_x = self.exit_rect.left - Config.FINGER_IMAGE.get_width() - 10
                    self.finger_y = self.exit_rect.centery - \
                        Config.FINGER_IMAGE.get_height() // 2 + 10
                    self.m_screen_one.blit(
                        Config.FINGER_IMAGE, (self.finger_x, self.finger_y))
                elif is_hover_on_scores_rect:
                    self.finger_x = self.scores_rect.left - Config.FINGER_IMAGE.get_width() - \
                        self.scores_finger_x_offset
                    self.finger_y = self.scores_rect.centery - \
                        Config.FINGER_IMAGE.get_height() // 2 + self.scores_finger_y_offset
                    self.m_screen_one.blit(
                        Config.FINGER_IMAGE, (self.finger_x, self.finger_y))

            # Present the rendered menu frame.
            pygame.display.update()
            Config.CLOCK.tick(Config.FPS)

        return None

    # Draw the main menu background and text buttons.
    def display_menu(self):
        # Background
        self.m_screen_one.blit(self.background_image, (0, 0))
        self.m_screen_one.blit(self.paper_image, self.paper_menu_pos)

        # Draw menu labels.
        self.m_screen_one.blit(self.play_game_text, self.play_game_rect)
        self.m_screen_one.blit(self.instructions_text, self.instructions_rect)
        self.m_screen_one.blit(self.exit_text, self.exit_rect)
        self.m_screen_one.blit(self.scores_text, self.scores_rect)

    # Add a new score, keep top scores sorted, and persist to file.
    def add_score(self, score):
        safe_score = max(0, int(score))
        Menu.last_score = safe_score
        Menu.score_history.append(safe_score)
        Menu.score_history.sort(reverse=True)
        Menu.score_history = Menu.score_history[:10]
        self.save_scores_to_file()

    # Load score data from disk and sanitize input values.
    def load_scores_from_file(self):
        try:
            if not os.path.exists(self.scores_file_path):
                return

            with open(self.scores_file_path, "r", encoding="utf-8") as score_file:
                score_data = json.load(score_file)

            if isinstance(score_data, dict):
                score_history = score_data.get("score_history", [])
                last_score = score_data.get("last_score", 0)
            else:
                score_history = []
                last_score = 0

            cleaned_scores = [
                max(0, int(item)) for item in score_history if isinstance(item, (int, float))]
            cleaned_scores.sort(reverse=True)
            Menu.score_history = cleaned_scores[:10]
            Menu.last_score = max(0, int(last_score))
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            Menu.score_history = []
            Menu.last_score = 0

    # Save current score data to disk in JSON format.
    def save_scores_to_file(self):
        try:
            os.makedirs(os.path.dirname(self.scores_file_path), exist_ok=True)
            score_data = {
                "last_score": int(Menu.last_score),
                "score_history": [int(item) for item in Menu.score_history],
            }
            with open(self.scores_file_path, "w", encoding="utf-8") as score_file:
                json.dump(score_data, score_file, ensure_ascii=False, indent=2)
        except OSError:
            return

        # Render the score board screen and back button.
    def display_scores(self):
        self.m_screen_one.blit(self.background_image, (0, 0))
        self.m_screen_one.blit(self.paper_image, self.paper_scores_pos)
        title_rect = self.scores_title.get_rect(center=(Config.WIDTH // 2, 90))
        self.m_screen_one.blit(self.scores_title, title_rect)

        last_score_text = self.menu_font.render(
            f"LAST: {Menu.last_score}", True, Config.BLACK)
        self.m_screen_one.blit(last_score_text, (220, 145))

        if Menu.score_history:
            top_scores = Menu.score_history[:5]
            for index, score in enumerate(top_scores, start=1):
                score_text = self.menu_font.render(
                    f"{index}. {score}", True, Config.BLACK)
                self.m_screen_one.blit(score_text, (220, 145 + index * 58))
        else:
            no_scores_text = self.menu_font.render(
                "NO SCORES YET", True, Config.BLACK)
            self.m_screen_one.blit(no_scores_text, (220, 220))

        self.m_screen_one.blit(self.back_text, self.back_rect)
