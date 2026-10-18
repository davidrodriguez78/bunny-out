from setting import *
from sprites import *
from player import Player
from camera import Camera
# Game class
class Game:
    def __init__(self):
        pygame.init()
        self.screen_surface = pygame.display.set_mode((WINDOW_WIDHT, WINDOW_HEIGTH), pygame.SCALED)
        pygame.display.set_caption(GAME_NAME)
        self.clock = pygame.time.Clock()
        self.running = True

        # Groups
        self.all_sprites_groups = pygame.sprite.Group()
        self.collision_sprites_groups = pygame.sprite.Group()
        
        # test platform  
        self.test_level = load_pygame(join("data", "tmx", "test_map.tmx"))
        # Map draw
        for x, y, image in self.test_level.get_layer_by_name("ground").tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE),image, self.all_sprites_groups)
        # platform collision
        for obj in self.test_level.get_layer_by_name("collision"):
            CollisionSprites((obj.x, obj.y), pygame.Surface((obj.width, obj.height)),self.collision_sprites_groups)

        # Object
        self.player = Player((120,50), self.all_sprites_groups, self.collision_sprites_groups)
        self.camera = Camera(WINDOW_WIDHT, WINDOW_HEIGTH)

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Camera
            self.camera.follow(self.player)

            # BG color
            self.screen_surface.fill("black")


            # Update groups
            self.all_sprites_groups.update(dt)

            # Draw groups
            self.camera.draw(self.all_sprites_groups, self.screen_surface)
            
            # Display update
            pygame.display.update()
        pygame.quit()
        sys.exit()
if __name__ == "__main__":
    game = Game()
    game.run()