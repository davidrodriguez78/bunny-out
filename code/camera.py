from setting import *

# Camera class
class Camera:
    def __init__(self, width, height, level_width, level_height):
        self.width = width
        self.height = height
        
        self.level_width = level_width
        self.level_height = level_height
        
        self.offset = pygame.Vector2()
        
        # Actual Room
        self.room_x = 0
        self.room_y = 0

    def follow(self, target):
        
        # Detect player room
        self.room_x = int(target.rect.centerx // self.width)
        self.room_y = int(target.rect.centery // self.height)
        
        # Limit the room
        max_room_x = max(0, (self.level_width - 1) // self.width)
        max_room_y = max(0, (self.level_height - 1) // self.height)
        
        self.room_x = max(0, min(self.room_x, max_room_x))
        self.room_y = max(0, min(self.room_y, max_room_y))
         # Move the camera by rooms
        self.offset.x = self.room_x * self.width
        self.offset.y = self.room_y * self.height
        
        # Limit the camera by room dimention
        self.offset.x = min(self.offset.x, max(0, self.level_width - self.width))
        self.offset.y = min(self.offset.y, max(0, self.level_height - self.height))
        # self.offset.x = target.rect.centerx - self.width / 2
        # self.offset.y = target.rect.centery - self.height / 2
        
        # limit the cam horizontal
        # self.offset.x = max(0, self.offset.x)
        # self.offset.x = min(self.offset.x, self.level_width - self.width)
        
        # limit the cam vertical
        # self.offset.y = max(0, self.offset.y)
        # self.offset.y = min(self.offset.y, self.level_height - self.height)

    def draw(self, group, surface):
        for sprite in group:
            screen_pos = sprite.rect.topleft - self.offset
            surface.blit(sprite.image, screen_pos)