import random
from block import Block
from settings import *

class Board:
    """游戏面板类"""

    def __init__(self, size=BOARD_SIZE):
        self.size = size
        self.blocks = []
        self.selected_blocks = []
        self.animation_path = []  # 存储动画路径
        self.animation_timer = 0  # 动画计时器
        self.initialize_board()

    def initialize_board(self):
        """初始化游戏面板"""
        # 创建空的面板
        self.blocks = []
        for y in range(self.size):
            row = []
            for x in range(self.size):
                row.append(Block(x, y, 0))
            self.blocks.append(row)

        # 生成成对的方块
        self.generate_blocks()

    def generate_blocks(self):
        """生成成对的方块"""
        # 计算需要多少对方块（留出一些空白位置）
        total_positions = self.size * self.size
        pairs_count = (total_positions - 4) // 2  # 留出4个空位

        # 生成方块对
        block_types = []
        for i in range(pairs_count):
            block_type = (i % len(BLOCK_COLORS)) + 1
            block_types.extend([block_type, block_type])

        # 随机打乱位置
        random.shuffle(block_types)

        # 填充到面板中
        positions = []
        for y in range(self.size):
            for x in range(self.size):
                positions.append((x, y))

        random.shuffle(positions)

        # 分配方块类型到位置
        for i, (x, y) in enumerate(positions[:len(block_types)]):
            self.blocks[y][x].block_type = block_types[i]

    def get_block(self, x, y):
        """获取指定位置的方块"""
        if 0 <= x < self.size and 0 <= y < self.size:
            return self.blocks[y][x]
        return None

    def is_valid_position(self, x, y):
        """检查位置是否有效"""
        return 0 <= x < self.size and 0 <= y < self.size

    def is_position_empty(self, x, y):
        """检查位置是否为空"""
        if not self.is_valid_position(x, y):
            return False
        return self.blocks[y][x].is_empty()

    def click_block(self, x, y):
        """点击方块"""
        block = self.get_block(x, y)
        if not block or block.is_empty():
            return False

        # 如果已经选中了这个方块，取消选中
        if block in self.selected_blocks:
            block.selected = False
            self.selected_blocks.remove(block)
            return False

        # 如果已经选中了两个方块，清除选择
        if len(self.selected_blocks) >= 2:
            self.clear_selection()

        # 选中方块
        block.selected = True
        self.selected_blocks.append(block)

        # 如果选中了两个方块，检查是否可以消除
        if len(self.selected_blocks) == 2:
            return self.try_match()

        return False

    def try_match(self):
        """尝试匹配选中的两个方块"""
        if len(self.selected_blocks) != 2:
            return False

        block1, block2 = self.selected_blocks

        # 检查类型是否相同
        if not block1.is_same_type(block2):
            self.clear_selection()
            return False

        # 检查路径是否可达
        from path_finder import PathFinder
        path_finder = PathFinder(self)
        path = path_finder.find_path(block1.x, block1.y, block2.x, block2.y)
        if path:
            # 设置动画路径
            self.animation_path = path
            self.animation_timer = 30  # 30帧动画

            # 消除方块
            block1.block_type = 0
            block2.block_type = 0
            self.clear_selection()
            return True
        else:
            self.clear_selection()
            return False

    def clear_selection(self):
        """清除选择"""
        for block in self.selected_blocks:
            block.selected = False
        self.selected_blocks.clear()

    def is_game_over(self):
        """检查游戏是否结束"""
        # 检查是否还有方块
        for row in self.blocks:
            for block in row:
                if not block.is_empty():
                    return False
        return True

    def has_possible_moves(self):
        """检查是否还有可能的移动"""
        from path_finder import PathFinder
        path_finder = PathFinder(self)

        # 检查所有可能的方块对
        blocks = []
        for row in self.blocks:
            for block in row:
                if not block.is_empty():
                    blocks.append(block)

        for i in range(len(blocks)):
            for j in range(i + 1, len(blocks)):
                block1, block2 = blocks[i], blocks[j]
                if (block1.is_same_type(block2) and
                    path_finder.can_connect(block1.x, block1.y, block2.x, block2.y)):
                    return True

        return False

    def update_animation(self):
        """更新动画"""
        if self.animation_timer > 0:
            self.animation_timer -= 1
            if self.animation_timer <= 0:
                self.animation_path = []

    def draw(self, screen):
        """绘制游戏面板"""
        # 绘制渐变背景
        self.draw_gradient_background(screen)

        # 绘制游戏面板背景（圆角）
        board_rect = pygame.Rect(BOARD_X - 15, BOARD_Y - 15,
                                self.size * BLOCK_SIZE + 30,
                                self.size * BLOCK_SIZE + 30)
        pygame.draw.rect(screen, WHITE, board_rect, border_radius=15)
        pygame.draw.rect(screen, DARK_GRAY, board_rect, 3, border_radius=15)

        # 绘制网格（淡化）
        for y in range(self.size + 1):
            start_pos = (BOARD_X, BOARD_Y + y * BLOCK_SIZE)
            end_pos = (BOARD_X + self.size * BLOCK_SIZE, BOARD_Y + y * BLOCK_SIZE)
            pygame.draw.line(screen, LIGHT_GRAY, start_pos, end_pos, 1)

        for x in range(self.size + 1):
            start_pos = (BOARD_X + x * BLOCK_SIZE, BOARD_Y)
            end_pos = (BOARD_X + x * BLOCK_SIZE, BOARD_Y + self.size * BLOCK_SIZE)
            pygame.draw.line(screen, LIGHT_GRAY, start_pos, end_pos, 1)

        # 绘制所有方块
        for row in self.blocks:
            for block in row:
                block.draw(screen)

        # 绘制连线动画
        if self.animation_path and self.animation_timer > 0:
            self.draw_connection_animation(screen)

    def draw_gradient_background(self, screen):
        """绘制渐变背景"""
        # 简单的渐变效果
        for y in range(SCREEN_HEIGHT):
            color_value = int(200 + 55 * y / SCREEN_HEIGHT)
            color = (color_value, color_value + 20, 255)
            pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))

    def draw_connection_animation(self, screen):
        """绘制连线动画"""
        if len(self.animation_path) < 2:
            return

        # 计算动画进度
        progress = 1.0 - (self.animation_timer / 30.0)

        # 绘制路径
        points = []
        for x, y in self.animation_path:
            screen_x = BOARD_X + x * BLOCK_SIZE + BLOCK_SIZE // 2
            screen_y = BOARD_Y + y * BLOCK_SIZE + BLOCK_SIZE // 2
            points.append((screen_x, screen_y))

        if len(points) >= 2:
            # 绘制完整路径（淡化）
            pygame.draw.lines(screen, LIGHT_GRAY, False, points, 3)

            # 绘制动画部分（高亮）
            total_length = len(points) - 1
            current_length = progress * total_length

            if current_length >= 1:
                end_index = int(current_length) + 1
                animated_points = points[:end_index]

                # 如果有部分段，添加插值点
                if current_length != int(current_length) and end_index < len(points):
                    fraction = current_length - int(current_length)
                    start_point = points[end_index - 1]
                    end_point = points[end_index]
                    interpolated_x = start_point[0] + (end_point[0] - start_point[0]) * fraction
                    interpolated_y = start_point[1] + (end_point[1] - start_point[1]) * fraction
                    animated_points.append((interpolated_x, interpolated_y))

                if len(animated_points) >= 2:
                    pygame.draw.lines(screen, RED, False, animated_points, 5)