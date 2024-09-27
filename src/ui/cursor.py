import pygame


class Cursor:
    def __init__(self, image_path, scale=1.0, offset_x=0, offset_y=0):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * scale), int(self.image.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.show = True

    def update(self, x, y):
        self.rect.topleft = (x + self.offset_x, y + self.offset_y)

    def set_show(self, show):
        self.show = show

    def draw(self, display):
        if self.show:
            display.blit(self.image, self.rect.topleft)

    def handle_event(self, event):
        pass