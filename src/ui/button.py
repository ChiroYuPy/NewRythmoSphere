import pygame


class Button:
    def __init__(self, x, y, width, height, press_action=None, unpress_action=None, offset_x=0, offset_y=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.press_action = press_action
        self.unpress_action = unpress_action
        self.clicked = False

    def update(self):
        if self.is_hovered():
            if self.is_pressed() != self.clicked:
                self.clicked = self.is_pressed()
                action = self.press_action if self.clicked else self.unpress_action
                if action: action()

    def is_hovered(self):
        mx, my = pygame.mouse.get_pos()
        return self.get_bounds().collidepoint(mx, my)

    def is_pressed(self):
        return pygame.mouse.get_pressed()[0]

    def get_bounds(self):
        return pygame.Rect(self.x - self.width / 2, self.y - self.height / 2, self.width, self.height)


class GraphicButton(Button):
    def __init__(self, x, y, width, height, press_action=None, unpress_action=None, color=(255, 0, 0), hover_color=(200, 0, 0), border_radius=0):
        super().__init__(x, y, width, height, press_action, unpress_action)
        self.color = color
        self.hover_color = hover_color
        self.border_radius = border_radius

    def draw(self, display):
        current_color = self.hover_color if self.is_hovered() else self.color
        pygame.draw.rect(display, current_color, self.get_bounds(), border_radius=self.border_radius)