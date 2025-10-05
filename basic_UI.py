import pygame
import random

# 初始化
pygame.init()

class MonopolyBoard:
    def __init__(self, screen_width=1200, screen_height=800):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # 格子配置
        self.tile_size = 60  # 每个格子的大小
        self.tiles_per_side = 10  # 每边10个格子
        
        # 创建格子位置（顺时针）
        self.tiles = self.create_tiles()
        
        # 格子类型和图标
        self.tile_types = self.define_tile_types()
        
    def create_tiles(self):
        """生成40个格子的坐标"""
        tiles = []
        margin = 50  # 边距
        
        # 底边（从左到右）- 格子 0-9
        for i in range(self.tiles_per_side):
            tiles.append({
                'x': margin + i * self.tile_size,
                'y': self.screen_height - margin - self.tile_size,
                'index': i
            })
        
        # 右边（从下到上）- 格子 10-19
        for i in range(self.tiles_per_side):
            tiles.append({
                'x': self.screen_width - margin - self.tile_size,
                'y': self.screen_height - margin - self.tile_size - (i+1) * self.tile_size,
                'index': 10 + i
            })
        
        # 顶边（从右到左）- 格子 20-29
        for i in range(self.tiles_per_side):
            tiles.append({
                'x': self.screen_width - margin - self.tile_size - (i+1) * self.tile_size,
                'y': margin,
                'index': 20 + i
            })
        
        # 左边（从上到下）- 格子 30-39
        for i in range(self.tiles_per_side):
            tiles.append({
                'x': margin,
                'y': margin + (i+1) * self.tile_size,
                'index': 30 + i
            })
        
        return tiles
    
    def define_tile_types(self):
        """定义每个格子的类型"""
        types = ['START'] + ['RANDOM'] * 39  # 先全部设为随机
        
        # 手动设置特殊格子
        special_positions = {
            0: 'START',      # 起点
            10: 'EXCHANGE',  # 交易所
            20: 'JACKPOT',   # 大奖
            30: 'TRAP',      # 陷阱
            5: 'NEWS',
            15: 'NEWS',
            25: 'NEWS',
            35: 'NEWS',
        }
        
        for pos, tile_type in special_positions.items():
            types[pos] = tile_type
        
        # 随机填充其他格子
        random_types = ['BONUS', 'LUCKY', 'CHANCE', 'NEWS', 'QUEST']
        for i in range(40):
            if types[i] == 'RANDOM':
                types[i] = random.choice(random_types)
        
        return types
    
    def draw(self, screen, player_position):
        """绘制整个棋盘"""
        # 绘制中央背景
        center_rect = pygame.Rect(
            110, 110,
            self.screen_width - 220,
            self.screen_height - 220
        )
        pygame.draw.rect(screen, (30, 30, 50), center_rect)
        
        # 绘制所有格子
        for i, tile in enumerate(self.tiles):
            self.draw_tile(screen, tile, i, player_position)
    
    def draw_tile(self, screen, tile, index, player_position):
        """绘制单个格子"""
        tile_type = self.tile_types[index]
        
        # 格子颜色
        colors = {
            'START': (0, 255, 0),
            'BONUS': (255, 215, 0),
            'NEWS': (255, 100, 100),
            'LUCKY': (100, 100, 255),
            'CHANCE': (255, 165, 0),
            'EXCHANGE': (0, 200, 200),
            'TRAP': (150, 0, 0),
            'QUEST': (200, 0, 200),
            'JACKPOT': (255, 215, 0),
        }
        
        color = colors.get(tile_type, (100, 100, 100))
        
        # 绘制格子矩形
        rect = pygame.Rect(tile['x'], tile['y'], self.tile_size, self.tile_size)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (255, 255, 255), rect, 2)  # 白色边框
        
        # 绘制格子类型文字（不用emoji，防止字体问题）
        font = pygame.font.Font(None, 18)
        type_abbrev = {
            'START': 'GO',
            'BONUS': '$',
            'NEWS': 'N',
            'LUCKY': 'L',
            'CHANCE': '?',
            'EXCHANGE': 'EX',
            'TRAP': 'X',
            'QUEST': 'Q',
            'JACKPOT': '!!!',
        }
        
        abbrev = type_abbrev.get(tile_type, '?')
        text = font.render(abbrev, True, (255, 255, 255))
        screen.blit(text, (tile['x'] + 10, tile['y'] + 10))
        
        # 绘制索引编号（小字）
        small_font = pygame.font.Font(None, 14)
        index_text = small_font.render(str(index), True, (200, 200, 200))
        screen.blit(index_text, (tile['x'] + 5, tile['y'] + 42))
        
        # 玩家在这个格子上
        if index == player_position:
            self.draw_player_token(screen, tile)
    
    def draw_player_token(self, screen, tile):
        """绘制玩家标记"""
        center_x = tile['x'] + self.tile_size // 2
        center_y = tile['y'] + self.tile_size // 2
        
        # 绘制圆形玩家标记
        pygame.draw.circle(screen, (255, 0, 0), (center_x, center_y), 15)
        pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), 15, 2)


class Player:
    def __init__(self):
        self.position = 0
        self.target_position = 0
        self.is_moving = False
        self.move_speed = 15  # 每次移动多少帧
        self.move_counter = 0
        
    def move_to(self, steps):
        """设置移动目标"""
        self.target_position = (self.position + steps) % 40
        self.is_moving = True
        self.move_counter = 0
        
    def update(self):
        """更新玩家位置"""
        if self.is_moving:
            self.move_counter += 1
            
            if self.move_counter >= self.move_speed:
                self.move_counter = 0
                self.position = (self.position + 1) % 40
                
                # 到达目标位置
                if self.position == self.target_position:
                    self.is_moving = False
                    return True  # 移动完成
        
        return False  # 还在移动中


class Dice:
    def __init__(self):
        self.value = 1
        self.rolling = False
        self.roll_timer = 0
        
    def roll(self):
        """开始掷骰子"""
        self.rolling = True
        self.roll_timer = 30  # 30帧动画
        
    def update(self):
        """更新骰子动画"""
        if self.rolling:
            self.roll_timer -= 1
            self.value = random.randint(1, 6)  # 动画过程中随机显示
            
            if self.roll_timer <= 0:
                self.rolling = False
                self.value = random.randint(1, 6)  # 最终结果
                return self.value
        return None
    
    def draw(self, screen, x, y):
        """绘制骰子"""
        size = 80
        rect = pygame.Rect(x, y, size, size)
        
        # 骰子背景
        color = (255, 255, 200) if self.rolling else (255, 255, 255)
        pygame.draw.rect(screen, color, rect, border_radius=10)
        pygame.draw.rect(screen, (0, 0, 0), rect, 3, border_radius=10)
        
        # 骰子点数
        font = pygame.font.Font(None, 64)
        text = font.render(str(self.value), True, (0, 0, 0))
        text_rect = text.get_rect(center=(x + size//2, y + size//2))
        screen.blit(text, text_rect)


class CryptoMonopolyGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Crypto Monopoly Trading Game")
        self.clock = pygame.time.Clock()
        
        # 游戏组件
        self.board = MonopolyBoard()
        self.player = Player()
        self.dice = Dice()
        
        # 游戏状态
        self.state = "WAITING"  # WAITING, ROLLING, MOVING, EVENT
        self.running = True
        
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.state == "WAITING":
                    # 按空格掷骰子
                    self.dice.roll()
                    self.state = "ROLLING"
                    
    def update(self):
        if self.state == "ROLLING":
            result = self.dice.update()
            if result:  # 骰子停止
                self.player.move_to(result)
                self.state = "MOVING"
                
        elif self.state == "MOVING":
            if self.player.update():  # 移动完成
                self.state = "EVENT"  # 可以在这里处理格子事件
                # 暂时直接回到等待状态
                self.state = "WAITING"
                
    def draw(self):
        # 背景
        self.screen.fill((20, 20, 40))
        
        # 绘制棋盘
        self.board.draw(self.screen, self.player.position)
        
        # 绘制骰子
        self.dice.draw(self.screen, 560, 360)
        
        # 绘制UI提示
        font = pygame.font.Font(None, 36)
        if self.state == "WAITING":
            text = font.render("Press SPACE to roll dice", True, (255, 255, 255))
            self.screen.blit(text, (420, 300))
        elif self.state == "ROLLING":
            text = font.render("Rolling...", True, (255, 255, 0))
            self.screen.blit(text, (530, 300))
        elif self.state == "MOVING":
            text = font.render("Moving...", True, (0, 255, 255))
            self.screen.blit(text, (540, 300))
            
        # 显示当前位置
        small_font = pygame.font.Font(None, 24)
        pos_text = small_font.render(f"Position: {self.player.position}", True, (255, 255, 255))
        self.screen.blit(pos_text, (550, 500))
        
        tile_type = self.board.tile_types[self.player.position]
        type_text = small_font.render(f"Tile: {tile_type}", True, (255, 255, 255))
        self.screen.blit(type_text, (550, 530))
        
        pygame.display.flip()
        
    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()


if __name__ == "__main__":
    game = CryptoMonopolyGame()
    game.run()