# import Program2

import pygame
from Logic.Game import Game
from UI.Menu import Menu
from settings import Config

screen = pygame.display.set_mode((Config.WIDTH , Config.HEIGHT))

if __name__ == "__main__":
    while True:  # לולאה אינסופית שמאפשרת לחזור ל-Menu
        menu = Menu(screen)
        menu.run()

        game = Game(screen, menu)
        result_Game = game.run()
        result_Menu = menu.run()

        if result_Game != "back_to_menu":
            break  # אם המשחק הסתיים בדרך אחרת - יציאה מהלולאה
        # if result_Menu != "exit":
           #TODO לבדוק איך לצאת מהלולאה אחרי שיוצאים מהתפריט , כי בינתיים זה חוזר שוב למשחק

        #בדיקה בדיקה





