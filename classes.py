from config import *
import pygame
import math

class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/background.png")
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
    
    def draw(self, WIN):
        WIN.blit(self.image, (0, 0))


class Rocket(pygame.sprite.Sprite):
    def __init__(self, pos, player):
        super().__init__()
        if player == 0:
            self.image = pygame.image.load("images/rocket2.png")
            self.controls = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_SPACE]
        self.image = pygame.transform.scale(self.image, (40, 70), )
        self.rotation = 0
        self.speedx = 0
        self.speedy = 0
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.mask = pygame.mask.from_surface(self.image)
        


    def draw(self, WIN):

        image = self.image.copy() # Makes a copy of the image
        image = pygame.transform.rotate(image, self.rotation) # Rotates the copy so that the original is not corrupted
        self.rect = image.get_rect(center=self.rect.center) # Updates the rect to the new rotated image
        self.mask = pygame.mask.from_surface(image) # Updates the mask to the new rotated image
        
        pygame.draw.rect(WIN, (255, 0, 0), self.rect, 2) # Husk å fjern denne
        WIN.blit(image, self.rect)

        

    
    def move(self):
        keys = pygame.key.get_pressed()
        self.speedx *= FRICTION
        #self.speedy += GRAVITY

        self.rect.x += self.speedx
        self.rect.y += self.speedy


        if keys[self.controls[0]]:
            self.rotation += ROTATE_AMOUNT
        if keys[self.controls[1]]:
            self.rotation -= ROTATE_AMOUNT
        if keys[self.controls[2]]:
            self.speedx -= SPEED * math.sin(math.radians(self.rotation))
            self.speedy -= SPEED * math.cos(math.radians(self.rotation))
        
        

        

        
        
        
        

        if self.rotation > 360:
            self.rotation -= 360
        if self.rotation < 0:
            self.rotation += 360


    def update(self, WIN):
        self.move()
        self.draw(WIN)

        


class Mayhem:
    def __init__(self):
        self.fps = FPS
        self.width = WIDTH
        self.height = HEIGHT
        self.WIN = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.sprite.GroupSingle(Background())
        self.rocket = pygame.sprite.GroupSingle(Rocket((900, 70), 0))
    
    def check_collision(self, sprite1, sprite2):
        if pygame.sprite.spritecollide(sprite1.sprite, sprite2, False, pygame.sprite.collide_mask):
            print("Collided")

    
    def run(self):
        clock = pygame.time.Clock()


        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            self.WIN.fill(BLACK)
            self.background.draw(self.WIN)
            self.rocket.sprite.update(self.WIN)
            self.check_collision(self.rocket, self.background)

            # Display fps counter in top left
            
            print("FPS: ", clock.get_fps())

            pygame.display.update()
            clock.tick(self.fps)

            

        pygame.quit()
        