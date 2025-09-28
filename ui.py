import pygame
from settings import *

class UI:
    """用户界面类"""

    def __init__(self):
        # 尝试使用中文字体
        try:
            self.font = pygame.font.Font("C:/Windows/Fonts/simhei.ttf", 36)
            self.small_font = pygame.font.Font("C:/Windows/Fonts/simhei.ttf", 24)
            self.title_font = pygame.font.Font("C:/Windows/Fonts/simhei.ttf", 48)
        except:
            # 如果中文字体不可用，使用默认字体
            self.font = pygame.font.Font(None, 36)
            self.small_font = pygame.font.Font(None, 24)
            self.title_font = pygame.font.Font(None, 48)

    def draw_hud(self, screen, score, time_left):
        """绘制游戏界面的HUD信息"""
        # 绘制HUD背景
        hud_rect = pygame.Rect(5, 5, 200, 120)
        pygame.draw.rect(screen, WHITE, hud_rect, border_radius=10)
        pygame.draw.rect(screen, DARK_GRAY, hud_rect, 2, border_radius=10)

        # 绘制分数
        score_text = self.font.render(f"得分: {score}", True, BLUE)
        screen.blit(score_text, (15, 15))

        # 绘制剩余时间（根据时间改变颜色）
        time_color = RED if time_left < 30 else (ORANGE if time_left < 60 else GREEN)
        time_text = self.font.render(f"时间: {time_left}秒", True, time_color)
        screen.blit(time_text, (15, 50))

        # 绘制操作提示
        hint_text = self.small_font.render("按Q键退出游戏", True, GRAY)
        screen.blit(hint_text, (15, 85))

    def draw_game_over(self, screen, won, final_score):
        """绘制游戏结束界面"""
        # 创建半透明覆盖层
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        # 绘制游戏结束信息
        if won:
            title_text = self.font.render("恭喜过关！", True, GREEN)
        else:
            title_text = self.font.render("游戏结束", True, RED)

        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(title_text, title_rect)

        # 绘制最终分数
        score_text = self.font.render(f"最终得分: {final_score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(score_text, score_rect)

        # 绘制重新开始提示
        restart_text = self.small_font.render("按R键重新开始，按Q键退出", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(restart_text, restart_rect)

    def draw_menu(self, screen):
        """绘制主菜单"""
        # 绘制渐变背景
        self.draw_menu_background(screen)

        # 绘制标题
        title_text = self.title_font.render("🎮 欢乐连连看 🎮", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        # 添加阴影效果
        shadow_text = self.title_font.render("🎮 欢乐连连看 🎮", True, DARK_GRAY)
        shadow_rect = title_rect.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        screen.blit(shadow_text, shadow_rect)
        screen.blit(title_text, title_rect)

        # 绘制游戏说明背景
        rules_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, 180, 400, 300)
        pygame.draw.rect(screen, WHITE, rules_rect, border_radius=15)
        pygame.draw.rect(screen, BLUE, rules_rect, 3, border_radius=15)

        # 绘制游戏说明
        rules = [
            "🎯 游戏规则：",
            "1. 点击两个相同的方块进行连接",
            "2. 连接路径不能超过两个转弯",
            "3. 在时间用完前消除所有方块",
            "",
            "⌨️ 操作说明：",
            "空格键 - 开始游戏",
            "Q键 - 退出游戏"
        ]

        y_offset = 200
        for i, rule in enumerate(rules):
            if "游戏规则" in rule:
                text = self.font.render(rule, True, BLUE)
            elif "操作说明" in rule:
                text = self.font.render(rule, True, GREEN)
            elif rule == "":
                continue
            else:
                text = self.small_font.render(rule, True, BLACK)

            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset + i * 30))
            screen.blit(text, text_rect)

        # 绘制开始游戏提示
        start_text = self.font.render("✨ 按空格键开始游戏 ✨", True, RED)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))

        # 添加闪烁效果
        import time
        if int(time.time() * 2) % 2:
            # 添加发光效果
            glow_text = self.font.render("✨ 按空格键开始游戏 ✨", True, YELLOW)
            glow_rect = start_rect.copy()
            for dx in [-2, -1, 0, 1, 2]:
                for dy in [-2, -1, 0, 1, 2]:
                    if dx != 0 or dy != 0:
                        glow_rect.x = start_rect.x + dx
                        glow_rect.y = start_rect.y + dy
                        screen.blit(glow_text, glow_rect)

        screen.blit(start_text, start_rect)

    def draw_menu_background(self, screen):
        """绘制菜单渐变背景"""
        for y in range(SCREEN_HEIGHT):
            color_value = int(100 + 100 * y / SCREEN_HEIGHT)
            color = (color_value, color_value + 50, 255)
            pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))