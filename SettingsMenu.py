import pygame


class SettingsMenu:
    def __init__(self, app):
        self.app = app
        self.width = 360
        self.height = app.DISPLAY_HEIGHT  # Full height of the window
        self.rect = pygame.Rect(app.DISPLAY_WIDTH - self.width, 0, self.width,
                                self.height)  # Initialize the menu on the right side
        self.is_open = False  # Flag to track if the menu is open
        self.scroll_index = 0  # Current index of the menu item

        # Load options from the GameConfig
        self.display_width_options = app.config.get_options('display_width_options')
        self.display_height_options = app.config.get_options('display_height_options')
        self.max_fps_options = app.config.get_options('max_fps_options')

        # Initialize the menu items with the active values
        self.menu_items = [
            ("Display Width", self.display_width_options),
            ("Display Height", self.display_height_options),
            ("Max FPS", self.max_fps_options),
            ("Back", None)  # None indicates a back button
        ]

        # Set the current value indices based on active settings
        self.value_indices = [
            self.display_width_options.index(app.DISPLAY_WIDTH),
            self.display_height_options.index(app.DISPLAY_HEIGHT),
            self.max_fps_options.index(app.MAX_FPS)
        ]

        self.current_position = app.DISPLAY_WIDTH  # Start fully off-screen to the right
        self.target_position_x = app.DISPLAY_WIDTH  # Target position to keep the menu closed
        self.button_height = 40  # Height of each button
        self.button_color = (100, 100, 100, 127)  # Default button color
        self.hover_color = (200, 200, 200, 127)  # Color when hovering over button

    def update_parameter(self, index):
        param_name, values = self.menu_items[index]
        current_value = values[self.value_indices[index]]

        # Update the App parameters based on the selected index
        if param_name == "Display Width":
            self.app.DISPLAY_WIDTH = current_value
            self.app.config.set_parameter('game.display.width', current_value)  # Save to config
            self.app.display = pygame.display.set_mode((self.app.DISPLAY_WIDTH, self.app.DISPLAY_HEIGHT),
                                                       pygame.DOUBLEBUF)
            self.update_menu_position()
        elif param_name == "Display Height":
            self.app.DISPLAY_HEIGHT = current_value
            self.app.config.set_parameter('game.display.height', current_value)  # Save to config
            self.app.display = pygame.display.set_mode((self.app.DISPLAY_WIDTH, self.app.DISPLAY_HEIGHT),
                                                       pygame.DOUBLEBUF)
            self.update_menu_position()
        elif param_name == "Max FPS":
            self.app.MAX_FPS = current_value
            self.app.config.set_parameter('game.max_fps', current_value)  # Save to config

    def _smooth_scroll(self, current, target, dt, velocity_factor=8):
        if current != target:
            direction = target - current
            velocity = direction * velocity_factor
            current += velocity * dt
            if abs(direction) < 1:  # If close to the target, snap to it
                return target
        return current

    def toggle(self, value=None):
        self.is_open = value if value is not None else not self.is_open
        self.scroll_index = 0
        self.target_position_x = self.app.DISPLAY_WIDTH - self.width if self.is_open else self.app.DISPLAY_WIDTH

    def draw(self, display):
        # Update current position using smooth scroll
        dt = self.app.clock.get_time() / 1000.0  # Time since last frame in seconds
        self.current_position = self._smooth_scroll(self.current_position, self.target_position_x, dt)

        # Update the rectangle's right position
        self.rect.x = self.current_position

        # Only draw if the menu is open or currently moving
        if self.is_open or self.current_position < self.app.DISPLAY_WIDTH:
            # Draw menu background with SRCALPHA
            menu_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            menu_surface.fill((50, 50, 50, 127))  # Semi-transparent grey
            display.blit(menu_surface, self.rect.topleft)

            # Draw buttons
            for i, (text, value_list) in enumerate(self.menu_items):
                button_rect = pygame.Rect(self.rect.x + 10, self.rect.y + 10 + i * (self.button_height + 5),
                                          self.width - 20, self.button_height)

                # Change color if hovered or selected
                button_color = self.hover_color if i == self.scroll_index else self.button_color
                button_surface = pygame.Surface((button_rect.width, button_rect.height), pygame.SRCALPHA)
                button_surface.fill(button_color)
                display.blit(button_surface, button_rect.topleft)

                # Display the button text and its current value if applicable
                display_text = f"{text}: {self.menu_items[i][1][self.value_indices[i]]}" if value_list else text
                label = self.app.font24.render(display_text, True, (0, 0, 0))  # Black text
                label_rect = label.get_rect(center=button_rect.center)
                display.blit(label, label_rect)  # Draw the button text

            # Draw the single step indicator at the bottom of the menu
            if self.menu_items[self.scroll_index][1]:  # Only draw if the selected item has values
                indicator_y = self.rect.y + 10 + len(self.menu_items) * (
                        self.button_height + 5) + 40  # Position below buttons
                indicator_radius = 4
                selected_radius = 6
                step_spacing = 16  # Fixed spacing between points

                # Calculate the total width of the indicator area based on number of points
                total_width = (len(self.menu_items[self.scroll_index][1]) - 1) * step_spacing
                # Center the indicator within the menu
                indicator_x_start = self.rect.x + (self.width - total_width) // 2

                # Draw each point in the indicator
                for j in range(len(self.menu_items[self.scroll_index][1])):
                    point_color = (0, 255, 0) if j == self.value_indices[self.scroll_index] else (50, 50, 50)
                    radius = selected_radius if j == self.value_indices[self.scroll_index] else indicator_radius

                    # Calculate the position of each point
                    adjusted_position_x = indicator_x_start + j * step_spacing
                    pygame.draw.circle(display, point_color, (adjusted_position_x, indicator_y), radius)

    def handle_event(self, event):
        if self.is_open:
            # Handle arrow key events for navigating menu and changing values
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:  # Navigate up
                    self.scroll_index = (self.scroll_index - 1) % len(self.menu_items)
                elif event.key == pygame.K_DOWN:  # Navigate down
                    self.scroll_index = (self.scroll_index + 1) % len(self.menu_items)
                elif event.key == pygame.K_LEFT and self.scroll_index < len(
                        self.menu_items) - 1:  # Ensure not on "Back"
                    self.value_indices[self.scroll_index] = (self.value_indices[self.scroll_index] - 1) % len(
                        self.menu_items[self.scroll_index][1])
                    self.update_parameter(self.scroll_index)  # Update the parameter in App
                elif event.key == pygame.K_RIGHT and self.scroll_index < len(
                        self.menu_items) - 1:  # Ensure not on "Back"
                    self.value_indices[self.scroll_index] = (self.value_indices[self.scroll_index] + 1) % len(
                        self.menu_items[self.scroll_index][1])
                    self.update_parameter(self.scroll_index)  # Update the parameter in App
                elif event.key == pygame.K_ESCAPE:  # Close the menu with ESC
                    self.toggle()
                elif event.key == pygame.K_RETURN:  # Handle "Back" action
                    if self.scroll_index == len(self.menu_items) - 1:  # If "Back" is selected
                        self.toggle()  # Close the menu

    def update_menu_position(self):
        # Recalculate the menu position based on the new display width
        self.target_position_x = self.app.DISPLAY_WIDTH - self.width
        self.height = self.app.DISPLAY_HEIGHT

    def is_active(self):
        return self.is_open  # Return the active state of the menu
