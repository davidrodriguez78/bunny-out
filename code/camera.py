from setting import *

# Camera class
class Camera:
    def __init__(self, width, height, level_width, level_height):
        self.offset = pygame.Vector2()
        self.width = width
        self.height = height
        
        self.level_width = level_width
        self.level_height = level_height

    def follow(self, target):
        self.offset.x = target.rect.centerx - self.width / 2
        self.offset.y = target.rect.centery - self.height / 2
        
        # limit the cam horizontal
        self.offset.x = max(0, self.offset.x)
        self.offset.x = min(self.offset.x, self.level_width - self.width)
        
        # limit the cam vertical
        self.offset.y = max(0, self.offset.y)
        self.offset.y = min(self.offset.y, self.level_height - self.height)

    def draw(self, group, surface):
        for sprite in group:
            screen_pos = sprite.rect.topleft - self.offset
            surface.blit(sprite.image, screen_pos)