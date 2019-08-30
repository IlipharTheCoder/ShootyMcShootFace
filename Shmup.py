# Pygame template
import pygame
import random
import os

WIDTH = 480
HIGHT = 600
fps = 60

# Colors
White = (255, 255, 255)
Block = (0, 0, 0)
Red = (255, 0, 0)
ShrekColor = (0, 255, 0)
Blue = (0, 0, 255)
Yellow = (255, 255, 0)
Orange = (255, 140, 0)

# set up assets (folders)
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

# Start pygame and make window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HIGHT))
pygame.display.set_caption("Shooty McShoot Face")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "PlayerShip.png")).convert()
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HIGHT - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -10
        if keystate[pygame.K_d]:
            self.speedx = 10
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,40))
        self.image.fill(Red)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(('10,20'))
        self.image.fill(Yellow)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill it if disaperated
        if self.rect.bottom < 0:
            self.kill()


all_sprites = pygame.sprite.Group()
player = Player()
bullets = pygame.sprite.Group()
mobs = pygame.sprite.Group()
all_sprites.add(player)
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

# Game loop
running = True
while running:
    #Keep clock running
    clock.tick(fps)
    # Prosses inputs and outputs (events)
    for event in pygame.event.get():
        #Check 4 close button
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    # Update
    all_sprites.update()
    #see if bullets hit mobs
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
    # check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits:
        running = False
    # Draw
    screen.fill(Block)
    all_sprites.draw(screen)
    # LAST!!!! |
    #          \/
    pygame.display.flip()

pygame.quit()
