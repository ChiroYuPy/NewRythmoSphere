import pygame

from src.beatmap_manager.BeatMapExplorer import BeatMapExplorer
from src.scene.Scene import Scene
from src.ui.button import GraphicButton
from src.ui.label import Label


class BeatMapSelectionScreen(Scene):
    def __init__(self, app):
        super().__init__(app)
        self.name = "selection"
        self.beatmap_explorer = BeatMapExplorer(self.app, self.launch_beatmap)
        self.return_button = GraphicButton(40, self.app.DISPLAY_HEIGHT - 40, 64, 64)
        self.return_button.press_action = lambda e="main": self.app.switch_scene(e)
        self.buttons = [self.return_button]

        # Labels
        info_color = (80, 120, 160)
        self.labels = {
            "beatmap_name": Label("", self.app.font32, info_color),
            "difficulty_name": Label("", self.app.font32, info_color),
            "artist": Label("", self.app.font32, info_color),
            "creator": Label("", self.app.font32, info_color),
            "preview_time": Label("", self.app.font32, info_color)
        }

    def launch_beatmap(self, beatmap):
        self.app.music_player.stop()
        self.app.switch_scene("game")

    def update(self, dt):
        self.beatmap_explorer.update(dt)
        for button in self.buttons:
            button.update()

        self.labels["beatmap_name"].update(f"name: {self.app.beatmap_selected.beatmap_name}")
        self.labels["difficulty_name"].update(f"difficulty: {self.app.beatmap_selected.difficulty_name}")
        self.labels["artist"].update(f"artist: {self.app.beatmap_selected.artist}")
        self.labels["creator"].update(f"creator: {self.app.beatmap_selected.creator}")
        self.labels["preview_time"].update(f"preview time: {self.app.beatmap_selected.preview_time:.2f} s")

        self.labels["beatmap_name"].rect.topleft = 60, self.app.DISPLAY_HEIGHT / 2 - 60
        self.labels["difficulty_name"].rect.topleft = 60, self.app.DISPLAY_HEIGHT / 2 - 30
        self.labels["artist"].rect.topleft = 60, self.app.DISPLAY_HEIGHT / 2
        self.labels["creator"].rect.topleft = 60, self.app.DISPLAY_HEIGHT / 2 + 30
        self.labels["preview_time"].rect.topleft = 60, self.app.DISPLAY_HEIGHT / 2 + 60

    def draw(self, display):
        self.beatmap_explorer.draw(display)
        for button in self.buttons:
            button.draw(display)
        for label in self.labels.values():
            label.draw(display)


    def handle_event(self, event):
        self.beatmap_explorer.handle_event(event)
        if event.type == pygame.K_ESCAPE:
            self.beatmap_explorer.clear_search()
            print(len(self.beatmap_explorer.search_input.get_input()))
            if len(self.beatmap_explorer.search_input.get_input()) < 2:
                self.app.switch_scene("main")

    def reset(self):
        pass