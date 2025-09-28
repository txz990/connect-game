class PathFinder:
    """路径寻找算法类"""

    def __init__(self, board):
        self.board = board

    def find_path(self, x1, y1, x2, y2):
        """找到连接路径，返回路径点列表"""
        if not self.can_connect(x1, y1, x2, y2):
            return None

        # 尝试直线连接
        path = self.find_straight_path(x1, y1, x2, y2)
        if path:
            return path

        # 尝试一个转弯的连接
        path = self.find_one_turn_path(x1, y1, x2, y2)
        if path:
            return path

        # 尝试两个转弯的连接
        path = self.find_two_turns_path(x1, y1, x2, y2)
        if path:
            return path

        return None

    def find_straight_path(self, x1, y1, x2, y2):
        """找到直线路径"""
        if self.can_connect_straight(x1, y1, x2, y2):
            return [(x1, y1), (x2, y2)]
        return None

    def find_one_turn_path(self, x1, y1, x2, y2):
        """找到一个转弯的路径"""
        # 尝试路径：(x1,y1) -> (x2,y1) -> (x2,y2)
        if (self.is_path_clear(x1, y1, x2, y1) and
            self.is_path_clear(x2, y1, x2, y2) and
            (self.board.is_position_empty(x2, y1) or (x2 == x1 and y1 == y1) or (x2 == x2 and y1 == y2))):
            return [(x1, y1), (x2, y1), (x2, y2)]

        # 尝试路径：(x1,y1) -> (x1,y2) -> (x2,y2)
        if (self.is_path_clear(x1, y1, x1, y2) and
            self.is_path_clear(x1, y2, x2, y2) and
            (self.board.is_position_empty(x1, y2) or (x1 == x1 and y2 == y1) or (x1 == x2 and y2 == y2))):
            return [(x1, y1), (x1, y2), (x2, y2)]

        return None

    def find_two_turns_path(self, x1, y1, x2, y2):
        """找到两个转弯的路径"""
        # 尝试通过边界连接
        paths = [
            self.find_edge_path(x1, y1, x2, y2, -1, 'top'),
            self.find_edge_path(x1, y1, x2, y2, self.board.size, 'bottom'),
            self.find_edge_path(x1, y1, x2, y2, -1, 'left'),
            self.find_edge_path(x1, y1, x2, y2, self.board.size, 'right')
        ]

        for path in paths:
            if path:
                return path

        return None

    def find_edge_path(self, x1, y1, x2, y2, edge_pos, edge_type):
        """找到通过边界的路径"""
        if edge_type == 'top' or edge_type == 'bottom':
            y_edge = edge_pos
            if (self.is_path_clear_to_edge(x1, y1, x1, y_edge, edge_type) and
                self.is_path_clear_along_edge(x1, y_edge, x2, y_edge, edge_type) and
                self.is_path_clear_to_edge(x2, y_edge, x2, y2, edge_type)):
                return [(x1, y1), (x1, y_edge), (x2, y_edge), (x2, y2)]

        elif edge_type == 'left' or edge_type == 'right':
            x_edge = edge_pos
            if (self.is_path_clear_to_edge(x1, y1, x_edge, y1, edge_type) and
                self.is_path_clear_along_edge(x_edge, y1, x_edge, y2, edge_type) and
                self.is_path_clear_to_edge(x_edge, y2, x2, y2, edge_type)):
                return [(x1, y1), (x_edge, y1), (x_edge, y2), (x2, y2)]

        return None

    def can_connect(self, x1, y1, x2, y2):
        """检查两个位置是否可以连接"""
        # 如果是同一个位置，不能连接
        if x1 == x2 and y1 == y2:
            return False

        # 尝试直线连接
        if self.can_connect_straight(x1, y1, x2, y2):
            return True

        # 尝试一个转弯的连接
        if self.can_connect_one_turn(x1, y1, x2, y2):
            return True

        # 尝试两个转弯的连接
        if self.can_connect_two_turns(x1, y1, x2, y2):
            return True

        return False

    def can_connect_straight(self, x1, y1, x2, y2):
        """检查是否可以直线连接"""
        # 水平直线
        if y1 == y2:
            min_x, max_x = min(x1, x2), max(x1, x2)
            for x in range(min_x + 1, max_x):
                if not self.board.is_position_empty(x, y1):
                    return False
            return True

        # 垂直直线
        if x1 == x2:
            min_y, max_y = min(y1, y2), max(y1, y2)
            for y in range(min_y + 1, max_y):
                if not self.board.is_position_empty(x1, y):
                    return False
            return True

        return False

    def can_connect_one_turn(self, x1, y1, x2, y2):
        """检查是否可以通过一个转弯连接"""
        # 尝试路径：(x1,y1) -> (x2,y1) -> (x2,y2)
        if (self.is_path_clear(x1, y1, x2, y1) and
            self.is_path_clear(x2, y1, x2, y2) and
            (self.board.is_position_empty(x2, y1) or (x2 == x1 and y1 == y1) or (x2 == x2 and y1 == y2))):
            return True

        # 尝试路径：(x1,y1) -> (x1,y2) -> (x2,y2)
        if (self.is_path_clear(x1, y1, x1, y2) and
            self.is_path_clear(x1, y2, x2, y2) and
            (self.board.is_position_empty(x1, y2) or (x1 == x1 and y2 == y1) or (x1 == x2 and y2 == y2))):
            return True

        return False

    def can_connect_two_turns(self, x1, y1, x2, y2):
        """检查是否可以通过两个转弯连接"""
        # 尝试通过边界连接
        return (self.try_connect_through_edges(x1, y1, x2, y2))

    def try_connect_through_edges(self, x1, y1, x2, y2):
        """尝试通过边界连接"""
        # 尝试上边界
        if self.try_connect_through_edge(x1, y1, x2, y2, -1, 'top'):
            return True

        # 尝试下边界
        if self.try_connect_through_edge(x1, y1, x2, y2, self.board.size, 'bottom'):
            return True

        # 尝试左边界
        if self.try_connect_through_edge(x1, y1, x2, y2, -1, 'left'):
            return True

        # 尝试右边界
        if self.try_connect_through_edge(x1, y1, x2, y2, self.board.size, 'right'):
            return True

        return False

    def try_connect_through_edge(self, x1, y1, x2, y2, edge_pos, edge_type):
        """尝试通过指定边界连接"""
        if edge_type == 'top' or edge_type == 'bottom':
            # 通过上下边界
            y_edge = edge_pos
            # 路径：(x1,y1) -> (x1,y_edge) -> (x2,y_edge) -> (x2,y2)
            if (self.is_path_clear_to_edge(x1, y1, x1, y_edge, edge_type) and
                self.is_path_clear_along_edge(x1, y_edge, x2, y_edge, edge_type) and
                self.is_path_clear_to_edge(x2, y_edge, x2, y2, edge_type)):
                return True

        elif edge_type == 'left' or edge_type == 'right':
            # 通过左右边界
            x_edge = edge_pos
            # 路径：(x1,y1) -> (x_edge,y1) -> (x_edge,y2) -> (x2,y2)
            if (self.is_path_clear_to_edge(x1, y1, x_edge, y1, edge_type) and
                self.is_path_clear_along_edge(x_edge, y1, x_edge, y2, edge_type) and
                self.is_path_clear_to_edge(x_edge, y2, x2, y2, edge_type)):
                return True

        return False

    def is_path_clear(self, x1, y1, x2, y2):
        """检查路径是否畅通（不包括起点和终点）"""
        if x1 == x2:  # 垂直路径
            min_y, max_y = min(y1, y2), max(y1, y2)
            for y in range(min_y + 1, max_y):
                if not self.board.is_position_empty(x1, y):
                    return False
        elif y1 == y2:  # 水平路径
            min_x, max_x = min(x1, x2), max(x1, x2)
            for x in range(min_x + 1, max_x):
                if not self.board.is_position_empty(x, y1):
                    return False
        else:
            return False

        return True

    def is_path_clear_to_edge(self, x1, y1, x2, y2, edge_type):
        """检查到边界的路径是否畅通"""
        if edge_type in ['top', 'bottom']:
            # 垂直移动到边界
            if x1 != x2:
                return False
            if edge_type == 'top':
                # 向上移动
                for y in range(min(y1, y2), max(y1, y2)):
                    if y != y1 and not self.board.is_position_empty(x1, y):
                        return False
            else:
                # 向下移动
                for y in range(min(y1, y2) + 1, max(y1, y2) + 1):
                    if y != y1 and not self.board.is_position_empty(x1, y):
                        return False
        else:
            # 水平移动到边界
            if y1 != y2:
                return False
            if edge_type == 'left':
                # 向左移动
                for x in range(min(x1, x2), max(x1, x2)):
                    if x != x1 and not self.board.is_position_empty(x, y1):
                        return False
            else:
                # 向右移动
                for x in range(min(x1, x2) + 1, max(x1, x2) + 1):
                    if x != x1 and not self.board.is_position_empty(x, y1):
                        return False

        return True

    def is_path_clear_along_edge(self, x1, y1, x2, y2, edge_type):
        """检查沿边界的路径是否畅通"""
        # 边界路径总是畅通的
        return True