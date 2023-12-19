import pygame
import random
import time

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

circle_on_screen = False
enemy_on_screen = False

white = (255, 255, 255)
font = pygame.font.Font("freesansbold.ttf", 36)
score = 0
text = font.render('Score: ' + str(score), True, white)

textRect = text.get_rect()

textRect.topleft = (10, 10)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image2 = pygame.Surface((10, 10))
        self.image.fill("blue")
        self.image2.fill("white")
        self.rect = self.image.get_rect()
        self.rect.center = (screen.get_width() / 2, screen.get_height() / 2)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= 5.5
        if keys[pygame.K_d] and self.rect.right < screen.get_width():
            self.rect.x += 5
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= 6
        if keys[pygame.K_s] and self.rect.bottom < screen.get_height():
            self.rect.y += 5.5

class Trigger(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill("red")
        self.rect = self.image.get_rect()
        self.randomize_position()

    def randomize_position(self):
        self.rect.x = random.randint(0, screen.get_width() - self.rect.width)
        self.rect.y = random.randint(0, screen.get_height() - self.rect.height)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill("black")
        self.rect = self.image.get_rect()
        self.randomize_position()
        self.speed_x = random.choice([-3, 3])
        self.speed_y = random.choice([-3, 3])

    def randomize_position(self):
        self.rect.x = random.randint(0, screen.get_width() - self.rect.width)
        self.rect.y = random.randint(0, screen.get_height() - self.rect.height)

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.left < 0 or self.rect.right > screen.get_width():
            self.speed_x *= -1

        if self.rect.top < 0 or self.rect.bottom > screen.get_height():
            self.speed_y *= -1


class Player2(pygame.sprite.Sprite):
    def __init__(self, player_position):
        super().__init__()
        self.image = pygame.Surface((15, 15))
        self.image.fill("orange")
        self.rect = self.image.get_rect()
        self.rect.center = player_position

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            all_sprites.add(player2)
            self.rect.x -= 5 
        if keys[pygame.K_RIGHT]:
            all_sprites.add(player2)
            self.rect.x += 5
        if keys[pygame.K_UP]:
            all_sprites.add(player2)
            self.rect.y += 5 
        if keys[pygame.K_DOWN]:
            all_sprites.add(player2)
            self.rect.y -= 5 
            
def reset_game():
    global circle_on_screen, enemy_on_screen, game_over, score

    circle_on_screen = False
    enemy_on_screen = False
    game_over = False
    
    player.rect.center = (screen.get_width() / 2, screen.get_height() / 2)

    all_sprites.empty()
    all_sprites.add(player)

    enemy_group.empty()
    score -= 5
    
player = Player()
player2 = Player2(player.rect.center)
trigger = Trigger(30, 30)

all_sprites = pygame.sprite.Group()
all_sprites.add(player)

enemy_group = pygame.sprite.Group()

game_over = False

while running:
    screen.fill("green")
    text = font.render('Score: ' + str(score), True, white)
    screen.blit(text, textRect)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                reset_game()

    if circle_on_screen:
        if not all_sprites.has(trigger):
            trigger.randomize_position()
            all_sprites.add(trigger)
    else:
        all_sprites.remove(trigger)
        circle_on_screen = True

    if enemy_on_screen:
        if len(enemy_group) < 5:
            enemy = Enemy(50, 50)
            enemy_group.add(enemy)
            all_sprites.add(enemy)
    else:
        enemy_group.empty()
        enemy_on_screen = True
    
    player2.update()    
    all_sprites.update()
    enemy_group.update()

    if pygame.sprite.collide_rect(player, trigger):
        score += 1
        circle_on_screen = False
        
    if pygame.sprite.collide_rect(player2, trigger):
        score += 1
        circle_on_screen = False

    if pygame.sprite.spritecollide(player, enemy_group, False):
        player.kill()
        game_over = True

    all_sprites.draw(screen)
    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()
