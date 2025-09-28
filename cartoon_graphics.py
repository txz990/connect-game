import pygame
import math
from settings import *

def create_cartoon_surface(size, shape_type, color, border_color=None):
    """创建卡通风格的图形表面"""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    center = size // 2

    if shape_type == "circle":
        # 绘制圆形
        pygame.draw.circle(surface, color, (center, center), center - 3)
        if border_color:
            pygame.draw.circle(surface, border_color, (center, center), center - 3, 3)

    elif shape_type == "star":
        # 绘制星形
        points = []
        for i in range(10):
            angle = math.pi * i / 5
            if i % 2 == 0:
                radius = center - 5
            else:
                radius = (center - 5) // 2
            x = center + radius * math.cos(angle - math.pi / 2)
            y = center + radius * math.sin(angle - math.pi / 2)
            points.append((x, y))
        pygame.draw.polygon(surface, color, points)
        if border_color:
            pygame.draw.polygon(surface, border_color, points, 2)

    elif shape_type == "heart":
        # 绘制心形
        draw_heart(surface, center, center, center - 5, color)
        if border_color:
            draw_heart_outline(surface, center, center, center - 5, border_color)

    elif shape_type == "diamond":
        # 绘制钻石
        points = [
            (center, 5),
            (size - 5, center),
            (center, size - 5),
            (5, center)
        ]
        pygame.draw.polygon(surface, color, points)
        if border_color:
            pygame.draw.polygon(surface, border_color, points, 2)

    elif shape_type == "triangle":
        # 绘制三角形
        points = [
            (center, 5),
            (size - 5, size - 5),
            (5, size - 5)
        ]
        pygame.draw.polygon(surface, color, points)
        if border_color:
            pygame.draw.polygon(surface, border_color, points, 2)

    elif shape_type == "flower":
        # 绘制花朵
        draw_flower(surface, center, center, center - 8, color)
        if border_color:
            draw_flower_outline(surface, center, center, center - 8, border_color)

    elif shape_type == "butterfly":
        # 绘制蝴蝶
        draw_butterfly(surface, center, center, center - 8, color)
        if border_color:
            draw_butterfly_outline(surface, center, center, center - 8, border_color)

    elif shape_type == "gem":
        # 绘制宝石
        draw_gem(surface, center, center, center - 5, color)
        if border_color:
            draw_gem_outline(surface, center, center, center - 5, border_color)

    return surface

def draw_heart(surface, x, y, size, color):
    """绘制心形"""
    # 简化的心形绘制
    pygame.draw.circle(surface, color, (x - size//3, y - size//4), size//3)
    pygame.draw.circle(surface, color, (x + size//3, y - size//4), size//3)
    points = [
        (x - size//2, y),
        (x, y + size//2),
        (x + size//2, y)
    ]
    pygame.draw.polygon(surface, color, points)

def draw_heart_outline(surface, x, y, size, color):
    """绘制心形轮廓"""
    pygame.draw.circle(surface, color, (x - size//3, y - size//4), size//3, 2)
    pygame.draw.circle(surface, color, (x + size//3, y - size//4), size//3, 2)

def draw_flower(surface, x, y, size, color):
    """绘制花朵"""
    # 花瓣
    petal_size = size // 3
    for i in range(6):
        angle = math.pi * i / 3
        petal_x = x + size//2 * math.cos(angle)
        petal_y = y + size//2 * math.sin(angle)
        pygame.draw.circle(surface, color, (int(petal_x), int(petal_y)), petal_size)

    # 花心
    pygame.draw.circle(surface, YELLOW, (x, y), petal_size//2)

def draw_flower_outline(surface, x, y, size, color):
    """绘制花朵轮廓"""
    petal_size = size // 3
    for i in range(6):
        angle = math.pi * i / 3
        petal_x = x + size//2 * math.cos(angle)
        petal_y = y + size//2 * math.sin(angle)
        pygame.draw.circle(surface, color, (int(petal_x), int(petal_y)), petal_size, 2)

def draw_butterfly(surface, x, y, size, color):
    """绘制蝴蝶"""
    # 左翅膀
    pygame.draw.ellipse(surface, color, (x - size, y - size//2, size, size))
    # 右翅膀
    pygame.draw.ellipse(surface, color, (x, y - size//2, size, size))
    # 身体
    pygame.draw.ellipse(surface, BLACK, (x - 2, y - size//2, 4, size), 0)

def draw_butterfly_outline(surface, x, y, size, color):
    """绘制蝴蝶轮廓"""
    pygame.draw.ellipse(surface, color, (x - size, y - size//2, size, size), 2)
    pygame.draw.ellipse(surface, color, (x, y - size//2, size, size), 2)

def draw_gem(surface, x, y, size, color):
    """绘制宝石"""
    points = [
        (x, y - size),
        (x - size//2, y - size//2),
        (x - size//3, y + size//2),
        (x + size//3, y + size//2),
        (x + size//2, y - size//2)
    ]
    pygame.draw.polygon(surface, color, points)

def draw_gem_outline(surface, x, y, size, color):
    """绘制宝石轮廓"""
    points = [
        (x, y - size),
        (x - size//2, y - size//2),
        (x - size//3, y + size//2),
        (x + size//3, y + size//2),
        (x + size//2, y - size//2)
    ]
    pygame.draw.polygon(surface, color, points, 2)

# 定义卡通图案类型和颜色
CARTOON_SHAPES = [
    ("circle", RED),
    ("star", YELLOW),
    ("heart", PINK),
    ("diamond", CYAN),
    ("triangle", GREEN),
    ("flower", PURPLE),
    ("butterfly", ORANGE),
    ("gem", BLUE)
]

def get_cartoon_surface(block_type, size=BLOCK_SIZE):
    """获取卡通图案表面"""
    if block_type <= 0 or block_type > len(CARTOON_SHAPES):
        return None

    shape_type, color = CARTOON_SHAPES[block_type - 1]
    return create_cartoon_surface(size - 4, shape_type, color, WHITE)