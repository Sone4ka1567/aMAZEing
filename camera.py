import pygame
import settings as const


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, player):
        return player.rect.move(self.camera.topleft)

    def update(self, player):
        x = -player.rect.x + const.WIDTH // 2
        y = -player.rect.y + const.HEIGHT // 2

        x = min(0, x)  # настрои слева
        y = min(0, y)  # настроим сверху
        x = max(-(self.width - const.WIDTH), x)  # настроим справа
        y = max(-(self.height - const.HEIGHT), y)  # настроим снизу
        self.camera = pygame.Rect(x, y, self.width, self.height)
