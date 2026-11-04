import pygame

class Bullet:
    def __init__(self,screen,ship):
        self.screen = screen
        self.image = pygame.Surface((5, 15))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        self.speed = 10

    def update(self):
        self.rect.y -= self.speed

    def blitme(self):
        self.screen.blit(self.image, self.rect)