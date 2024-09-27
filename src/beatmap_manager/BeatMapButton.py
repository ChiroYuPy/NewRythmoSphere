from src.ui.button import GraphicButton


class BeatMapButton(GraphicButton):
    def __init__(self, x, y, width, height, beatmap, font):
        super().__init__(x, y, width, height, color=(127, 64, 160), border_radius=16)
        self.beatmap = beatmap
        self.font = font
        self.offset_x = 0
        self.scroll_x = 80
        self.target_offset_x = 0
        self.color = (127, 64, 160)
        self.initialize_text()

    def initialize_text(self):
        self.beatmap_text = self.font.render(self.beatmap.beatmap_name, True, (255, 255, 255))
        self.difficulty_text = self.font.render(self.beatmap.difficulty_name, True, (255, 255, 255))
        self.creator_text = self.font.render(self.beatmap.creator, True, (255, 255, 255))

    def select(self):
        self.target_offset_x = self.scroll_x
        self.color = (80, 54, 140)

    def unselect(self):
        self.target_offset_x = 0
        self.color = (127, 64, 160)

    def draw(self, display):
        super().draw(display)
        self._draw_texts(display)

    def _draw_texts(self, display):
        display.blit(self.beatmap_text, (self.x - self.width / 2 + 4, self.y - self.height / 2 + 6))
        display.blit(self.difficulty_text, (self.x - self.width / 2 + 4, self.y - self.height / 2 + 30))
        display.blit(self.creator_text, (self.x - self.width / 2 + 4, self.y - self.height / 2 + 54))