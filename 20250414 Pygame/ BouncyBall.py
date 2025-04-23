import pygame

class Ball:
    def __init__(self, screen, color, radius, pos, velocity):
        self.screen = screen
        self.color = color
        self.radius = radius
        self.pos = pos
        self.velocity = velocity
    
    def update(self, screen_width, screen_height):
        # 更新位置
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        
        # 檢查左右邊界，若碰到則反轉 x 軸速度
        if self.pos[0] - self.radius <= 0 or self.pos[0] + self.radius >= screen_width:
            self.velocity[0] = -self.velocity[0]
            
        # 檢查上下邊界，若碰到則反轉 y 軸速度
        if self.pos[1] - self.radius <= 0 or self.pos[1] + self.radius >= screen_height:
            self.velocity[1] = -self.velocity[1]
    
    def draw(self):
        pygame.draw.circle(self.screen, self.color, (int(self.pos[0]), int(self.pos[1])), self.radius)

def main():
    # 初始化 Pygame
    pygame.init()
    
    # 設定視窗大小和標題
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("BouncyBall")
    
    # 創建兩個球
    ball1 = Ball(
        screen=screen,
        color=(255, 255, 255),  # 白色
        radius=20,
        pos=[screen_width // 2, screen_height // 2],  # 初始位置在畫面中央
        velocity=[3, 3]
    )
    
    ball2 = Ball(
        screen=screen,
        color=(255, 0, 0),  # 紅色
        radius=30,  # 不同的半徑
        pos=[screen_width // 4, screen_height // 3],  # 不同的初始位置
        velocity=[5, 2]  # 不同的速度
    )
    
    clock = pygame.time.Clock()
    running = True
    
    # 主迴圈：持續更新與繪製
    while running:
        # 處理事件，當使用者關閉視窗時結束程式
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # 設定背景色為黑色並清空畫面
        screen.fill((0, 0, 0))
        
        # 更新球的位置及反彈邏輯
        ball1.update(screen_width, screen_height)
        ball2.update(screen_width, screen_height)
        
        # 繪製球
        ball1.draw()
        ball2.draw()
        
        # 更新畫面
        pygame.display.flip()
        
        # 控制遊戲速度
        clock.tick(60)
    
    # 結束 Pygame
    pygame.quit()

if __name__ == "__main__":
    main()