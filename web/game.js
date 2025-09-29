class ConnectGame {
    constructor() {
        this.boardSize = 8;
        this.board = [];
        this.selectedBlocks = [];
        this.score = 0;
        this.timeLeft = 300; // 5分钟
        this.gameState = 'menu'; // menu, playing, gameOver
        this.timer = null;
        this.blockTypes = ['🔴', '⭐', '💖', '💎', '🔺', '🌸', '🦋', '💠'];
        this.animationTimeout = null;
        this.isProcessingMatch = false; // 防止快速点击导致的重复处理

        this.initEventListeners();
    }

    initEventListeners() {
        document.addEventListener('keydown', (e) => {
            if (e.key.toLowerCase() === 'q') {
                if (this.gameState === 'playing') {
                    this.showMenu();
                }
            }
        });
    }

    showMenu() {
        this.gameState = 'menu';
        document.getElementById('menu').classList.remove('hidden');
        document.getElementById('game').classList.add('hidden');
        document.getElementById('gameOverOverlay').classList.add('hidden');
        this.stopTimer();
    }

    startGame() {
        this.gameState = 'playing';
        this.score = 0;
        this.timeLeft = 300;
        this.selectedBlocks = [];
        this.isProcessingMatch = false; // 重置处理状态

        document.getElementById('menu').classList.add('hidden');
        document.getElementById('game').classList.remove('hidden');
        document.getElementById('gameOverOverlay').classList.add('hidden');

        this.initBoard();
        this.renderBoard();
        this.updateHUD();
        this.startTimer();
    }

    initBoard() {
        this.board = [];

        // 创建空棋盘
        for (let y = 0; y < this.boardSize; y++) {
            this.board[y] = [];
            for (let x = 0; x < this.boardSize; x++) {
                this.board[y][x] = 0; // 0表示空
            }
        }

        // 生成成对的方块
        const totalPositions = this.boardSize * this.boardSize;
        const pairsCount = Math.floor((totalPositions - 4) / 2); // 留出一些空位

        const blockTypes = [];
        for (let i = 0; i < pairsCount; i++) {
            const blockType = (i % this.blockTypes.length) + 1;
            blockTypes.push(blockType, blockType);
        }

        // 随机打乱
        this.shuffleArray(blockTypes);

        // 获取所有位置并随机打乱
        const positions = [];
        for (let y = 0; y < this.boardSize; y++) {
            for (let x = 0; x < this.boardSize; x++) {
                positions.push({x, y});
            }
        }
        this.shuffleArray(positions);

        // 分配方块类型到位置
        for (let i = 0; i < blockTypes.length && i < positions.length; i++) {
            const pos = positions[i];
            this.board[pos.y][pos.x] = blockTypes[i];
        }
    }

    shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
    }

    renderBoard() {
        const gameBoard = document.getElementById('gameBoard');
        gameBoard.innerHTML = '';

        for (let y = 0; y < this.boardSize; y++) {
            for (let x = 0; x < this.boardSize; x++) {
                const block = document.createElement('div');
                block.className = 'block';
                block.dataset.x = x;
                block.dataset.y = y;

                const blockType = this.board[y][x];
                if (blockType === 0) {
                    block.classList.add('empty');
                } else {
                    block.classList.add(`type-${blockType}`);
                    block.textContent = this.blockTypes[blockType - 1];
                    block.addEventListener('click', () => this.onBlockClick(x, y));
                }

                gameBoard.appendChild(block);
            }
        }
    }

    onBlockClick(x, y) {
        if (this.gameState !== 'playing' || this.isProcessingMatch) return;

        const blockType = this.board[y][x];
        if (blockType === 0) return;

        const blockElement = document.querySelector(`[data-x="${x}"][data-y="${y}"]`);

        // 检查是否已经选中
        const selectedIndex = this.selectedBlocks.findIndex(b => b.x === x && b.y === y);
        if (selectedIndex !== -1) {
            // 取消选中
            this.selectedBlocks.splice(selectedIndex, 1);
            blockElement.classList.remove('selected');
            return;
        }

        // 如果已经选中了两个方块，清除选择
        if (this.selectedBlocks.length >= 2) {
            this.clearSelection();
        }

        // 选中方块
        this.selectedBlocks.push({x, y, type: blockType});
        blockElement.classList.add('selected');

        // 如果选中了两个方块，尝试匹配
        if (this.selectedBlocks.length === 2) {
            this.isProcessingMatch = true;
            setTimeout(() => this.tryMatch(), 50); // 减少延迟
        }
    }

    tryMatch() {
        if (this.selectedBlocks.length !== 2) {
            this.isProcessingMatch = false;
            return;
        }

        const [block1, block2] = this.selectedBlocks;

        // 检查类型是否相同
        if (block1.type !== block2.type) {
            this.clearSelection();
            this.isProcessingMatch = false;
            return;
        }

        // 检查路径是否可达
        const path = this.findPath(block1.x, block1.y, block2.x, block2.y);
        console.log('找到的路径:', path);

        if (path) {
            // 立即消除方块和更新状态，不等待动画
            this.board[block1.y][block1.x] = 0;
            this.board[block2.y][block2.x] = 0;
            this.score += 10;

            // 显示连线动画（不阻塞操作）
            this.showConnectionAnimation(path);

            // 立即更新界面和重置状态
            this.clearSelection();
            this.renderBoard();
            this.updateHUD();
            this.isProcessingMatch = false;

            // 检查游戏是否结束
            if (this.isGameWon()) {
                this.endGame(true);
            } else if (!this.hasPossibleMoves()) {
                this.endGame(false);
            }
        } else {
            // 添加失败效果
            this.selectedBlocks.forEach(block => {
                const element = document.querySelector(`[data-x="${block.x}"][data-y="${block.y}"]`);
                if (element) {
                    element.style.animation = 'shake 0.3s ease-in-out';
                    setTimeout(() => {
                        element.style.animation = '';
                    }, 300);
                }
            });

            setTimeout(() => {
                this.clearSelection();
                this.isProcessingMatch = false;
            }, 300);
        }
    }

    findPath(x1, y1, x2, y2) {
        // 简化的路径查找算法

        // 直线连接
        if (this.canConnectStraight(x1, y1, x2, y2)) {
            return [{x: x1, y: y1}, {x: x2, y: y2}];
        }

        // 一个转弯
        const oneTurnPath = this.findOneTurnPath(x1, y1, x2, y2);
        if (oneTurnPath) return oneTurnPath;

        // 两个转弯（通过边界）
        const twoTurnPath = this.findTwoTurnPath(x1, y1, x2, y2);
        if (twoTurnPath) return twoTurnPath;

        return null;
    }

    canConnectStraight(x1, y1, x2, y2) {
        if (y1 === y2) {
            // 水平连接
            const minX = Math.min(x1, x2);
            const maxX = Math.max(x1, x2);
            for (let x = minX + 1; x < maxX; x++) {
                if (this.board[y1][x] !== 0) return false;
            }
            return true;
        }

        if (x1 === x2) {
            // 垂直连接
            const minY = Math.min(y1, y2);
            const maxY = Math.max(y1, y2);
            for (let y = minY + 1; y < maxY; y++) {
                if (this.board[y][x1] !== 0) return false;
            }
            return true;
        }

        return false;
    }

    findOneTurnPath(x1, y1, x2, y2) {
        // 尝试路径：(x1,y1) -> (x2,y1) -> (x2,y2)
        if (this.isPathClear(x1, y1, x2, y1) &&
            this.isPathClear(x2, y1, x2, y2) &&
            (this.board[y1][x2] === 0 || (x2 === x1 && y1 === y1) || (x2 === x2 && y1 === y2))) {
            return [{x: x1, y: y1}, {x: x2, y: y1}, {x: x2, y: y2}];
        }

        // 尝试路径：(x1,y1) -> (x1,y2) -> (x2,y2)
        if (this.isPathClear(x1, y1, x1, y2) &&
            this.isPathClear(x1, y2, x2, y2) &&
            (this.board[y2][x1] === 0 || (x1 === x1 && y2 === y1) || (x1 === x2 && y2 === y2))) {
            return [{x: x1, y: y1}, {x: x1, y: y2}, {x: x2, y: y2}];
        }

        return null;
    }

    findTwoTurnPath(x1, y1, x2, y2) {
        // 尝试通过边界连接（改进实现）

        // 通过上边界
        if (this.canReachTop(x1, y1) && this.canReachTop(x2, y2)) {
            return [{x: x1, y: y1}, {x: x1, y: -1}, {x: x2, y: -1}, {x: x2, y: y2}];
        }

        // 通过下边界
        if (this.canReachBottom(x1, y1) && this.canReachBottom(x2, y2)) {
            return [{x: x1, y: y1}, {x: x1, y: this.boardSize}, {x: x2, y: this.boardSize}, {x: x2, y: y2}];
        }

        // 通过左边界
        if (this.canReachLeft(x1, y1) && this.canReachLeft(x2, y2)) {
            return [{x: x1, y: y1}, {x: -1, y: y1}, {x: -1, y: y2}, {x: x2, y: y2}];
        }

        // 通过右边界
        if (this.canReachRight(x1, y1) && this.canReachRight(x2, y2)) {
            return [{x: x1, y: y1}, {x: this.boardSize, y: y1}, {x: this.boardSize, y: y2}, {x: x2, y: y2}];
        }

        return null;
    }

    canReachTop(x, y) {
        for (let i = y - 1; i >= 0; i--) {
            if (this.board[i][x] !== 0) return false;
        }
        return true;
    }

    canReachBottom(x, y) {
        for (let i = y + 1; i < this.boardSize; i++) {
            if (this.board[i][x] !== 0) return false;
        }
        return true;
    }

    canReachLeft(x, y) {
        for (let i = x - 1; i >= 0; i--) {
            if (this.board[y][i] !== 0) return false;
        }
        return true;
    }

    canReachRight(x, y) {
        for (let i = x + 1; i < this.boardSize; i++) {
            if (this.board[y][i] !== 0) return false;
        }
        return true;
    }

    isPathClear(x1, y1, x2, y2) {
        if (x1 === x2) {
            const minY = Math.min(y1, y2);
            const maxY = Math.max(y1, y2);
            for (let y = minY + 1; y < maxY; y++) {
                if (this.board[y][x1] !== 0) return false;
            }
        } else if (y1 === y2) {
            const minX = Math.min(x1, x2);
            const maxX = Math.max(x1, x2);
            for (let x = minX + 1; x < maxX; x++) {
                if (this.board[y1][x] !== 0) return false;
            }
        } else {
            return false;
        }
        return true;
    }

    showConnectionAnimation(path) {
        console.log('显示连线动画:', path);

        if (!path || path.length < 2) {
            console.log('路径无效，取消动画');
            return;
        }

        // 如果有正在进行的动画，先清除
        if (this.animationTimeout) {
            clearTimeout(this.animationTimeout);
            this.animationTimeout = null;
        }

        const gameBoard = document.getElementById('gameBoard');
        const gameBoardRect = gameBoard.getBoundingClientRect();

        // 清除之前的动画线条
        const existingLines = document.querySelectorAll('.connection-line');
        existingLines.forEach(line => line.remove());

        // 清除旧的动画容器
        const oldContainers = document.querySelectorAll('.animation-container');
        oldContainers.forEach(container => container.remove());

        // 创建动画容器，相对于整个页面定位
        const animationContainer = document.createElement('div');
        animationContainer.className = 'animation-container';
        animationContainer.style.position = 'fixed';
        animationContainer.style.top = '0';
        animationContainer.style.left = '0';
        animationContainer.style.width = '100vw';
        animationContainer.style.height = '100vh';
        animationContainer.style.pointerEvents = 'none';
        animationContainer.style.zIndex = '1000';
        document.body.appendChild(animationContainer);

        // 计算方块的实际大小和间距 (60px方块 + 2px间距)
        const blockSize = 60;
        const gap = 2;
        const cellSize = blockSize + gap;

        // 辅助函数：获取屏幕坐标
        const getScreenCoord = (x, y) => {
            let screenX, screenY;

            if (x < 0) {
                screenX = gameBoardRect.left - 15;
            } else if (x >= this.boardSize) {
                screenX = gameBoardRect.left + 15 + this.boardSize * cellSize + 15;
            } else {
                screenX = gameBoardRect.left + 15 + x * cellSize + blockSize / 2;
            }

            if (y < 0) {
                screenY = gameBoardRect.top - 15;
            } else if (y >= this.boardSize) {
                screenY = gameBoardRect.top + 15 + this.boardSize * cellSize + 15;
            } else {
                screenY = gameBoardRect.top + 15 + y * cellSize + blockSize / 2;
            }

            return { x: screenX, y: screenY };
        };

        // 为每段路径创建线条，使用实际的路径
        for (let i = 0; i < path.length - 1; i++) {
            const start = path[i];
            const end = path[i + 1];

            const line = document.createElement('div');
            line.className = 'connection-line';

            const startCoord = getScreenCoord(start.x, start.y);
            const endCoord = getScreenCoord(end.x, end.y);

            console.log(`线段 ${i}: (${start.x}, ${start.y}) -> (${end.x}, ${end.y})`);
            console.log(`屏幕坐标: (${startCoord.x}, ${startCoord.y}) -> (${endCoord.x}, ${endCoord.y})`);

            // 计算线条属性
            const deltaX = endCoord.x - startCoord.x;
            const deltaY = endCoord.y - startCoord.y;
            const length = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
            const angle = Math.atan2(deltaY, deltaX) * 180 / Math.PI;

            // 设置线条样式
            line.style.position = 'absolute';
            line.style.left = startCoord.x + 'px';
            line.style.top = (startCoord.y - 4) + 'px'; // 减去线条高度的一半以居中
            line.style.width = length + 'px';
            line.style.height = '8px';
            line.style.background = 'linear-gradient(90deg, #fd79a8, #fdcb6e, #fd79a8)';
            line.style.transform = `rotate(${angle}deg)`;
            line.style.transformOrigin = '0 50%';
            line.style.borderRadius = '4px';
            line.style.boxShadow = '0 0 15px rgba(253, 121, 168, 0.8)';
            line.style.border = '2px solid #fff';

            // 使用CSS动画而不是延迟，让所有线段同时出现
            line.style.animation = 'connectionAppear 0.4s ease-in-out forwards';

            animationContainer.appendChild(line);
        }

        // 添加连线出现动画的CSS
        if (!document.getElementById('connectionAnimationStyle')) {
            const style = document.createElement('style');
            style.id = 'connectionAnimationStyle';
            style.textContent = `
                @keyframes connectionAppear {
                    0% {
                        opacity: 0;
                        transform: scale(0);
                        filter: brightness(2);
                    }
                    50% {
                        opacity: 1;
                        transform: scale(1.1);
                        filter: brightness(1.5);
                    }
                    100% {
                        opacity: 1;
                        transform: scale(1);
                        filter: brightness(1);
                    }
                }

                @keyframes connectionFadeOut {
                    0% {
                        opacity: 1;
                        transform: scale(1);
                    }
                    100% {
                        opacity: 0;
                        transform: scale(0.8);
                    }
                }

                .connection-line {
                    opacity: 0;
                }
            `;
            document.head.appendChild(style);
        }

        // 0.5秒后开始淡出动画
        this.animationTimeout = setTimeout(() => {
            const lines = animationContainer.querySelectorAll('.connection-line');
            lines.forEach(line => {
                line.style.animation = 'connectionFadeOut 0.2s ease-in-out forwards';
            });

            // 再0.2秒后清除容器
            setTimeout(() => {
                if (animationContainer && animationContainer.parentNode) {
                    animationContainer.remove();
                }
                this.animationTimeout = null;
            }, 200);
        }, 500);
    }

    clearSelection() {
        this.selectedBlocks.forEach(block => {
            const blockElement = document.querySelector(`[data-x="${block.x}"][data-y="${block.y}"]`);
            if (blockElement) {
                blockElement.classList.remove('selected');
            }
        });
        this.selectedBlocks = [];
    }

    isGameWon() {
        for (let y = 0; y < this.boardSize; y++) {
            for (let x = 0; x < this.boardSize; x++) {
                if (this.board[y][x] !== 0) return false;
            }
        }
        return true;
    }

    hasPossibleMoves() {
        const blocks = [];
        for (let y = 0; y < this.boardSize; y++) {
            for (let x = 0; x < this.boardSize; x++) {
                if (this.board[y][x] !== 0) {
                    blocks.push({x, y, type: this.board[y][x]});
                }
            }
        }

        for (let i = 0; i < blocks.length; i++) {
            for (let j = i + 1; j < blocks.length; j++) {
                const block1 = blocks[i];
                const block2 = blocks[j];
                if (block1.type === block2.type &&
                    this.findPath(block1.x, block1.y, block2.x, block2.y)) {
                    return true;
                }
            }
        }
        return false;
    }

    startTimer() {
        this.stopTimer();
        this.timer = setInterval(() => {
            this.timeLeft--;
            this.updateHUD();

            if (this.timeLeft <= 0) {
                this.endGame(false);
            }
        }, 1000);
    }

    stopTimer() {
        if (this.timer) {
            clearInterval(this.timer);
            this.timer = null;
        }
    }

    updateHUD() {
        document.getElementById('score').textContent = this.score;

        const timerElement = document.getElementById('timer');
        timerElement.textContent = `时间: ${this.timeLeft}秒`;

        // 根据剩余时间改变颜色
        timerElement.className = 'time';
        if (this.timeLeft < 30) {
            timerElement.classList.add('danger');
        } else if (this.timeLeft < 60) {
            timerElement.classList.add('warning');
        }
    }

    endGame(won) {
        this.gameState = 'gameOver';
        this.stopTimer();

        const overlay = document.getElementById('gameOverOverlay');
        const title = document.getElementById('gameOverTitle');
        const finalScore = document.getElementById('finalScore');

        if (won) {
            title.textContent = '🎉 恭喜过关！';
            title.className = 'game-over-title win';
            // 时间奖励
            const timeBonus = this.timeLeft;
            this.score += timeBonus;
        } else {
            title.textContent = '😢 游戏结束';
            title.className = 'game-over-title lose';
        }

        finalScore.textContent = this.score;
        overlay.classList.remove('hidden');
    }
}

// 全局函数
let game;

function startGame() {
    if (!game) {
        game = new ConnectGame();
    }
    game.startGame();
}

function showMenu() {
    if (game) {
        game.showMenu();
    }
}

// 初始化游戏
document.addEventListener('DOMContentLoaded', () => {
    game = new ConnectGame();
});