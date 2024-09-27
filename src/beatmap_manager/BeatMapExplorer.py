import math
import random

import pygame

from src.beatmap_manager.BeatMapButton import BeatMapButton
from src.ui.input import SearchInput


class BeatMapExplorer:
    def __init__(self, app, beatmap_clic_action):
        self.app = app
        self.beatmap_buttons = []
        self.beatmap_buttons_in_search = []
        self.beatmap_clic_action = beatmap_clic_action
        self.scroll, self.scroll_speed, self.target_scroll, self.scroll_velocity = 0, 96, 0, 0
        self.beatmap_button_selected = None
        self.button_width, self.button_height, self.button_margin = 400, 80, 4
        self.special_characters = "!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?~ "
        self._initialize_beatmap_buttons()
        self.search_input = SearchInput(self.app.font32, "assets/textures/icons/search.png", self.app.DISPLAY_WIDTH * 0.7, 48)

    def _initialize_beatmap_buttons(self):
        for beatmap in self.app.beatmaps:
            beatmap_button = BeatMapButton(0, 0, width=self.button_width, height=self.button_height, beatmap=beatmap,
                                           font=self.app.font24)
            beatmap_button.unpress_action = lambda diff_button=beatmap_button: self.select_beatmap(diff_button)
            self.beatmap_buttons.append(beatmap_button)
            self.beatmap_buttons_in_search.append(beatmap_button)

    def select_beatmap(self, beatmap_button):
        self._center_on_button(beatmap_button, self.app.DISPLAY_HEIGHT / 2)

        if self.beatmap_button_selected == beatmap_button:
            self.beatmap_clic_action(beatmap_button.beatmap)
        elif self.beatmap_button_selected:
            self.beatmap_button_selected.unselect()

        beatmap_button.select()

        self.beatmap_button_selected = beatmap_button

        if beatmap_button.beatmap.beatmap_name != self.app.beatmap_selected.beatmap_name:
            self.app.beatmap_selected = beatmap_button.beatmap
            self.app.music_player.load_music()
            self.app.music_player.play()
            self.app.music_player.set_cursor(self.app.beatmap_selected.preview_time)
        self.app.beatmap_selected = beatmap_button.beatmap

    def _center_on_button(self, beatmap_button, center_y):
        self.target_scroll = self.scroll - (beatmap_button.y - center_y)

    def update(self, dt):
        self._update_scroll(dt)
        self._update_buttons(dt)
        self.update_positions()

    def draw(self, display):
        self._draw_buttons(display)
        self._draw_ui(display)

    def _update_buttons(self, dt):
        for beatmap_button in self.beatmap_buttons_in_search:
            beatmap_button.update()

    def _update_scroll(self, dt):
        self.scroll = self._smooth_scroll(self.scroll, self.target_scroll, dt)
        for button in self.beatmap_buttons_in_search:
            button.offset_x = self._smooth_scroll(button.offset_x, button.target_offset_x, dt)
        self._handle_edge_scroll()

    def _smooth_scroll(self, current, target, dt, velocity_factor=8):
        if current != target:
            direction = target - current
            velocity = direction * velocity_factor
            current += velocity * dt
            if abs(direction) < 1:
                return target
        return current

    def _handle_edge_scroll(self):
        if self.beatmap_buttons_in_search:
            if self.beatmap_buttons_in_search[0].y > self.app.DISPLAY_HEIGHT / 2:
                self._center_on_button(self.beatmap_buttons_in_search[0], self.app.DISPLAY_HEIGHT / 2)
            elif self.beatmap_buttons_in_search[-1].y < self.app.DISPLAY_HEIGHT / 2:
                self._center_on_button(self.beatmap_buttons_in_search[-1], self.app.DISPLAY_HEIGHT / 2)

    def _draw_buttons(self, display):
        button_index_in_center = self._get_button_index_in_center()
        area_in_num_button = int(self.app.DISPLAY_HEIGHT // (self.button_height + self.button_margin))
        start_index = max(0, button_index_in_center - 1)
        end_index = min(len(self.beatmap_buttons_in_search), button_index_in_center + area_in_num_button + 1)

        for button in self.beatmap_buttons_in_search[start_index:end_index]:
            button.draw(display)

    def _draw_ui(self, display):
        self.search_input.draw(display)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse_scroll(event)
        elif event.type == pygame.KEYDOWN:
            self._handle_keyboard_event(event)

    def _handle_keyboard_event(self, event):
        # Allow only specific keys for navigation and functionality
        if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_F2]:
            self._handle_navigation_keys(event)
        elif event.key == pygame.K_BACKSPACE:
            self._handle_search_backspace()
        elif event.unicode:  # Ensure we're only processing unicode input
            # Allow letters, digits, and specific special characters
            if (event.unicode.isalpha() or event.unicode.isdigit() or
                    event.unicode in self.special_characters):
                self._add_search_char(event.unicode)

    def _handle_mouse_scroll(self, event):
        if event.button == 4:
            self.target_scroll += self.scroll_speed
        elif event.button == 5:
            self.target_scroll -= self.scroll_speed

    def _handle_navigation_keys(self, event):
        if event.key == pygame.K_UP:
            self.previous_beatmap()
        elif event.key == pygame.K_DOWN:
            self.next_beatmap()
        elif event.key == pygame.K_F2:
            self.select_random_beatmap()

    def _handle_search_backspace(self):
        self.search_input.remove_char()
        self.update_search()
        self.update_positions()

    def clear_search(self):
        self.search_input.clear_input()
        self.update_search()
        self.update_positions()

    def _add_search_char(self, char):
        self.search_input.add_char(char)
        self.update_search()
        self.update_positions()

    def update_search(self):
        search_input_value = self.search_input.get_input().lower()
        search_terms = search_input_value.split()

        self.beatmap_buttons_in_search = [
            button for button in self.beatmap_buttons
            if all(
                term in button.beatmap.beatmap_name.lower() or term in button.beatmap.difficulty_name.lower() for term
                in search_terms)
        ]

    def select_first_beatmap(self):
        if self.beatmap_buttons_in_search:
            self.select_beatmap(self.beatmap_buttons_in_search[0])

    def next_beatmap(self):
        self._navigate_beatmap(1)

    def previous_beatmap(self):
        self._navigate_beatmap(-1)

    def _navigate_beatmap(self, step):
        if not self.beatmap_button_selected:
            self.select_first_beatmap()
            return

        current_index = self.beatmap_buttons_in_search.index(self.beatmap_button_selected)
        next_index = (current_index + step) % len(self.beatmap_buttons_in_search)
        self.select_beatmap(self.beatmap_buttons_in_search[next_index])

    def select_random_beatmap(self):
        if self.beatmap_buttons_in_search:
            random_button = random.choice(self.beatmap_buttons_in_search)
            self.select_beatmap(random_button)

    def update_positions(self):
        menu_x, menu_y = self.app.DISPLAY_WIDTH * 0.9, 0
        y_offset = self.scroll + menu_y
        amplitude = -int(self.app.DISPLAY_WIDTH / 24)

        for beatmap_button in self.beatmap_buttons_in_search:
            angle = (y_offset / self.app.DISPLAY_HEIGHT) * math.pi
            beatmap_button.x = menu_x + (math.sin(angle) * amplitude) - beatmap_button.offset_x
            beatmap_button.y = y_offset
            y_offset += beatmap_button.height + self.button_margin

    def _get_button_index_in_center(self) -> int:
        return int(0 - self.scroll // (self.button_height + self.button_margin))