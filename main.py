import pygame as pg

def main():
    pg.init()
    #-----------------------משתנים----------------------
    width = 720
    height = 480
    screen = pg.display.set_mode((width, height))
    clock = pg.time.Clock()

    running = True

    player = pg.Rect(100, 200, 50, 50)

    speed = 5
    velocity_y = 0.0
    gravity = 0.8
    jump_speedgravity = -16

    scroll_line = 100
    fall_line = 200

    target_ofplatforms = 6

    platform_color = (60, 170, 220)
    platforms = [
        pg.Rect(0, height - 20, width, 20),
        pg.Rect(60, height - 140, 120, 16),
        pg.Rect(240, height - 260, 120, 16),
        pg.Rect(140, height - 380, 120, 16),
    ]
    #---------------------------------------------
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        keys = pg.key.get_pressed()
        step_x = 0
        step_y = 0

        # -------------------תנועה לפי מקשים----------------
        if keys[pg.K_LEFT]:
            step_x -= speed
        if keys[pg.K_RIGHT]:
            step_x += speed

        # תנועה אופקית + תיקון אופקי מול פלטפורמות
        player.x += step_x
        for each_rect in platforms:
            if player.colliderect(each_rect):
                if step_x > 0:
                    player.right = each_rect.left
                elif step_x < 0:
                    player.left = each_rect.right

        # פיזיקה אנכית
        step_y += velocity_y
        velocity_y += gravity
        player.y += step_y

        # קוליזיות אנכיות
        on_ground = False
        for each_rect in platforms:
            if player.colliderect(each_rect):
                if step_y > 0:
                    player.bottom = each_rect.top
                    velocity_y = 0
                    on_ground = True
                elif step_y < 0:
                    player.top = each_rect.bottom
                    velocity_y = 0

        # קפיצה
        if on_ground and keys[pg.K_SPACE]:
            velocity_y = jump_speedgravity

        # --------- גלילת נפילה (שומר על השחקן בפריים בזמן ירידה) ----------
        if player.bottom > fall_line and step_y > 0:
            scroll = player.bottom - fall_line
            player.bottom = fall_line
            for plat in platforms:
                plat.y -= scroll

        # --------- גלילת עלייה (כשעולים מעל קו הגלילה) ----------
        if player.top < scroll_line and step_y < 0:
            scroll = scroll_line - player.top
            player.top = scroll_line
            for each_rect in platforms:
                each_rect.y += scroll

        # סינון פלטפורמות שנפלו מתחת למסך (אופציונלי)
        platforms_onthescreen = []
        for each_rect in platforms:
            if each_rect.top < height:
                platforms_onthescreen.append(each_rect)
        platforms = platforms_onthescreen

        # -------------------תיקון גבולות (רק X!)-------------------
        if player.left < 0:
            player.left = 0
        if player.right > width:
            player.right = width

        #-------------------ציור על המסך-------------------
        screen.fill((0, 0, 0))
        for each_rect in platforms:
            pg.draw.rect(screen, platform_color, each_rect)
        pg.draw.rect(screen, (50, 245, 125), player)
        pg.display.flip()
        clock.tick(60)

    pg.quit()

if __name__ == "__main__":
    main()
