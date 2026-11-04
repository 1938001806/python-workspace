import pygame
# import random

# class Alien:
#     def __init__(self,screen): #初始化
#         self.screen = screen
#         self.screen_rect = screen.get_rect()

#         self.image = pygame.Surface((40, 40)) #画出矩形
#         self.image.fill((255, 0, 0)) #上色

#         self.rect = self.image.get_rect() 

#         self.rect.x = random.randint(0, self.screen_rect.right - self.rect.width)
#         self.rect.y = random.randint(-100, -40)

#         self.speed = 1

#     def update(self):
#         self.rect.y += self.speed

#     def blitme(self):
#         self.screen.blit(self.image, self.rect)

#创建矩形框 将矩形框加载入窗口中 随机生成并从顶部向下移动 移动到底部或者接触飞船时判定游戏失败 接触到子弹判定为消失
class Alien:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 0, 0 ))
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.speed = 1

    def update(self, direction):
        self.rect.x += self.speed * direction

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def drop_down(self):
        self.rect.y += 20