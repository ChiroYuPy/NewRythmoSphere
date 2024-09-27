import pygame


class Input:
    def __init__(self):
        self.text = ""

    def clear_input(self):
        self.text = ""

    def add_char(self, char):
        self.text += char

    def remove_char(self):
        self.text = self.text[:-1]

    def get_input(self):
        return self.text


class SearchInput(Input):
    def __init__(self, font, image_path, x, y):
        super().__init__()
        self.font = font
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*0.4, self.image.get_height()*0.4))
        self.x = x
        self.y = y

    def draw(self, display):
        display.blit(self.image, (self.x-self.image.get_width(), self.y - 6))
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        display.blit(text_surface, (self.x, self.y))