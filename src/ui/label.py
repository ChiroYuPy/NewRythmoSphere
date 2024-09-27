class Label:
    def __init__(self, text, font, color=(255, 255, 255), x=0.0, y=0.0):
        self.color = color
        self.text = text

        self.font = font
        self.rendered_text = self.font.render(text, True, self.color)

        self.rect = self.rendered_text.get_rect(topleft=(x, y))

    def update(self, text):
        if text != self.text:
            self.text = text
            self.rendered_text = self.font.render(text, True, self.color)
            self.rect = self.rendered_text.get_rect(topleft=self.rect.topleft)

    def draw(self, surface):
        surface.blit(self.rendered_text, self.rect)