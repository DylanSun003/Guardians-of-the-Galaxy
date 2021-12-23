import os
import pygame
import random

FPS = 60
WIDTH = 700  # Port width 
HEIGHT = 900 # Port height
SPACESHIP_SPEED = 8
CHANCE_REMAIN = 3
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TREASURE_DROP_RATE = 0.90
STONE_NUMBER = 10

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Guardians of the Galaxy")

###########################################################################################
# Adding image 
BACKGROUND = pygame.image.load(os.path.join("image","space_background.jpeg")).convert()
MISSILE_IMAGE = pygame.image.load(os.path.join("image","missile.png")).convert()
SPACESHIP_MINI_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("image","spaceship.png")), (35,45))
SPACESHIP_MINI_IMAGE.set_colorkey(BLACK)
pygame.display.set_icon(SPACESHIP_MINI_IMAGE)


explode_Image_List = []
for i in range(11):
    EXPLODE_IMAGE = pygame.image.load(os.path.join("image/explode", f"explode{i}.png")).convert()
    EXPLODE_IMAGE.set_colorkey(BLACK)
    explode_Image_List.append(EXPLODE_IMAGE)

spaceship_Image_List = [] 
for i in range(2):
    SPACESHIP_IMAGE = pygame.image.load(os.path.join("image", f"spaceship{i}.png")).convert()
    spaceship_Image_List.append(SPACESHIP_IMAGE)

spaceship_With_Shield_Image_List = [] 
for i in range(2):
    SPACESHIP_With_Shield_IMAGE = pygame.image.load(os.path.join("image", f"spaceshipwithShield{i}.png")).convert()
    spaceship_With_Shield_Image_List.append(SPACESHIP_With_Shield_IMAGE)

rock_Image_List = []
for i in range(3):
    STONE_IMAGE = pygame.image.load(os.path.join("image", f"rock{i}.png")).convert()
    rock_Image_List.append(STONE_IMAGE)

treasure_List = {}
treasure_List["missile"] = pygame.image.load(os.path.join("image", "missile2.png")).convert()
treasure_List["shield"] = pygame.image.load(os.path.join("image", "shield.png")).convert()


font_name = pygame.font.match_font('arial')


###########################################################################################
# Adding sound track 
BACKGROUND_TRACK = pygame.mixer.music.load(os.path.join("sound","background.ogg"))
pygame.mixer.music.set_volume(0.1)

SHOOTING_SOUND = pygame.mixer.Sound(os.path.join("sound","shoot.wav"))
pygame.mixer.Sound.set_volume(SHOOTING_SOUND,0.1)

SPACESHIP_EXPLODE = pygame.mixer.Sound(os.path.join("sound", "rumble.ogg"))
pygame.mixer.Sound.set_volume(SPACESHIP_EXPLODE,0.2)

stone_explode_sound_list = []
for i in range(1):
    STONE_EXPLODE_SOUND = pygame.mixer.Sound(os.path.join("sound",f"expl{i}.wav"))
    pygame.mixer.Sound.set_volume(STONE_EXPLODE_SOUND,0.1)
    stone_explode_sound_list.append(STONE_EXPLODE_SOUND)

MISSILE_LEVEL_UP = pygame.mixer.Sound(os.path.join("sound","pow0.wav"))
SHIELD_UP = pygame.mixer.Sound(os.path.join("sound","pow1.wav"))

###########################################################################################
# Helping function: 
# Adding deleted stone
def add_stone():
    fallingStone = FallingStone()
    all_sprites.add(fallingStone)
    stone_sprites.add(fallingStone)

def add_treasure(hit):
    if random.random() > TREASURE_DROP_RATE:
        if random.randrange(0, 2):
            treasure = Missile_Treasure(hit.rect.center)
        else:
            treasure = Shield_Treasure(hit.rect.center)

        all_sprites.add(treasure)
        treasure_sprites.add(treasure)

# Adding health bar
def draw_Health_Bar(surf, hp, x, y):
    BAR_WIDTH = 100
    BAR_HEIGHT = 10
    fill = (hp/100)*BAR_WIDTH
    outline_rect = pygame.Rect(x, y, BAR_WIDTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, (0,255,0), fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

# Adding life remain
def draw_life_remain(surf, life_remain, x, y):
    for i in range(life_remain):
        img_rect = SPACESHIP_MINI_IMAGE.get_rect()
        img_rect.x = x + 40*i
        img_rect.y = y
        surf.blit(SPACESHIP_MINI_IMAGE, img_rect)


# Adding text to the screen
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)


# Adding initial screen
def draw_init_screen():
    screen.blit(pygame.transform.rotate(BACKGROUND, 90), (0,0))
    draw_text(screen, "Guardians of the Galaxy", 50, WIDTH/2, HEIGHT/2-200)
    draw_text(screen, "\"\u2190 \u2192\" to move to left and right", 30, WIDTH/2, HEIGHT/2-40)
    draw_text(screen, "\"\u2191 \u2193\" to move to up and down", 30, WIDTH/2, HEIGHT/2)
    draw_text(screen, "Space to shoot", 30, WIDTH/2, HEIGHT/2+40)
    draw_text(screen, "Push any key to start", 20, WIDTH/2, HEIGHT/2+200)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYUP:
                waiting = False
                return True

# Adding Gameover screen
def draw_Gameover_screen():
    screen.blit(pygame.transform.rotate(BACKGROUND, 90), (0,0))
    draw_text(screen, "Game Over!", 50, WIDTH/2, HEIGHT/2-100)
    draw_text(screen, "Push Space to continue", 20, WIDTH/2, HEIGHT/2+200)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    waiting = False
                    return True
                

# Adding explosion anim
def add_explosion(hit):
    explosion = ExplodeAnimation(hit.rect.center, hit.radius)
    all_sprites.add(explosion)
    return explosion

###########################################################################################
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(random.choice(spaceship_Image_List), (90,160))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 25
        # pygame.draw.circle(self.image, (0,255,0), [self.rect.centerx,self.rect.centery], self.radius)
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 20
        self.lifeRemain = CHANCE_REMAIN
        self.health = 100
        self.hidden = False
        self.hidden_time = 0

        self.missileUp = False
        self.missileUpRemain = 0
        self.missileUpAlrUpTime = 0
        
        self.shieldUp = False
        self.shieldUpRemain = 0
        self.shieldUpAlrUpTime = 0

        self.damage = 20

    def update(self):
        current = pygame.time.get_ticks()
        if self.missileUpRemain <= current - self.missileUpAlrUpTime:
            self.missileUp = False
            self.damage = 20

        if self.shieldUpRemain <= current - self.shieldUpAlrUpTime:
            self.image = pygame.transform.scale(random.choice(spaceship_Image_List), (90,160))
            self.image.set_colorkey(BLACK)
            self.shieldUp = False
        else:
            self.image = pygame.transform.scale(random.choice(spaceship_With_Shield_Image_List), (120,165))
            self.image.set_colorkey(BLACK)

        if self.hidden: 
            self.rect.centery -= 6
            if self.rect.centery < HEIGHT - 200 :
                self.hidden = False
            
        key_input = pygame.key.get_pressed()
        if key_input[pygame.K_RIGHT]:
            if self.rect.right >= WIDTH:
                return
            self.rect.x += SPACESHIP_SPEED
        if key_input[pygame.K_LEFT]:
            if self.rect.left <= 0:
                return
            self.rect.x -= SPACESHIP_SPEED
        if key_input[pygame.K_UP]:
            if self.rect.top <= 0:
                return
            self.rect.y -= SPACESHIP_SPEED
        if key_input[pygame.K_DOWN]:
            if self.rect.bottom >= HEIGHT + 20:
                return
            self.rect.y += SPACESHIP_SPEED
        
    def shoot(self):
        if not self.hidden:
            if self.missileUp:
                missileOne = Missile(self.rect.centerx-20, self.rect.top)
                missileTwo = Missile(self.rect.centerx+20, self.rect.top)
                all_sprites.add(missileOne)
                missile_sprites.add(missileOne)
                all_sprites.add(missileTwo)
                missile_sprites.add(missileTwo)
            else:

                missile = Missile(self.rect.centerx, self.rect.top)
                all_sprites.add(missile)
                missile_sprites.add(missile)

            SHOOTING_SOUND.play()
    
    def hidePlane(self):
        self.hidden = True
        self.hidden_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT + 400) 
        self.addShieldTime(3000)

    def addShieldTime(self, timeRemain):
        self.shieldUpRemain = timeRemain
        self.shieldUpAlrUpTime = pygame.time.get_ticks()
        self.shieldUp = True
    
    def addMissileTime(self, timeRemain):
        MISSILE_LEVEL_UP.play()
        self.damage = 40
        self.missileUpRemain = timeRemain
        self.missileUpAlrUpTime = pygame.time.get_ticks()
        self.missileUp = True


###########################################################################################
class FallingStone(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = pygame.transform.scale(random.choice(rock_Image_List), (random.randrange(20, 200), random.randrange(20,200)))
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width/2.7)
        # pygame.draw.circle(self.image_ori, (0,255,0), [self.rect.centerx,self.rect.centery], self.radius)
        self.rect.centerx = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-200, -120)
        self.speedy = random.randrange(2, 12)
        self.speedx = random.randrange(-5, 5)
        self.total_rotate_degree = 0
        self.rotate_degree = random.randrange(-5, 5)
        self.health = self.radius

    def rotate(self):
        self.total_rotate_degree += self.rotate_degree
        self.total_rotate_degree %= 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_rotate_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.rect.centerx = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 10)
            self.speedx = random.randrange(-3, 3)
    
   
###########################################################################################    
class Missile(pygame.sprite.Sprite):
    def __init__(self, spaceShipX, spaceShipY):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(MISSILE_IMAGE, (20, 70))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = spaceShipX
        self.rect.bottom = spaceShipY
        self.speedy = -8

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0: 
            self.kill()

###########################################################################################    
class Treasure(pygame.sprite.Sprite):
    def __init__(self, center, treasure_Type, treasure_Type_Size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(treasure_Type, treasure_Type_Size)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = random.randrange(2, 12)
        self.speedx = random.randrange(-5, 5)

    def update(self):
        self.rect.centerx += self.speedx
        self.rect.centery += self.speedy
        if self.rect.top > HEIGHT: 
            self.kill()

class Missile_Treasure(Treasure):
    def __init__(self, center):
        super().__init__(center, treasure_List["missile"], (15, 55))
        self.time_Remain = 4;

class Shield_Treasure(Treasure):
    def __init__(self, center):
        super().__init__(center, treasure_List["shield"], (30, 40))
        self.time_Remain = 6;


###########################################################################################    
class ExplodeAnimation(pygame.sprite.Sprite):
    def __init__(self, center, explode_Size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(explode_Image_List[0], (explode_Size*10, explode_Size*10))
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.radius = explode_Size*10
        self.frame = 0
        self.last_Update = pygame.time.get_ticks()
        self.frame_Rate = 40

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_Update > self.frame_Rate:
            self.last_Update = now
            self.frame += 1
            if self.frame == len(explode_Image_List):
                self.kill()
            else:    
                self.image = pygame.transform.scale(explode_Image_List[self.frame], (self.radius, self.radius))
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center



###########################################################################################
all_sprites = pygame.sprite.Group()
stone_sprites = pygame.sprite.Group()
missile_sprites = pygame.sprite.Group()
treasure_sprites = pygame.sprite.Group()

player = Player()
all_sprites.add(player)
score = 0 

# Generating stone
for i in range(STONE_NUMBER): 
    fallingStone = FallingStone()
    all_sprites.add(fallingStone)
    stone_sprites.add(fallingStone)


###########################################################################################
# Main game loop

running = True
show_init_screen = True

# background music
pygame.mixer.music.play(-1) 

while running:
    if show_init_screen:
        if not draw_init_screen():
            break

        all_sprites = pygame.sprite.Group()
        stone_sprites = pygame.sprite.Group()
        missile_sprites = pygame.sprite.Group()
        treasure_sprites = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        score = 0 
        # Generating stone
        for i in range(STONE_NUMBER): 
            fallingStone = FallingStone()
            all_sprites.add(fallingStone)
            stone_sprites.add(fallingStone)

        show_init_screen = False

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    all_sprites.update()
    hitsStones = pygame.sprite.groupcollide(stone_sprites, missile_sprites, False, True)
    for hit in hitsStones:
        hit.health -= player.damage
        hit.speedy -= player.damage / 35
        if hit.health <= 0:
            hit.kill()
            add_stone()
            add_explosion(hit)
            add_treasure(hit)
            score += hit.radius
            random.choice(stone_explode_sound_list).play()
    
    hitTreasure = pygame.sprite.spritecollide(player, treasure_sprites, True, pygame.sprite.collide_circle)
    for hit in hitTreasure:
        timeRemainForTreasure= getattr(hit, "time_Remain")*1000
        if type(hit) == Missile_Treasure:
            player.addMissileTime(timeRemainForTreasure)

        
        if type(hit) == Shield_Treasure:
            SHIELD_UP.play()
            player.addShieldTime(timeRemainForTreasure)
            

    hitSpaceShips = pygame.sprite.spritecollide(player,stone_sprites, True, pygame.sprite.collide_circle)
    for hit in hitSpaceShips:
        SPACESHIP_EXPLODE.play()
        add_stone()
        add_explosion(hit)
        if not player.shieldUp:
            player.health -= int(hit.radius)
            if player.health <= 0:
                player.hidePlane()
                player.health = 100
                if player.lifeRemain > 1:
                    player.lifeRemain -= 1
                else:
                    if not draw_Gameover_screen():
                        pygame.quit()

                    show_init_screen = True


    screen.blit(pygame.transform.rotate(BACKGROUND, 90), (0,0))
    all_sprites.draw(screen)
    draw_text(screen, str(score), 20, WIDTH/2, 10)
    # draw_text(screen, "Remain: "+str(player.lifeRemain), 20, 55, 10)
    draw_life_remain(screen, player.lifeRemain, 20, 10)
    draw_text(screen, "Health: "+str(player.health), 20, WIDTH - 55, 35)
    draw_Health_Bar(screen, player.health, WIDTH - 105, 15)
    
    pygame.display.update()

pygame.quit()
