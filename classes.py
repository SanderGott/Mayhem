
from config import *
import pygame
import math
import time
import random

class Mayhem:
    pygame.init()
    WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # Creates the window outside the init so that it can be accessed to convert images
    def __init__(self):
        self.fps = FPS
        self.width = WIDTH
        self.height = HEIGHT
        self.WIN = Mayhem.WIN
        self.background = pygame.sprite.GroupSingle(Background())
        self.stars = pygame.image.load("images/starbackground.png").convert_alpha()
        self.stars = pygame.transform.scale(self.stars, (self.width, self.height))
        self.rocket = pygame.sprite.GroupSingle(Rocket((900, 70), 0, self))
        self.rocket2 = pygame.sprite.GroupSingle(Rocket((100, 70), 1, self))
        self.p0bullets = pygame.sprite.Group()
        self.p1bullets = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.platforms.add(Platform((794, 885)))
        self.platforms.add(Platform((137, 885)))
        self.smokegroup = pygame.sprite.Group()
        self.score = [0, 0]
        self.run()
    def check_collision(self, sprite1, sprite2):
        return pygame.sprite.spritecollide(sprite1.sprite, sprite2, False, pygame.sprite.collide_mask)
    
    def reset(self):
        self.rocket.sprite.x, self.rocket.sprite.y = R0_START_POS
        self.rocket.sprite.rotation = 0
        self.rocket.sprite.fuel = FUEL
        self.rocket.sprite.health = HEALTH
        self.rocket.sprite.speedx = 0
        self.rocket.sprite.speedy = 0
        self.rocket2.sprite.x, self.rocket2.sprite.y = R1_START_POS
        self.rocket2.sprite.rotation = 0
        self.rocket2.sprite.fuel = FUEL
        self.rocket2.sprite.health = HEALTH
        self.rocket2.sprite.speedx = 0
        self.rocket2.sprite.speedy = 0

    def draw_stats(self):
        # Draw score
        font = pygame.font.Font("fonts/ARCADECLASSIC.TTF", 30)
        text = font.render(("Player 1       Player 2"), 1, (255, 255, 255))
        text2 = font.render(("Score " + str(self.score[0]) + "       Score " + str(self.score[1])), 1, (255, 255, 255))
        self.WIN.blit(text, (WIDTH - text.get_width() - 5, 120))
        self.WIN.blit(text2, (WIDTH - text2.get_width() - 5, 150))

        # Draw health
        rect1 = pygame.rect.Rect(780, 300 - self.rocket.sprite.health / HEALTH * 100, 30, self.rocket.sprite.health / HEALTH * 100)
        rect2 = pygame.rect.Rect(900, 300 - self.rocket2.sprite.health / HEALTH * 100, 30, self.rocket2.sprite.health / HEALTH* 100)
        pygame.draw.rect(self.WIN, (255, 0, 0), rect1)
        pygame.draw.rect(self.WIN, (255, 0, 0), rect2)

        # Draw fuel
        rect1 = pygame.rect.Rect(820, 300 - self.rocket.sprite.fuel / FUEL * 100, 30, self.rocket.sprite.fuel / FUEL * 100)
        rect2 = pygame.rect.Rect(940, 300 - self.rocket2.sprite.fuel / FUEL * 100, 30, self.rocket2.sprite.fuel / FUEL * 100)
        pygame.draw.rect(self.WIN, (0, 0, 255), rect1)
        pygame.draw.rect(self.WIN, (0, 0, 255), rect2)
    def draw_winner(self, winner):
        font = pygame.font.Font("fonts/ARCADECLASSIC.TTF", 100)
        text = font.render(("Player " + str(winner) + " wins!"), 1, (255, 255, 255))
        self.WIN.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
        pygame.display.update()
        time.sleep(3)
        self.reset()
    
    def check_collisions(self):
        # Rocket collision with background
        rocket_collide = self.check_collision(self.rocket, self.background)
        rocket2_collide = self.check_collision(self.rocket2, self.background) 
        if rocket_collide:
            self.rocket.sprite.health -= 1
        if rocket2_collide:
            self.rocket2.sprite.health -= 1
        
        # Rocket collision with bullets - bullets are deleted
        rocket_bullet_collide = pygame.sprite.groupcollide(self.rocket, self.p1bullets, False, True, pygame.sprite.collide_mask)
        rocket2_bullet_collide = pygame.sprite.groupcollide(self.rocket2, self.p0bullets, False, True, pygame.sprite.collide_mask)
        if rocket_bullet_collide:
            self.rocket.sprite.health -= MISSILE_DMG 
        if rocket2_bullet_collide:
            self.rocket2.sprite.health -= MISSILE_DMG
        
        # Bullet collision with background - bullets are deleted
        pygame.sprite.groupcollide(self.background, self.p0bullets, False, True, pygame.sprite.collide_mask) 
        pygame.sprite.groupcollide(self.background, self.p1bullets, False, True, pygame.sprite.collide_mask)
        

        # Rocket collision with each other
        rockets_collide = self.check_collision(self.rocket, self.rocket2)
        if rockets_collide:
            self.rocket.sprite.health -= 1
            self.rocket2.sprite.health -= 1 # Loses health when colliding with each other
    
        # If rocket is outside screen
        if self.rocket.sprite.x > WIDTH or self.rocket.sprite.x < 0 or self.rocket.sprite.y > HEIGHT or self.rocket.sprite.y < 0:
            self.rocket.sprite.health = -1
        if self.rocket2.sprite.x > WIDTH or self.rocket2.sprite.x < 0 or self.rocket2.sprite.y > HEIGHT or self.rocket2.sprite.y < 0:
            self.rocket2.sprite.health = -1

    def run(self):
        self.reset()
        clock = pygame.time.Clock()
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False 

            # Rocket collision with platforms
            platform_collide = self.check_collision(self.rocket, self.platforms) 
            platform2_collide = self.check_collision(self.rocket2, self.platforms)
            if platform_collide:
                self.rocket.sprite.speedy = 0
                self.rocket.sprite.y = 885 - 43
                if self.rocket.sprite.fuel < FUEL:
                    self.rocket.sprite.fuel += 5
            if platform2_collide:
                self.rocket2.sprite.speedy = 0
                self.rocket2.sprite.y = 885 - 43 # Stops the rocket from falling through the platform
                if self.rocket2.sprite.fuel < FUEL:
                    self.rocket2.sprite.fuel += 5

            self.WIN.blit(self.stars, (0, 0))
            self.background.draw(self.WIN)
            self.rocket.update()
            self.rocket2.update()
            self.p0bullets.update()
            self.p1bullets.update()
            self.smokegroup.update()
            
            self.check_collisions()

            # Resets when a rocket dies
            if self.rocket.sprite.health <= 0:
                self.score[1] += 1
                self.draw_winner(2)
            if self.rocket2.sprite.health <= 0:
                self.score[0] += 1
                self.draw_winner(1)
            
            
            self.smokegroup.draw(self.WIN)
            self.rocket.draw(self.WIN)
            self.rocket2.draw(self.WIN)
            self.p0bullets.draw(self.WIN)
            self.p1bullets.draw(self.WIN)
            self.platforms.draw(self.WIN)
            self.draw_stats()
            pygame.display.update()
            clock.tick(self.fps)  
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]: # Reset button
                self.reset()
        pygame.quit()


class Background(pygame.sprite.Sprite):
    image = pygame.image.load("images/background.png").convert_alpha()
    def __init__(self):
        super().__init__()
        self.image = Background.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)


class Rocket(pygame.sprite.Sprite):
    rocket_img = {
        0: {
            "original": pygame.transform.scale(pygame.image.load("images/rocket2.png"), (28, 49)).convert_alpha(),
            "fire": pygame.transform.scale(pygame.image.load("images/rocket2_fire.png"), (28, 49)).convert_alpha()
        },
        1: {
            "original": pygame.transform.scale(pygame.image.load("images/rocket.png"), (28,49)).convert_alpha(),
            "fire": pygame.transform.scale(pygame.image.load("images/rocket_fire.png"), (28,49)).convert_alpha()
        }
    }
    def __init__(self, pos, player, game):
        super().__init__()
        self.game = game
        self.player = player
        self.fuel = FUEL
        self.health = HEALTH
        if player == 0:
            self.original_image = Rocket.rocket_img[0]["original"]
            self.original_image_fire = Rocket.rocket_img[0]["fire"]
            self.image = self.original_image
            self.controls = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_SPACE]
        else:
            self.original_image = Rocket.rocket_img[1]["original"]
            self.original_image_fire = Rocket.rocket_img[1]["fire"]
            self.image = self.original_image
            self.controls = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_RCTRL]
        self.rotation = 0
        self.speedx = 0
        self.speedy = 0
        self.x = pos[0]
        self.y = pos[1]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.mask = pygame.mask.from_surface(self.image)
        self.lastshot = time.time()

    def shoot(self):    
        missile = Missile((self.x, self.y), self.rotation)
        if self.player == 0:
            self.game.p0bullets.add(missile)
        else:
            self.game.p1bullets.add(missile)

    def update(self):
        # Moving
        keys = pygame.key.get_pressed()
        self.speedy += GRAVITY
        self.x += self.speedx # Using own x and y since rect x and y can only be integers
        self.y += self.speedy # Gets smoother movement this way
        self.rect.x = self.x # Converts the float back to int
        self.rect.y = self.y
        self.image = self.original_image
        if keys[self.controls[0]]: # Rotate left
            self.rotation += ROTATE_AMOUNT
        if keys[self.controls[1]]: # Rotate right
            self.rotation -= ROTATE_AMOUNT
        if keys[self.controls[2]]: ## Thrust key
            if self.fuel > 0: # Only thrust if there is fuel left
                self.fuel -= 1
                self.speedx -= SPEED * math.sin(math.radians(self.rotation))
                self.speedy -= SPEED * math.cos(math.radians(self.rotation))
                self.image = self.original_image_fire # Copy of image if the rocket is firing 
                smoke_pos = (self.x + 14 * math.sin(math.radians(self.rotation)), self.y + 14 * math.cos(math.radians(self.rotation))) 
                self.game.smokegroup.add(Smoke(smoke_pos))
      
        if keys[self.controls[3]]: # Shoot key
            if time.time() - self.lastshot > FIRERATE: # Limits firing rate
                self.shoot()
                self.lastshot = time.time()
        if self.rotation > 360:
            self.rotation -= 360
        if self.rotation < 0:
            self.rotation += 360   

        # Update image, rect and mask
        self.image = pygame.transform.rotate(self.image, self.rotation) # Rotates the copy so that the original is not corrupted
        self.rect = self.image.get_rect(center=(self.x, self.y)) # Updates the rect to the new rotated image
        self.mask = pygame.mask.from_surface(self.image) # Updates the mask to the new rotated image 


class Missile(pygame.sprite.Sprite):
    original_image = pygame.image.load("images/missile.png").convert_alpha()
    def __init__(self, pos, direction):
        super().__init__()
        self.image = pygame.transform.rotate(Missile.original_image, direction)
        self.x, self.y = pos
        self.speedx = BULLET_SPEED * math.sin(math.radians(direction))
        self.speedy = BULLET_SPEED * math.cos(math.radians(direction))
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)  

    def update(self):
        self.x -= self.speedx
        self.y -= self.speedy
        self.rect.center = (self.x, self.y)


class Platform(pygame.sprite.Sprite):
    original_image = pygame.image.load("images/platform.png").convert_alpha()
    def __init__(self, pos):
        super().__init__()
        self.x, self.y = pos
        self.image = pygame.transform.scale(Platform.original_image, (80, 41))
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)


class Smoke(pygame.sprite.Sprite):
    image = pygame.image.load("images/smoke.png").convert_alpha()
    def __init__(self, pos):
        super().__init__()
        self.image = Smoke.image
        self.x, self.y = pos
        self.time = time.time() # Time the smoke was created
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        if time.time() - self.time > SMOKE_DURATION: # Removes smoke after time
            self.kill()   
        else:
            self.x += random.randint(-2, 2) # Makes the smoke look more realistic
            self.y -= random.randint(0, 2) # Moves the smoke upwards
            self.rect.center = (self.x, self.y) # Updates the rect to the new position
            