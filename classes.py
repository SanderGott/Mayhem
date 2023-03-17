
from config import *
import pygame
import math
import time

class Mayhem:
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
        self.missile = pygame.image.load("images/missile.png").convert_alpha()
        self.run()
    
    def check_collision(self, sprite1, sprite2):
        return pygame.sprite.spritecollide(sprite1.sprite, sprite2, False, pygame.sprite.collide_mask)
    
    def check_bullet_collision(self, sprite1, sprite2):
        if pygame.sprite.spritecollide(sprite1.sprite, sprite2, False, pygame.sprite.collide_mask):
            print("Collided")
    
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



    def run(self):
        clock = pygame.time.Clock()
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            self.WIN.blit(self.stars, (0, 0))
            self.background.draw(self.WIN)
            self.rocket.sprite.update()
            self.rocket2.sprite.update()
            self.p0bullets.update()
            self.p1bullets.update()
            
            rocket_collide = self.check_collision(self.rocket, self.background)
            rocket2_collide = self.check_collision(self.rocket2, self.background)
            if rocket_collide:
                self.rocket.sprite.health -= 1
                print("Rocket 1 health: ", self.rocket.sprite.health)
            if rocket2_collide:
                self.rocket2.sprite.health -= 1
            
            rocket_bullet_collide = pygame.sprite.groupcollide(self.rocket, self.p1bullets, False, True, pygame.sprite.collide_mask)
            rocket2_bullet_collide = pygame.sprite.groupcollide(self.rocket2, self.p0bullets, False, True, pygame.sprite.collide_mask)
            if rocket_bullet_collide:
                self.rocket.sprite.health -= MISSILE_DMG
                
            if rocket2_bullet_collide:
                self.rocket2.sprite.health -= MISSILE_DMG
            
            pygame.sprite.groupcollide(self.background, self.p0bullets, False, True, pygame.sprite.collide_mask)
            pygame.sprite.groupcollide(self.background, self.p1bullets, False, True, pygame.sprite.collide_mask)


            self.rocket.draw(self.WIN)
            self.rocket2.draw(self.WIN)

            
            self.check_bullet_collision(self.rocket, self.p1bullets)
            self.check_bullet_collision(self.rocket2, self.p0bullets)
            self.p0bullets.draw(self.WIN)
            self.p1bullets.draw(self.WIN)

            pygame.display.update()
            clock.tick(self.fps)  



            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]: # Temp reset button
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

