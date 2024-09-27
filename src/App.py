import pygame
from random import choice

from GameConfig import GameConfig
from SettingsMenu import SettingsMenu
from src.beatmap_manager.BeatMapLoader import BeatmapLoader
from src.beatmap_manager.MusicPlayer import MusicPlayer
from src.scene.BeatMapEditorScene import BeatMapEditorScreen
from src.scene.BeatMapSelectionScene import BeatMapSelectionScreen
from src.scene.GameScene import GameScene
from src.scene.MainScene import MainScreen
from src.ui.cursor import Cursor
from src.ui.label import Label


class App:
    def __init__(self):
        # Load configuration
        self.config = GameConfig('config.yml')  # Path to your YAML config file

        # Access parameters using dot notation
        self.DISPLAY_WIDTH = self.config.get_parameter('game.display.width')
        self.DISPLAY_HEIGHT = self.config.get_parameter('game.display.height')
        self.MAX_FPS = self.config.get_parameter('game.max_fps')
        self.CAPTION = f"{self.config.get_parameter('game.name')} - {self.config.get_parameter('game.version')}"

        self.settings_menu = SettingsMenu(self)

        # Pygame setup
        self.running = True
        self.display = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT), pygame.DOUBLEBUF)
        pygame.display.set_caption(self.CAPTION)
        self.clock = pygame.time.Clock()

        # Fonts
        self.font96 = pygame.font.Font('assets/fonts/Mouldy.ttf', 96)
        self.font80 = pygame.font.Font('assets/fonts/Mouldy.ttf', 80)
        self.font64 = pygame.font.Font('assets/fonts/Mouldy.ttf', 64)
        self.font48 = pygame.font.Font('assets/fonts/Mouldy.ttf', 48)
        self.font32 = pygame.font.Font('assets/fonts/Mouldy.ttf', 32)
        self.font24 = pygame.font.Font('assets/fonts/Mouldy.ttf', 24)
        self.font16 = pygame.font.Font('assets/fonts/Mouldy.ttf', 16)

        # Beatmaps
        self.beatmap_loader = BeatmapLoader()
        self.beatmaps = self.beatmap_loader.load_beatmaps("beatmaps/")
        self.beatmap_selected = choice(self.beatmaps)
        self.music_player = MusicPlayer(self)
        self.music_player.load_music()
        self.music_player.play()

        # Scenes
        self.main_scene = MainScreen(self)
        self.beatmap_selection_scene = BeatMapSelectionScreen(self)
        self.beatmap_editor_scene = BeatMapEditorScreen(self)
        self.game_scene = GameScene(self)

        self.current_scene = MainScreen(self)

        # Labels
        info_color = (127, 127, 127)
        self.scene_label = Label("", self.font16, info_color, 0, 20)
        self.fps_label = Label("", self.font16, info_color, 0, 0)
        self.beatmap_label = Label("", self.font16, info_color, 0, 40)
        self.labels = [self.scene_label, self.fps_label, self.beatmap_label]

        # Cursor
        pygame.mouse.set_visible(False)
        self.menu_cursor = Cursor("assets/textures/menu-cursor.png", scale=0.1, offset_x=-4, offset_y=-2)

    def run(self):
        while self.running:
            # Global update
            self.clock.tick(self.MAX_FPS)
            dt = self.clock.get_time() / 1000.0
            self.update(dt)

            # Global render
            self.display.fill((0, 0, 0))
            self.draw(self.display)
            pygame.display.update()

            # Global events
            for event in pygame.event.get():
                self.handle_event(event)

    def draw(self, display):
        self.current_scene.draw(display)
        for label in self.labels:
            label.draw(display)

        self.settings_menu.draw(display)
        self.menu_cursor.draw(display)

    def update(self, dt):
        self.music_player.update(dt)
        mouse_x, mouse_y = pygame.mouse.get_pos()

        self.current_scene.update(dt)
        self.scene_label.update(f"Scene: {self.current_scene.name}")
        self.fps_label.update(f"FPS: {int(min(self.clock.get_fps(), self.MAX_FPS))}/{self.MAX_FPS}")
        self.beatmap_label.update(
            f"Beatmap: {self.beatmap_selected.beatmap_name}" if self.beatmap_selected else "Beatmap: No")

        self.menu_cursor.update(mouse_x, mouse_y)
        if pygame.mouse.get_focused():
            self.menu_cursor.set_show(True)
        else:
            self.menu_cursor.set_show(False)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.quit()

        # Check for the key combination (LCTRL + o) to toggle settings menu
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if event.key == pygame.K_o and keys[pygame.K_LCTRL]:
                self.settings_menu.toggle()
            elif event.key == pygame.K_ESCAPE:
                self.settings_menu.toggle(False)

        # Handle events for the settings menu if it is active
        if self.settings_menu.is_active():
            self.settings_menu.handle_event(event)
        else:
            self.menu_cursor.handle_event(event)
            self.current_scene.handle_event(event)

    def quit(self):
        self.running = False

    def switch_scene(self, scene: str):
        match scene:
            case self.main_scene.name:
                self.current_scene = self.main_scene
            case self.beatmap_selection_scene.name:
                self.current_scene = self.beatmap_selection_scene
            case self.beatmap_editor_scene.name:
                self.current_scene = self.beatmap_editor_scene
            case self.game_scene.name:
                self.current_scene = self.game_scene
            case _:
                raise ValueError(f"Scene {scene} does not exist.")
        self.current_scene.reset()
