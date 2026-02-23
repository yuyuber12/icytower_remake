# import Program2

import pygame
from Screens.Game import Game
from Screens.Instructions import Instructions
from Screens.Menu import Menu
from settings import Config

screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))

if __name__ == "__main__":
    while True:  # לולאה אינסופית שמאפשרת לחזור ל-Menu
        menu = Menu(screen)

        result_Menu = menu.run()
        if result_Menu == "exit":
            break  # יוצאים מהלולאה ומסיימים את התוכנית

        game = Game(screen, menu)
        result_Game = game.run()
        if result_Game != "back_to_menu":
            break

        # TODO לבדוק איך לצאת מהלולאה אחרי שיוצאים מהתפריט , כי בינתיים זה חוזר שוב למשחק
        # נראה לי שהצלחתי לשנות את הסגירת הMenu
