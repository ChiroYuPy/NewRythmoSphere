import math
from src.scene.Scene import Scene
from src.ui.button import GraphicButton

import pygame


class DynamicButton(GraphicButton):
    def __init__(self, x, y, font, text="", icon_path=None):
        self.icon = pygame.image.load(icon_path).convert_alpha() if icon_path else None
        if self.icon:
            self.icon = pygame.transform.scale(self.icon, (self.icon.get_width(), self.icon.get_height()))
        self.base_size = self.icon.get_height() * 1.5
        super().__init__(x, y, self.base_size, self.base_size)
        self.original_width = self.base_size
        self.base_height = self.base_size
        self.font = font
        self.text = text
        self.target_width = self.base_size
        self.velocity = 1000

        original_text_surface = self.font.render(self.text, True, pygame.Color('white'))
        text_rect = original_text_surface.get_rect()
        self.hover_added_width = text_rect.width + 8

    def draw(self, display):
        super().draw(display)

        content_y = self.y
        icon_rect = self.icon.get_rect(center=(self.x, content_y))
        icon_left_position_x = self.x - (self.icon.get_width() + self.width - self.original_width) / 2
        icon_rect.topleft = (icon_left_position_x, content_y - self.icon.get_height() / 2)  # Center the icon vertically

        # Calculate the rotation factor based on current width
        percentage = (self.width - self.original_width) / self.hover_added_width
        percentage = min(max(percentage, 0), 1)  # Clamp between 0 and 1
        max_rotation_angle = -90  # Maximum rotation angle in degrees
        rotation_angle = percentage * max_rotation_angle  # Calculate rotation angle

        # Rotate the icon
        rotated_icon = pygame.transform.rotate(self.icon, -rotation_angle)  # Negative for clockwise rotation
        rotated_icon_rect = rotated_icon.get_rect(center=icon_rect.center)

        # Draw the rotated icon
        display.blit(rotated_icon, rotated_icon_rect)

        text_surf = self.font.render(self.text, True, pygame.Color('white'))

        if text_surf:
            cropped_width = self.width - self.base_size
            cropped_surf = pygame.Surface((cropped_width, text_surf.get_height()), pygame.SRCALPHA)

            # Blit the text to the cropped surface
            cropped_surf.blit(text_surf, (0, 0))

            text_rect = cropped_surf.get_rect()
            text_rect.x = icon_left_position_x + self.icon.get_width()  # Position text next to the icon
            text_rect.centery = content_y

            display.blit(cropped_surf, text_rect)


class InteractiveButtonMenu:
    def __init__(self, app):
        self.app = app
        self.buttons = []

    def add_button(self, x, text, icon_path, press_action, color, hover_color):
        button = DynamicButton(x, self.app.DISPLAY_HEIGHT / 2, font=self.app.font48, text=text, icon_path=icon_path)
        button.color = color
        button.hover_color = hover_color
        button.press_action = press_action
        self.buttons.append(button)

    def update_positions(self, dt):
        center_x = self.app.DISPLAY_WIDTH / 2
        for button in self.buttons:
            if button.is_hovered():
                # Set target width to accommodate text and icon on hover
                button.target_width = button.original_width + button.hover_added_width
            else:
                button.target_width = button.original_width

        total_width = sum(button.width for button in self.buttons)
        current_x = center_x - total_width / 2

        for button in self.buttons:
            button.x = current_x + button.width / 2
            button.y = self.app.DISPLAY_HEIGHT / 2
            current_x += button.width

            if button.width != button.target_width:
                width_diff = button.target_width - button.width
                step = button.velocity * dt
                if abs(width_diff) < step:  # Close enough to the target
                    button.width = button.target_width
                else:
                    button.width += math.copysign(step, width_diff)

    def update(self, dt):
        self.update_positions(dt)
        for button in self.buttons:
            button.update()  # Pass dt to update method of buttons

    def draw(self, display):
        for button in self.buttons:
            button.draw(display)  # This will draw both the button and its text


class MainScreen(Scene):
    def __init__(self, app):
        super().__init__(app)
        self.app = app
        self.name = "main"

        # Create the button menu
        self.button_menu = InteractiveButtonMenu(app)

        # Add buttons to the menu

        self.button_menu.add_button(
            x=0,
            text="Settings",
            icon_path='assets/textures/icons/settings.png',
            press_action=self.app.settings_menu.toggle,
            color=(96, 96, 96),
            hover_color=(64, 64, 64)
        )

        self.button_menu.add_button(
            x=0,
            text="Play",
            icon_path='assets/textures/icons/play.png',
            press_action=lambda e="selection": self.app.switch_scene(e),
            color=(50, 200, 30),
            hover_color=(40, 160, 20)
        )

        self.button_menu.add_button(
            x=0,
            text="Edit",
            icon_path='assets/textures/icons/editor.png',
            press_action=lambda e="editor": self.app.switch_scene(e),
            color=(50, 30, 200),
            hover_color=(40, 20, 160)
        )

        self.button_menu.add_button(
            x=0,
            text="Quit",
            icon_path='assets/textures/icons/cross-circle.png',
            press_action=lambda: self.app.quit(),
            color=(200, 30, 30),
            hover_color=(160, 20, 20)
        )

    def update(self, dt):
        self.button_menu.update(dt)

    def draw(self, display):
        self.button_menu.draw(display)

    def handle_event(self, event):
        pass

    def reset(self):
        pass
