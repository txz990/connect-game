import pygame
import sys
from game import Game
from settings import *

def main():
    """主函数"""
    # 初始化Pygame
    pygame.init()

    # 创建屏幕
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("连连看小游戏")

    # 创建时钟对象
    clock = pygame.time.Clock()

    # 创建游戏对象
    game = Game()

    # 游戏主循环
    running = True
    while running:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键点击
                    game.handle_click(event.pos)

            elif event.type == pygame.KEYDOWN:
                if not game.handle_key(event.key):
                    running = False

        # 更新游戏状态
        game.update()

        # 绘制游戏
        game.draw(screen)

        # 更新显示
        pygame.display.flip()

        # 控制帧率
        clock.tick(FPS)

    # 退出游戏
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()