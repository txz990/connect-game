import pygame
import time
from board import Board
from ui import UI
from settings import *

class Game:
    """主游戏类"""

    def __init__(self):
        self.board = Board()
        self.ui = UI()
        self.score = 0
        self.start_time = None
        self.end_time = None
        self.game_state = "menu"  # menu, playing, game_over
        self.won = False

    def start_new_game(self):
        """开始新游戏"""
        self.board = Board()
        self.score = 0
        self.start_time = time.time()
        self.end_time = None
        self.game_state = "playing"
        self.won = False

    def get_time_left(self):
        """获取剩余时间"""
        if self.start_time is None:
            return GAME_TIME

        # 如果游戏已结束，使用结束时的时间
        if self.end_time is not None:
            elapsed = self.end_time - self.start_time
        else:
            elapsed = time.time() - self.start_time

        return max(0, GAME_TIME - int(elapsed))

    def is_time_up(self):
        """检查时间是否用完"""
        return self.get_time_left() <= 0

    def handle_click(self, pos):
        """处理鼠标点击"""
        if self.game_state != "playing":
            return

        mouse_x, mouse_y = pos

        # 计算点击的网格坐标
        grid_x = (mouse_x - BOARD_X) // BLOCK_SIZE
        grid_y = (mouse_y - BOARD_Y) // BLOCK_SIZE

        # 检查点击是否在有效范围内
        if (0 <= grid_x < self.board.size and 0 <= grid_y < self.board.size):
            if self.board.click_block(grid_x, grid_y):
                # 成功匹配，增加分数
                self.score += POINTS_PER_MATCH

                # 检查游戏是否获胜
                if self.board.is_game_over():
                    self.won = True
                    self.end_time = time.time()  # 记录结束时间
                    self.game_state = "game_over"
                    # 时间奖励
                    time_bonus = self.get_time_left() * TIME_BONUS_MULTIPLIER
                    self.score += time_bonus

    def update(self):
        """更新游戏状态"""
        if self.game_state == "playing":
            # 更新动画
            self.board.update_animation()

            # 检查时间是否用完
            if self.is_time_up():
                self.won = False
                self.end_time = time.time()  # 记录结束时间
                self.game_state = "game_over"

            # 检查是否还有可能的移动
            elif not self.board.has_possible_moves():
                self.won = False
                self.end_time = time.time()  # 记录结束时间
                self.game_state = "game_over"

    def handle_key(self, key):
        """处理键盘输入"""
        if self.game_state == "menu":
            if key == pygame.K_SPACE:
                self.start_new_game()
            elif key == pygame.K_q:
                return False

        elif self.game_state == "playing":
            if key == pygame.K_q:
                return False

        elif self.game_state == "game_over":
            if key == pygame.K_r:
                self.start_new_game()
            elif key == pygame.K_q:
                return False

        return True

    def draw(self, screen):
        """绘制游戏"""
        screen.fill(WHITE)

        if self.game_state == "menu":
            self.ui.draw_menu(screen)

        elif self.game_state == "playing":
            # 绘制游戏面板
            self.board.draw(screen)

            # 绘制HUD
            self.ui.draw_hud(screen, self.score, self.get_time_left())

        elif self.game_state == "game_over":
            # 绘制游戏面板
            self.board.draw(screen)

            # 绘制HUD
            self.ui.draw_hud(screen, self.score, self.get_time_left())

            # 绘制游戏结束界面
            self.ui.draw_game_over(screen, self.won, self.score)