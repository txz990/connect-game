def get_board_position_from_screen(mouse_x, mouse_y):
    """将屏幕坐标转换为游戏面板坐标"""
    from settings import BOARD_X, BOARD_Y, BLOCK_SIZE, BOARD_SIZE

    grid_x = (mouse_x - BOARD_X) // BLOCK_SIZE
    grid_y = (mouse_y - BOARD_Y) // BLOCK_SIZE

    if 0 <= grid_x < BOARD_SIZE and 0 <= grid_y < BOARD_SIZE:
        return grid_x, grid_y
    return None, None

def get_screen_position_from_board(grid_x, grid_y):
    """将游戏面板坐标转换为屏幕坐标"""
    from settings import BOARD_X, BOARD_Y, BLOCK_SIZE

    screen_x = BOARD_X + grid_x * BLOCK_SIZE
    screen_y = BOARD_Y + grid_y * BLOCK_SIZE

    return screen_x, screen_y