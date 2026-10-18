from setting import *

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites_groups):
        super().__init__(groups)
        self.walk_frames = [
            pygame.image.load(join("assets", "player", "walk", "0.png")).convert_alpha(),
            pygame.image.load(join("assets", "player", "walk", "1.png")).convert_alpha(),
            pygame.image.load(join("assets", "player", "walk", "2.png")).convert_alpha(),
        ]
        self.jump_frames = [
            pygame.image.load(join("assets", "player", "jump", "0.png")).convert_alpha(),
            pygame.image.load(join("assets", "player", "jump", "1.png")).convert_alpha()
        ]
        self.frame_index = 0
        self.image = self.walk_frames[self.frame_index]
        self.rect = self.image.get_frect(center = pos)
        self.animation_timer = 0

        # Mask
        self.mask = pygame.mask.from_surface(self.image)
        # Movement
        self.direction = pygame.Vector2()
        self.speed = 100
        self.moving = False
        self.fliping = False

        # Gravity and Jump
        self.gravity = 800
        self.velocity_y = 0
        self.jump_speed = 300
        self.on_ground = False

        # Coyote jump
        self.coyote_time = 0.2
        self.coyote_timer = 0

        # collision group
        self.collision_sprites_groups = collision_sprites_groups

    def input(self):
        keys = pygame.key.get_pressed()

        # Horizontal Movement
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        
        # Jump: went is on ground
        jump_input = pygame.key.get_just_pressed()
        if jump_input[pygame.K_SPACE] and self.coyote_timer > 0:
            self.velocity_y = -self.jump_speed
            self.on_ground = False
            self.coyote_timer = 0
            

    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.collison("horizontal")

        # Applay gravity
        self.velocity_y += self.gravity * dt

        # check
        self.on_ground = False

        # Vertical movement
        self.rect.y += self.velocity_y * dt
        self.collison("vertical")


    def collison(self, direction):
        for sprite in self.collision_sprites_groups:
            if sprite.rect.colliderect(self.rect):
                if direction == "horizontal":
                    if self.direction.x > 0: self.rect.right = sprite.rect.left
                    if self.direction.x < 0: self.rect.left = sprite.rect.right
                    
                if direction == "vertical":
                    # Falling to platform
                    if self.velocity_y > 0: 
                        self.rect.bottom = sprite.rect.top
                        self.velocity_y = 0
                        self.on_ground = True

                    # Hit the bottom of platform
                    elif self.velocity_y < 0:
                        self.rect.top = sprite.rect.bottom
                        self.velocity_y = 0
                        self.on_ground = False
                    
    def update(self, dt):
        self.input()

         # check direction
        if self.direction.x > 0:
            self.fliping = True
        elif self.direction.x < 0:
            self.fliping = False


        # check if moving
        self.moving = self.direction.x != 0

        # animate
        if self.moving:
            self.animation_timer += dt

            if self.animation_timer >= 0.12:
                self.frame_index += 1
                self.frame_index %= len(self.walk_frames)
                self.animation_timer = 0
        else:
            self.frame_index = 0

        # fliping sprites
        frame = self.walk_frames[self.frame_index]
        self.image = pygame.transform.flip(frame, self.fliping, False)

        # check vertical direction
        if self.velocity_y < 0:
            self.image = pygame.transform.flip(self.jump_frames[0],self.fliping, False)
        elif self.velocity_y > 0:
            self.image = pygame.transform.flip(self.jump_frames[1],self.fliping, False)

        # coyote timer
        if self.on_ground:
            self.coyote_timer = self.coyote_time
        else:
            self.coyote_timer = max(0, self.coyote_timer - dt)
        
        self.move(dt)