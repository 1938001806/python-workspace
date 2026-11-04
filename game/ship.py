import pygame

class Ship:
    def __init__(self,screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.image = pygame.Surface((60, 80))
        self.image.fill((0, 255, 0))

        self.rect = self.image.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.x += 1
        if self.moving_left and self.rect.left > 0:
            self.rect.x -= 1
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.rect.y += 1
        if self.moving_up and self.rect.top > 0:
            self.rect.y -= 1

