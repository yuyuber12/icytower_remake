import pygame

# Initialize pygame resources used by shared game configuration.
pygame.init()

# Define global display and timing settings.
WIDTH = 720
HEIGHT = 520
FPS = 60
CLOCK = pygame.time.Clock()

# Define shared color constants.
DARK_COLOR = (245, 245, 245)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load shared fonts and UI assets used across screens.
CURRENT_FONT = pygame.font.Font("Fonts/BlankRiver.ttf", 45)
CURRENT_FONT_BIGGER = pygame.font.Font("Fonts/BlankRiver.ttf", 75)
FINGER_IMAGE = pygame.image.load("Menu_images/finger-selector.png")
FINGER_IMAGE = pygame.transform.scale(
    FINGER_IMAGE, ((WIDTH // 5 - 75), (HEIGHT // 5 - 50)))
