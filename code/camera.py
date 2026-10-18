from setting import *

# Camera class
class Camera:
    def __init__(self, width, height):
        self.offset = pygame.Vector2()
        self.width = width
        self.height = height

    def follow(self, target):
        self.offset.x = target.rect.centerx - self.width / 2
        self.offset.y = target.rect.centery - self.height / 2

    def draw(self, group, surface):
        for sprite in group:
            screen_pos = sprite.rect.topleft - self.offset
            surface.blit(sprite.image, screen_pos)