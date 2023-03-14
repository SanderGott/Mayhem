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
    
    def draw(self, WIN):
        WIN.blit(self.image, (0, 0))


class Rocket(pygame.sprite.Sprite):
    def __init__(self, pos, player, game):
        super().__init__()
        self.game = game
        self.player = player
        if player == 0:
            self.image = pygame.image.load("images/rocket2.png")
            self.fire_image = pygame.image.load("images/rocket2_fire.png")
            self.controls = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_SPACE]
        else:
            self.image = pygame.image.load("images/rocket.png")
            self.fire_image = pygame.image.load("images/rocket_fire.png")
            self.controls = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_RCTRL]
        self.image = pygame.transform.scale(self.image, (28, 49), )
        self.fire_image = pygame.transform.scale(self.fire_image, (28, 49), )
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
        #bullet = (x, y, speedx, speedy, rotation)
        bullet = [self.x, self.y, BULLET_SPEED * math.sin(math.radians(self.rotation)), BULLET_SPEED * math.cos(math.radians(self.rotation)), self.rotation]
        if self.player == 0:
            self.game.p0bullets.append(bullet)
        else:
            self.game.p1bullets.append(bullet)

    def update(self, WIN):
        # Moving
        keys = pygame.key.get_pressed()
        #self.speedx *= FRICTION
        self.speedy += GRAVITY

        self.x += self.speedx # Using own x and y since rect x and y can only be integers
        self.y += self.speedy # Gets smoother movement this way
        self.rect.x = self.x # Converts the float back to int
        self.rect.y = self.y


        if keys[self.controls[0]]:
            self.rotation += ROTATE_AMOUNT
        if keys[self.controls[1]]:
            self.rotation -= ROTATE_AMOUNT
        if keys[self.controls[2]]:
            self.speedx -= SPEED * math.sin(math.radians(self.rotation))
            self.speedy -= SPEED * math.cos(math.radians(self.rotation))
            image = self.fire_image.copy() # Copy of image if the rocket is firing
        else:
            image = self.image.copy() # Copy of image if the rocket is not firing
        if keys[self.controls[3]]:
            if time.time() - self.lastshot > 0.5:
                self.shoot()
                self.lastshot = time.time()
        if self.rotation > 360:
            self.rotation -= 360
        if self.rotation < 0:
            self.rotation += 360
        
        # Drawing
        
        image = pygame.transform.rotate(image, self.rotation) # Rotates the copy so that the original is not corrupted
        self.rect = image.get_rect(center=(self.x, self.y)) # Updates the rect to the new rotated image
        self.mask = pygame.mask.from_surface(image) # Updates the mask to the new rotated image
        
        pygame.draw.rect(WIN, (255, 0, 0), self.rect, 2) # Husk å fjern denne
        WIN.blit(image, self.rect)
        

        


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
        self.rokcet2 = pygame.sprite.GroupSingle(Rocket((100, 70), 1, self))
        self.p0bullets = []
        self.p1bullets = []
        self.missile = pygame.image.load("images/missile.png")
        self.run()
    
    def check_collision(self, sprite1, sprite2):
        if pygame.sprite.spritecollide(sprite1.sprite, sprite2, False, pygame.sprite.collide_mask):
            print("Collided")
    
    def move_bullets(self):
        #bullet = (x, y, speedx, speedy, rotation)
        for bullet in self.p1bullets:
            bullet[0] -= bullet[2]
            bullet[1] -= bullet[3]
            if self.background.sprite.mask.get_at((bullet[0], bullet[1])):
                self.p1bullets.remove(bullet)
            try: # Error message if bullet is outside mask
                if self.rocket.sprite.mask.get_at((bullet[0], bullet[1])):
                    self.p1bullets.remove(bullet)
                    print("Hit")
            except:
                pass
            
            # Draw bullet
            image = self.missile.copy()
            image = pygame.transform.rotate(image, bullet[4])
            self.WIN.blit(image, (bullet[0], bullet[1]))

        for bullet in self.p0bullets:
            bullet[0] -= bullet[2]
            bullet[1] -= bullet[3]
            if self.background.sprite.mask.get_at((bullet[0], bullet[1])):
                self.p0bullets.remove(bullet)
            try:
                if self.rokcet2.sprite.mask.get_at((bullet[0], bullet[1])):
                    self.p0bullets.remove(bullet)
                    print("Hit")
            except:
                pass
            
            # Draw bullet
            image = self.missile.copy()
            image = pygame.transform.rotate(image, bullet[4])
            self.WIN.blit(image, (bullet[0], bullet[1]))


    
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
            self.rocket.sprite.update(self.WIN)
            self.rokcet2.sprite.update(self.WIN)
            self.check_collision(self.rocket, self.background)

            self.move_bullets()
            pygame.display.update()
            clock.tick(self.fps)

            

        pygame.quit()
        