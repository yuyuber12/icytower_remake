import pygame

#Game settings:
pygame.init()
WIDTH = 720
HEIGHT = 480
FPS = 60
CLOCK = pygame.time.Clock()

DARK_COLOR = (245, 245, 245)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CURRENT_FONT = pygame.font.Font("Fonts/Grandboom Demo.otf", 45)
FINGER_IMAGE = pygame.image.load("Menu_images/finger-selector.png")
FINGER_IMAGE= pygame.transform.scale(FINGER_IMAGE, ((WIDTH // 5 -75) , (HEIGHT// 5 -50)))
