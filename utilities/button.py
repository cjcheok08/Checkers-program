from constants import SCREEN_WIDTH


class Button:
    def __init__(self, image, coordinates):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = coordinates  # (x, y)
        self.clicked = False

    def draw_self(self, screen):
        x, y = self.rect.topleft
        screen.blit(self.image, (x, y))

    def draw_self_center(self, screen):
        _, y = self.rect.topleft
        x = SCREEN_WIDTH / 2 - self.image.get_width() / 2
        self.rect.topleft = (x, y)
        screen.blit(self.image, (x, y))

