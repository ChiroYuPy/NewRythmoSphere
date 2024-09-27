import pygame
import os
import shutil
from src.scene.Scene import Scene

class BeatMapEditorScreen(Scene):
    def __init__(self, app):
        super().__init__(app)
        self.app = app
        self.name = "editor"
        self.temp_folder = os.path.join(os.getcwd(), ".temp")
        os.makedirs(self.temp_folder, exist_ok=True)
        self.image_path = None
        self.song_path = None
        self.image_surface = None
        self.font = pygame.font.Font(None, 36)

    def handle_event(self, event):
        if event.type == pygame.DROPFILE:
            self.copy_and_store_file(event.file)

    def copy_and_store_file(self, file_path):
        if file_path.endswith(('.mp3', '.wav', '.ogg')):
            self.song_path = file_path
            self.copy_file_to_temp(file_path)
        elif file_path.endswith(('.png', '.jpeg', '.jpg')):
            self.image_path = file_path
            self.image_surface = self.load_and_resize_image(file_path)
            self.copy_image_to_temp(file_path)

    def load_and_resize_image(self, file_path):
        image = pygame.image.load(file_path)
        return self.resize_and_crop_image(image)

    def resize_and_crop_image(self, image):
        target_size = (1280, 720)
        image_ratio = image.get_width() / image.get_height()
        target_ratio = target_size[0] / target_size[1]
        if image_ratio > target_ratio:
            new_height = target_size[1]
            new_width = int(new_height * image_ratio)
        else:
            new_width = target_size[0]
            new_height = int(new_width / image_ratio)
        resized_image = pygame.transform.scale(image, (new_width, new_height))
        x_offset = (new_width - target_size[0]) // 2
        y_offset = (new_height - target_size[1]) // 2
        return resized_image.subsurface((x_offset, y_offset, target_size[0], target_size[1]))

    def copy_image_to_temp(self, file_path):
        new_path = os.path.join(self.temp_folder, os.path.basename(file_path))
        if os.path.exists(new_path):
            os.remove(new_path)
        pygame.image.save(self.image_surface, new_path)

    def copy_file_to_temp(self, file_path):
        new_path = os.path.join(self.temp_folder, os.path.basename(file_path))
        if os.path.exists(new_path):
            os.remove(new_path)
        shutil.copy(file_path, new_path)

    def draw(self, display):
        rect_width, rect_height = 320, 180
        rect_x = (self.app.DISPLAY_WIDTH - rect_width) // 2
        rect_y = (self.app.DISPLAY_HEIGHT - rect_height) // 2
        pygame.draw.rect(display, (255, 255, 255), (rect_x, rect_y, rect_width, rect_height))
        if self.image_surface:
            displayed_image = pygame.transform.scale(self.image_surface, (rect_width, rect_height))
            display.blit(displayed_image, (rect_x, rect_y))
        else:
            text_surface = self.font.render("Insérez une image", True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(rect_x + rect_width // 2, rect_y + rect_height // 2))
            display.blit(text_surface, text_rect)
        self.draw_file_names(display)

    def draw_file_names(self, display):
        if self.image_path:
            image_name = os.path.basename(self.image_path)
            image_text = self.font.render(f"Image: {image_name}", True, (255, 255, 255))
            text_rect = image_text.get_rect(center=(self.app.DISPLAY_WIDTH // 2, 50))
            display.blit(image_text, text_rect)
        if self.song_path:
            song_name = os.path.basename(self.song_path)
            song_text = self.font.render(f"Song: {song_name}", True, (255, 255, 255))
            text_rect = song_text.get_rect(center=(self.app.DISPLAY_WIDTH // 2, 100))
            display.blit(song_text, text_rect)

    def reset(self):
        pass

    def update(self, dt):
        pass