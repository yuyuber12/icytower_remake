import pygame as pg


# Initialize the prototype game loop and demonstrate core movement/platform logic.
def main():
    # Initialize pygame and create the main window resources.
    pg.init()

    # Configure base screen and timing values.
    width = 720
    height = 480
    screen = pg.display.set_mode((width, height))
    clock = pg.time.Clock()

    # Define the initial game state.
    running = True

    player = pg.Rect(100, 200, 50, 50)

    # Configure player movement physics.
    speed = 5
    velocity_y = 0.0
    gravity = 0.8
    jump_speedgravity = -16

    # Configure camera helper lines for vertical scrolling.
    scroll_line = 100
    fall_line = 200

    # Configure platform generation and visual setup.
    target_ofplatforms = 6

    platform_color = (60, 170, 220)
    platforms = [
        pg.Rect(0, height - 20, width, 20),
        pg.Rect(60, height - 140, 120, 16),
        pg.Rect(240, height - 260, 120, 16),
        pg.Rect(140, height - 380, 120, 16),
    ]

    # Run the main frame loop.
    while running:
        # Process quit events.
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # Read player input and prepare per-frame movement deltas.
        keys = pg.key.get_pressed()
        step_x = 0
        step_y = 0

        # Apply horizontal input.
        if keys[pg.K_LEFT]:
            step_x -= speed
        if keys[pg.K_RIGHT]:
            step_x += speed

        # Move horizontally and resolve horizontal platform collisions.
        player.x += step_x
        for each_rect in platforms:
            if player.colliderect(each_rect):
                if step_x > 0:
                    player.right = each_rect.left
                elif step_x < 0:
                    player.left = each_rect.right

        # Apply vertical physics and movement.
        step_y += velocity_y
        velocity_y += gravity
        player.y += step_y

        # Resolve vertical collisions and detect whether the player is grounded.
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

        # Trigger jump when grounded and space is pressed.
        if on_ground and keys[pg.K_SPACE]:
            velocity_y = jump_speedgravity

        # Scroll world upward on descent to keep the player inside the camera area.
        if player.bottom > fall_line and step_y > 0:
            scroll = player.bottom - fall_line
            player.bottom = fall_line
            for plat in platforms:
                plat.y -= scroll

        # Scroll world downward on ascent after crossing the scroll line.
        if player.top < scroll_line and step_y < 0:
            scroll = scroll_line - player.top
            player.top = scroll_line
            for each_rect in platforms:
                each_rect.y += scroll

        # Keep only platforms that are still visible on screen.
        platforms_onthescreen = []
        for each_rect in platforms:
            if each_rect.top < height:
                platforms_onthescreen.append(each_rect)
        platforms = platforms_onthescreen

        # Clamp player within horizontal screen bounds.
        if player.left < 0:
            player.left = 0
        if player.right > width:
            player.right = width

        # Render all frame elements.
        screen.fill((0, 0, 0))
        for each_rect in platforms:
            pg.draw.rect(screen, platform_color, each_rect)
        pg.draw.rect(screen, (50, 245, 125), player)
        pg.display.flip()
        clock.tick(60)

    # Shut down pygame cleanly.
    pg.quit()


# Launch the prototype only when running this file directly.
if __name__ == "__main__":
    main()
