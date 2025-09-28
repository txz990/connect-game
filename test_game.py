#!/usr/bin/env python3
"""
连连看游戏测试脚本
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from board import Board
from path_finder import PathFinder
from block import Block

def test_board_creation():
    """测试面板创建"""
    print("测试面板创建...")
    board = Board()

    # 检查面板大小
    assert board.size == 8, f"面板大小错误：期望8，实际{board.size}"

    # 检查是否有方块
    block_count = 0
    for row in board.blocks:
        for block in row:
            if not block.is_empty():
                block_count += 1

    print(f"面板中有{block_count}个方块")
    assert block_count > 0, "面板中没有方块"
    print("面板创建测试通过")

def test_path_finding():
    """测试路径寻找"""
    print("\n测试路径寻找...")

    # 创建一个简单的测试面板
    board = Board()

    # 清空面板
    for row in board.blocks:
        for block in row:
            block.block_type = 0

    # 放置两个相同的方块
    board.blocks[0][0].block_type = 1
    board.blocks[0][2].block_type = 1

    path_finder = PathFinder(board)

    # 测试直线连接
    can_connect = path_finder.can_connect(0, 0, 2, 0)
    assert can_connect, "应该能够直线连接"

    # 在中间放置障碍物
    board.blocks[0][1].block_type = 2
    can_connect = path_finder.can_connect(0, 0, 2, 0)
    assert not can_connect, "不应该能够穿过障碍物连接"

    print("路径寻找测试通过")

def test_block_matching():
    """测试方块匹配"""
    print("\n测试方块匹配...")

    board = Board()

    # 清空面板
    for row in board.blocks:
        for block in row:
            block.block_type = 0

    # 放置两个相同的方块
    board.blocks[0][0].block_type = 1
    board.blocks[0][1].block_type = 1

    # 测试点击匹配
    result1 = board.click_block(0, 0)
    assert not result1, "第一次点击不应该返回匹配"

    result2 = board.click_block(1, 0)
    assert result2, "第二次点击应该返回匹配"

    # 检查方块是否被消除
    assert board.blocks[0][0].is_empty(), "第一个方块应该被消除"
    assert board.blocks[0][1].is_empty(), "第二个方块应该被消除"

    print("方块匹配测试通过")

def test_game_over_conditions():
    """测试游戏结束条件"""
    print("\n测试游戏结束条件...")

    board = Board()

    # 清空所有方块
    for row in board.blocks:
        for block in row:
            block.block_type = 0

    # 测试游戏胜利条件
    assert board.is_game_over(), "空面板应该表示游戏结束"

    # 放置一个方块
    board.blocks[0][0].block_type = 1
    assert not board.is_game_over(), "有方块时游戏不应该结束"

    print("游戏结束条件测试通过")

def run_all_tests():
    """运行所有测试"""
    print("开始运行连连看游戏测试...")
    print("=" * 50)

    try:
        test_board_creation()
        test_path_finding()
        test_block_matching()
        test_game_over_conditions()

        print("\n" + "=" * 50)
        print("所有测试通过！游戏核心功能正常工作。")

    except AssertionError as e:
        print(f"\n测试失败：{e}")
        return False
    except Exception as e:
        print(f"\n测试出错：{e}")
        return False

    return True

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)