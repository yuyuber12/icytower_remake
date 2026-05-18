
import pygame as pg
from pygame import Surface

from DataModels.GameObject import GameObject


# Represent the player entity and its drawable collision rectangle.
class Player(GameObject):
    # Initialize player geometry, style, and rectangle state.
    def __init__(self, width_position, height_position, player_width, player_height, color, border_radius):
        super().__init__(width_position, height_position,
                         player_width, player_height, color, border_radius)
        self._border_radius = border_radius
        self._color = color
        self.facing_right = True
        self.animation_tick = 0
        self.current_state = "idle"
        self.current_frame_index = 0
        self.render_width = max(int(player_width * 1.45), 68)
        self.render_height = max(int(player_height * 1.65), 82)

        # Create a concrete rectangle used for movement and rendering.
        self.player_rect: pg.Rect = pg.Rect(
            width_position, height_position, player_width, player_height)
        self.sprite_frames = self.build_sprite_frames()
        self.render_frames = self.build_render_frames()

    # Build reusable sprite frames for idle, run, and jump states.
    def build_sprite_frames(self):
        ground_frame = self.create_sprite_frame(blink=False)
        jump_frame = self.create_sprite_frame(airborne=True)
        return {
            "idle": [ground_frame],
            "run": [ground_frame],
            "jump": [jump_frame],
        }

    # Pre-build scaled and flipped frames once so rendering stays stable.
    def build_render_frames(self):
        render_frames = {}
        for state, frames in self.sprite_frames.items():
            right_frames = [
                pg.transform.scale(
                    frame,
                    (self.render_width, self.render_height),
                )
                for frame in frames
            ]
            left_frames = [pg.transform.flip(frame, True, False)
                           for frame in right_frames]
            render_frames[state] = {
                "right": right_frames,
                "left": left_frames,
            }

        return render_frames

    # Draw a stylized sprite frame onto a transparent surface.
    def create_sprite_frame(self, airborne=False, blink=False, lean=0):
        frame = pg.Surface(
            (self.player_rect.width, self.player_rect.height), pg.SRCALPHA)

        outline_color = (42, 27, 24)
        skin_color = (238, 196, 164)
        hair_color = (92, 54, 38)
        jacket_color = (214, 74, 124)
        shirt_color = (245, 240, 222)
        pants_color = (48, 48, 56)
        shoe_color = (250, 250, 250)
        headband_color = (255, 210, 70)
        shadow_color = (20, 10, 10, 70)

        pg.draw.ellipse(frame, shadow_color, (10, 41, 30, 6))

        head_rect = pg.Rect(14 + lean, 5, 22, 18)
        torso_rect = pg.Rect(12 + lean, 21, 26, 16)

        pg.draw.ellipse(frame, outline_color, head_rect)
        pg.draw.ellipse(frame, skin_color, head_rect.inflate(-3, -3))

        hair_rect = pg.Rect(head_rect.left + 1,
                            head_rect.top, head_rect.width - 2, 9)
        pg.draw.ellipse(frame, hair_color, hair_rect)
        pg.draw.rect(frame, headband_color, (head_rect.left + 2,
                     head_rect.top + 6, head_rect.width - 4, 3), border_radius=2)

        if blink:
            pg.draw.line(frame, outline_color,
                         (21 + lean, 15), (25 + lean, 15), 2)
        else:
            pg.draw.circle(frame, outline_color, (23 + lean, 15), 1)

        pg.draw.arc(frame, outline_color, (19 + lean, 15, 8, 5), 3.6, 5.8, 1)

        pg.draw.rect(frame, outline_color, torso_rect, border_radius=6)
        pg.draw.rect(frame, jacket_color,
                     torso_rect.inflate(-2, -2), border_radius=5)
        pg.draw.rect(frame, shirt_color,
                     (21 + lean, 22, 8, 14), border_radius=3)
        pg.draw.line(frame, outline_color, (25 + lean, 24), (25 + lean, 34), 1)

        left_arm_start = (14 + lean, 24)
        right_arm_start = (36 + lean, 24)
        left_arm_end = (9 + lean, 31)
        right_arm_end = (41 + lean, 31)
        pg.draw.line(frame, outline_color, left_arm_start, left_arm_end, 5)
        pg.draw.line(frame, outline_color, right_arm_start, right_arm_end, 5)
        pg.draw.line(frame, skin_color, left_arm_start, left_arm_end, 3)
        pg.draw.line(frame, skin_color, right_arm_start, right_arm_end, 3)

        hip_left = (21, 35)
        hip_right = (29, 35)
        left_leg_end = (20, 45)
        right_leg_end = (30, 45)

        pg.draw.line(frame, outline_color, hip_left, left_leg_end, 6)
        pg.draw.line(frame, outline_color, hip_right, right_leg_end, 6)
        pg.draw.line(frame, pants_color, hip_left, left_leg_end, 4)
        pg.draw.line(frame, pants_color, hip_right, right_leg_end, 4)

        pg.draw.line(frame, shoe_color, (left_leg_end[0] - 3, left_leg_end[1]),
                     (left_leg_end[0] + 4, left_leg_end[1]), 3)
        pg.draw.line(frame, shoe_color, (right_leg_end[0] - 3, right_leg_end[1]),
                     (right_leg_end[0] + 4, right_leg_end[1]), 3)

        return frame

    # Update sprite state based on current movement.
    def update_animation(self, velocity_x, velocity_y, on_ground):
        self.animation_tick += 1

        if velocity_x > 0.55:
            self.facing_right = True
        elif velocity_x < -0.55:
            self.facing_right = False

        if not on_ground:
            self.current_state = "jump"
            jump_frames = self.sprite_frames["jump"]
            if velocity_y < 0:
                self.current_frame_index = 0
            else:
                self.current_frame_index = min(1, len(jump_frames) - 1)
            return

        run_start_speed = 4.2
        run_stop_speed = 3.0
        should_run = abs(velocity_x) > run_start_speed
        if self.current_state == "run" and abs(velocity_x) > run_stop_speed:
            should_run = True

        if should_run:
            self.current_state = "run"
            self.current_frame_index = 0
            return

        self.current_state = "idle"
        self.current_frame_index = 0

    # Draw the player on the target surface.
    def draw(self, window: Surface):
        direction = "right" if self.facing_right else "left"
        current_frames = self.render_frames[self.current_state][direction]
        sprite = current_frames[self.current_frame_index]
        sprite_rect = sprite.get_rect(
            midbottom=(self.player_rect.centerx, self.player_rect.bottom + 4)
        )
        window.blit(sprite, sprite_rect.topleft)
