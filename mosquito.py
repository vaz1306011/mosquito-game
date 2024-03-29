import random
import sys
from typing import Tuple

import pygame
from pygame.locals import MOUSEBUTTONDOWN, QUIT, USEREVENT

pygame.init()

FPS = 60
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("蚊子大戰")

WHITE = pygame.Color("white")
BLACK = pygame.Color("black")

clock = pygame.time.Clock()
all_sprite = pygame.sprite.Group()


# 讀取貼圖
mosquito_sprite = pygame.image.load("./mosquito_sprite.png").convert_alpha()


class Mosquito(pygame.sprite.Sprite):
    SPRITE_WIDTH = 100
    SPRITE_HEIGHT = 100

    def __init__(self, x, y) -> None:
        # pygame物件繼承init
        super().__init__()

        # 蚊子圖片
        self.sprite = pygame.transform.scale(
            mosquito_sprite, (self.SPRITE_WIDTH, self.SPRITE_HEIGHT)
        )
        self.rect = self.sprite.get_rect()  # 蚊子位置
        self.rect.center = (x, y)

    def check_mouse(self, mouse_pos) -> bool:
        # 檢查是否滑鼠位置 x, y 在蚊子圖片上
        if self.rect.collidepoint(mouse_pos):
            return True
        return False


# 隨機產生位置
def get_random_position(widow_width, window_height) -> Tuple[float, float]:
    random_x = random.uniform(0, widow_width)
    random_y = random.uniform(0, window_height)

    return random_x, random_y


# 生成蚊子
def add_mosquito() -> Mosquito:
    random_x, random_y = get_random_position(WINDOW_WIDTH, WINDOW_HEIGHT)
    mosquito = Mosquito(random_x, random_y)
    all_sprite.add(mosquito)
    return mosquito


def main():
    mosquito = add_mosquito()

    reload_mosquito_event = USEREVENT + 1

    # 蚊子生成速度
    pygame.time.set_timer(reload_mosquito_event, 3000)
    points = 0

    my_font = pygame.font.SysFont(None, 30)
    my_hit_font = pygame.font.SysFont(None, 40)
    hit_text_surface = None

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == reload_mosquito_event:
                mosquito.kill()
                mosquito = add_mosquito()

            # 檢查是否滑鼠位置 x, y 在蚊子圖片上
            mouse_pos = pygame.mouse.get_pos()
            if (
                mosquito.rect.left <= mouse_pos[0] <= mosquito.rect.right
                and mosquito.rect.top <= mouse_pos[1] <= mosquito.rect.bottom
            ):
                mosquito.kill()
                mosquito = add_mosquito()
                # hit_text_surface = my_hit_font.render("Hit!!", True, BLACK)
                # 每次加五分
                points += 5

        # 背景顏色，清除畫面
        window_surface.fill(WHITE)

        # 遊戲分數儀表板
        text_surface = my_font.render("score: {}".format(points), True, BLACK)

        # 渲染物件
        window_surface.blit(mosquito.sprite, mosquito.rect)
        window_surface.blit(text_surface, (10, 0))

        # 顯示打中提示文字
        # if hit_text_surface:
        #     window_surface.blit(hit_text_surface, (10, 10))
        #     hit_text_surface = None

        pygame.display.update()


if __name__ == "__main__":
    main()
