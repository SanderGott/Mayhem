
from config import *
import pygame
import math
import time

class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/background.png")
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
    


class Rocket(pygame.sprite.Sprite):
    def __init__(self, pos, player, game):
        super().__init__()
        self.game = game
        self.player = player
        self.fuel = FUEL
        if player == 0:
            self.original_image = pygame.transform.scale(pygame.image.load("images/rocket2.png"), (28, 49))
            self.original_image_fire = pygame.transform.scale(pygame.image.load("images/rocket2_fire.png"), (28, 49))
            self.image = self.original_image
            self.controls = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_SPACE]
        else:
            self.original_image = pygame.transform.scale(pygame.image.load("images/rocket.png"), (28,49))
            self.original_image_fire = pygame.transform.scale(pygame.image.load("images/rocket_fire.png"), (28,49))
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
        if keys[self.controls[0]]:
            self.rotation += ROTATE_AMOUNT
        if keys[self.controls[1]]:
            self.rotation -= ROTATE_AMOUNT
        if keys[self.controls[2]]:
            if self.fuel > 0: # Only thrust if there is fuel left
                self.fuel -= 1
                self.speedx -= SPEED * math.sin(math.radians(self.rotation))
                self.speedy -= SPEED * math.cos(math.radians(self.rotation))
                self.image = self.original_image_fire # Copy of image if the rocket is firing
        
        if keys[self.controls[3]]:
            if time.time() - self.lastshot > 0.5: # Limits firing rate
                self.shoot()
                self.lastshot = time.time()
        if self.rotation > 360:
            self.rotation -= 360
        if self.rotation < 0:
            self.rotation += 360
        
        # Drawing
        self.image = pygame.transform.rotate(self.image, self.rotation) # Rotates the copy so that the original is not corrupted
        self.rect = self.image.get_rect(center=(self.x, self.y)) # Updates the rect to the new rotated image
        self.mask = pygame.mask.from_surface(self.image) # Updates the mask to the new rotated image
        
        
class Missile(pygame.sprite.Sprite):
    def __init__(self, pos, direction):
        super().__init__()
        self.image = pygame.transform.rotate(pygame.image.load("images/missile.png"), direction)
        self.x, self.y = pos
        self.speedx = BULLET_SPEED * math.sin(math.radians(direction))
        self.speedy = BULLET_SPEED * math.cos(math.radians(direction))
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self):
        self.x -= self.speedx
        self.y -= self.speedy
        self.rect.center = (self.x, self.y)



        


class Mayhem:
    def __init__(self):
        self.fps = FPS
        self.width = WIDTH
        self.height = HEIGHT
        self.WIN = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.sprite.GroupSingle(Background())
        self.stars = pygame.image.load("images/starbackground.jpg")
        self.stars = pygame.transform.scale(self.stars, (self.width, self.height))
        self.rocket = pygame.sprite.GroupSingle(Rocket((900, 70), 0, self))
        self.rocket2 = pygame.sprite.GroupSingle(Rocket((100, 70), 1, self))
        self.p0bullets = pygame.sprite.Group()
        self.p1bullets = pygame.sprite.Group()
        self.missile = pygame.image.load("images/missile.png")
        self.run()
    
    def check_collision(self, sprite1, sprite2):
        if pygame.sprite.spritecollide(sprite1.sprite, sprite2, False, pygame.sprite.collide_mask):
            #print("Collided")
            pass
    
    def check_bullet_collision(self, sprite1, sprite2):
        if pygame.sprite.spritecollide(sprite1.sprite, sprite2, False, pygame.sprite.collide_mask):
            print("Collided")
    

    
    def run(self):
        clock = pygame.time.Clock()

        lasttime = time.time()
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            self.WIN.blit(self.stars, (0, 0))
            self.background.draw(self.WIN)
            self.rocket.sprite.update()
            self.rocket2.sprite.update()
            self.check_collision(self.rocket, self.background)

            self.rocket.draw(self.WIN)
            self.rocket2.draw(self.WIN)

            self.p0bullets.update()
            self.p1bullets.update()
            self.check_bullet_collision(self.rocket, self.p1bullets)
            self.check_bullet_collision(self.rocket2, self.p0bullets)
            self.p0bullets.draw(self.WIN)
            self.p1bullets.draw(self.WIN)

            pygame.display.update()
            clock.tick(self.fps)
            #print(round(1/(time.time() - lasttime))) # print fps REMOVE AFTER
            lasttime = time.time()

            

        pygame.quit()
        