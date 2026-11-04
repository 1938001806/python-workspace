import pygame
import sys
# import random
from ship import Ship
from bullet import Bullet
from alien import Alien

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("外星人入侵")

font = pygame.font.SysFont(None, 48)
score = 0
game_active = True

my_ship = Ship(screen)
bullets = []
aliens = []
fleet_direction = 1

def create_fleet(screen, aliens):
    alien_width = 40
    alien_height = 40
    available_space_x = screen.get_rect().width - 2 * alien_width
    number_aliens_x = available_space_x // (2 * alien_width)

    ship_height = my_ship.rect.height
    available_space_y = screen.get_rect().height - (3 * alien_height) - ship_height
    number_rows = available_space_y // (2 * alien_height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            alien_x = alien_width + 2 * alien_width * alien_number
            alien_y = alien_height + 2 * alien_height * row_number
            new_alien = Alien(screen, alien_x, alien_y)
            aliens.append(new_alien)

create_fleet(screen, aliens)
# for i in range(10):
#     new_alien = Alien(screen)
#     aliens.append(new_alien)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bullets.append(Bullet(screen, my_ship))
    if game_active:
        keys = pygame.key.get_pressed()
        my_ship.moving_right = keys[pygame.K_RIGHT]
        my_ship.moving_left = keys[pygame.K_LEFT]
        my_ship.moving_up = keys[pygame.K_UP]
        my_ship.moving_down = keys[pygame.K_DOWN]
        my_ship.update()


        for bullet in bullets[:]:
            bullet.update()
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)
                continue

            for alien in aliens[:]:
                if bullet.rect.colliderect(alien.rect):
                    bullets.remove(bullet)
                    aliens.remove(alien)
                    score += 10
                    break

        for alien in aliens:
            if alien.rect.right >= screen.get_rect().right:
                fleet_direction = -1
                for a in aliens:
                    a.drop_down()
                break
            elif alien.rect.left <= 0:
                fleet_direction = 1
                for a in aliens:
                    a.drop_down()
                break
        for alien in aliens[:]:
            alien.update(fleet_direction)

            if alien.rect.bottom >= screen.get_rect().bottom:
                game_active = False
                print("外星人入侵底部，游戏结束！")
                break
            if alien.rect.colliderect(my_ship.rect):
                game_active = False
                print("飞船被撞毁，游戏结束！")
                break
        # if alien.rect.bottom >= screen.get_rect().bottom:
        #     print("外星人入侵底部，游戏结束！")
        #     sys.exit()
        # if alien.rect.colliderect(my_ship.rect):
        #     print("飞船被撞毁，游戏结束！")
        #     sys.exit()

    screen.fill((0, 0, 50))
    my_ship.blitme()
    for bullet in bullets:bullet.blitme()
    for alien in aliens:alien.blitme()
    score_image = font.render(f"Score: {score}", True, (25, 255, 255))
    screen.blit(score_image, (10, 10))
    if not game_active:
        over_text = font.render("GAME OVER", True, (255, 0, 0))
        over_rect = over_text.get_rect(center=(400, 300))
        screen.blit(over_text, over_rect)

    pygame.time.Clock().tick(60)
    pygame.display.flip()