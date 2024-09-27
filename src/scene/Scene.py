class Scene:
    def __init__(self, app):
        self.app = app
        self.name = "Scene is a Parent Class !"

    def reset(self):
        raise NotImplementedError("Must be implement in children classes.")

    def update(self, dt):
        raise NotImplementedError("Must be implement in children classes.")

    def draw(self, display):
        raise NotImplementedError("Must be implement in children classes.")

    def handle_event(self, event):
        raise NotImplementedError("Must be implement in children classes.")
