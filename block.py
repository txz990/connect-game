import pygame
from settings import *
from cartoon_graphics import get_cartoon_surface

class Block:
    """游戏方块类"""

    def __init__(self, x, y, block_type=0):
        self.x = x  # 网格坐标
        self.y = y
        self.block_type = block_type  # 0表示空块，1-8表示不同类型的方块
        self.selected = False

    def is_empty(self):
        """检查是否为空块"""
        return self.block_type == 0

    def is_same_type(self, other_block):
        """检查是否与另一个方块类型相同"""
        return (not self.is_empty() and
                not other_block.is_empty() and
                self.block_type == other_block.block_type)

    def get_screen_pos(self):
        """获取屏幕坐标"""
        screen_x = BOARD_X + self.x * BLOCK_SIZE
        screen_y = BOARD_Y + self.y * BLOCK_SIZE
        return screen_x, screen_y

    def get_rect(self):
        """获取方块的矩形区域"""
        screen_x, screen_y = self.get_screen_pos()
        return pygame.Rect(screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE)

    def draw(self, screen):
        """绘制方块"""
        if self.is_empty():
            return

        screen_x, screen_y = self.get_screen_pos()
        rect = pygame.Rect(screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE)

        # 绘制方块背景（圆角矩形效果）
        background_color = LIGHT_GRAY if not self.selected else YELLOW
        pygame.draw.rect(screen, background_color, rect, border_radius=8)

        # 绘制阴影效果
        shadow_rect = pygame.Rect(screen_x + 2, screen_y + 2, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen, DARK_GRAY, shadow_rect, border_radius=8)
        pygame.draw.rect(screen, background_color, rect, border_radius=8)

        # 绘制卡通图案
        cartoon_surface = get_cartoon_surface(self.block_type)
        if cartoon_surface:
            # 居中绘制卡通图案
            cartoon_rect = cartoon_surface.get_rect()
            cartoon_rect.center = rect.center
            screen.blit(cartoon_surface, cartoon_rect)

        # 绘制选中边框
        if self.selected:
            pygame.draw.rect(screen, ORANGE, rect, 3, border_radius=8)
        else:
            pygame.draw.rect(screen, WHITE, rect, 2, border_radius=8)