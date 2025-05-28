# monkey_balloons_pygame.py
"""
Simple tower‑defense demo inspired by "Monkey shoots balloons".

v1.1 features
-------------
* Press 1 or 2 to choose tower type before placing.
* HUD shows each tower price & current selection.
* Two towers, two monsters, three waves.

"""

import math
import sys
from collections import deque

import pygame

# ----------------------------- CONFIG ------------------------------------
#畫面和字體
SCREEN_W, SCREEN_H = 960, 540 ## 這個是螢幕大小 16*9
FPS = 60 #FPS
FONT_NAME = pygame.font.get_default_font() #取得 Pygame 預設使用的字體，OS不同會不同(？)

#遊戲初始參數 生命、錢、幾波
STARTING_LIVES = 20
STARTING_MONEY = 200
TOWER_COST = {"PeaShooter": 50, "RapidFox": 80}
WAVES = [
    (40, [("RunningRat", 8), ("HeavyToad", 3)]),
    (35, [("RunningRat", 12), ("HeavyToad", 6)]),
    (30, [("RunningRat", 20), ("HeavyToad", 10)]),
]

#先定義顏色的RGB，後面直接使用這些變數名，從這裡可以換其他顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 40, 40)
GREEN = (40, 180, 40)
BLUE = (40, 120, 220)
YELLOW = (240, 200, 40)

# ----------------------------- HELPERS -----------------------------------

def load_font(size):
    return pygame.font.Font(FONT_NAME, size)

# ----------------------------- SPRITES -----------------------------------
# Bullet：子彈，往怪物方向直線飛行(可能的BUG：怪物跑太快，子彈跟不上)
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, target, dmg, speed=8):
        super().__init__()
        self.image = pygame.Surface((6, 6))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(center=pos)
        self.dmg = dmg
        dx, dy = target[0] - pos[0], target[1] - pos[1]
        dist = math.hypot(dx, dy) or 1
        self.vx = speed * dx / dist
        self.vy = speed * dy / dist

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if (self.rect.right < 0 or self.rect.left > SCREEN_W or
                self.rect.bottom < 0 or self.rect.top > SCREEN_H):
            self.kill()

# Tower：射子彈的東西，射程 / 射擊冷卻
#  ├─ PeaShooter
#  └─ RapidFox
class Tower(pygame.sprite.Sprite):
    NAME = "Tower"
    COLOR = GREEN
    RANGE = 140
    COOLDOWN = 60
    DMG = 10

    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((34, 34), pygame.SRCALPHA)
        self.image.fill(self.COLOR)
        self.rect = self.image.get_rect(center=pos)
        self._cool = 0

    def update(self, monsters, bullets):
        if self._cool:
            self._cool -= 1
            return
        for m in monsters:
            if self._in_range(m):
                self.shoot(m, bullets)
                self._cool = self.COOLDOWN
                break

    def _in_range(self, m):
        dx = m.rect.centerx - self.rect.centerx
        dy = m.rect.centery - self.rect.centery
        return dx*dx + dy*dy <= self.RANGE*self.RANGE

    def shoot(self, m, bullets):
        bullets.add(Bullet(self.rect.center, m.rect.center, self.DMG))

class PeaShooter(Tower):
    NAME = "PeaShooter"
    COLOR = BLUE
    RANGE = 160
    COOLDOWN = 50
    DMG = 14

class RapidFox(Tower):
    NAME = "RapidFox"
    COLOR = RED
    RANGE = 120
    COOLDOWN = 15
    DMG = 6

# Monster：敵人基類
#  ├─ RunningRat（快血薄）
#  └─ HeavyToad（慢血厚）
class Monster(pygame.sprite.Sprite):
    COLOR = RED
    HP = 30
    SPEED = 1

    def __init__(self, path):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(self.COLOR)
        self.rect = self.image.get_rect(midleft=path[0])
        self.path = deque(path[1:])
        self.hp = self.HP

    def update(self):
        if not self.path:
            self.reached_goal = True
            self.kill()
            return
        target = self.path[0]
        dx, dy = target[0]-self.rect.centerx, target[1]-self.rect.centery
        dist = math.hypot(dx, dy)
        if dist < self.SPEED:
            self.rect.center = target
            self.path.popleft()
        else:
            self.rect.centerx += self.SPEED*dx/dist
            self.rect.centery += self.SPEED*dy/dist

    def hit(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.dead = True
            self.kill()

class RunningRat(Monster):
    COLOR = (120, 120, 255)
    HP = 20
    SPEED = 1.6

class HeavyToad(Monster):
    COLOR = (100, 200, 100)
    HP = 60
    SPEED = 0.8

MONSTER_CLASSES = {c.__name__: c for c in (RunningRat, HeavyToad)}
TOWER_CLASSES = {c.__name__: c for c in (PeaShooter, RapidFox)}

# ----------------------------- GAME --------------------------------------

##遊戲的主邏輯，包含了上面寫的怪物、子彈、塔、wave的邏輯
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Animal Defense")
        self.clock = pygame.time.Clock()
        self.font = load_font(20)

        self.towers = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        self.money = STARTING_MONEY
        self.lives = STARTING_LIVES
        self.wave_idx = -1
        self.spawn_delay = 0
        self.queue = deque()

        self.selected = "PeaShooter"
        self.path = [(0, SCREEN_H//2), (SCREEN_W, SCREEN_H//2)]
        self.next_wave()

    # ---------------- wave controls ----------------
    #next_wave() 讀取 WAVES，逐隻 spawn
    def next_wave(self):
        self.wave_idx += 1
        if self.wave_idx >= len(WAVES):
            return
        delay, pack = WAVES[self.wave_idx]
        self.spawn_delay = delay
        self.queue.clear()
        for name, cnt in pack:
            self.queue.extend([name]*cnt)

    def spawn_monster(self):
        cls = MONSTER_CLASSES[self.queue.popleft()]
        self.monsters.add(cls(self.path))

    # ---------------- tower place ------------------
    #place_tower() 讀取 TOWER_CLASSES，檢查錢夠不夠
    #self.selected的變更在 handle_events() 裡面(往下找一下)
    def place_tower(self, pos):
        cost = TOWER_COST[self.selected]
        if self.money < cost:
            return
        self.towers.add(TOWER_CLASSES[self.selected](pos))
        self.money -= cost

    # ---------------- main loop --------------------
    #這裡邏輯應該是對的！！！！少動這裡比較好！！
    #1. 處理輸入
    # 2. 依 spawn_delay 生成怪物
    # 3. 更新所有 sprite
    # 4. 檢查 碰撞（子彈↔怪物）
    # 5. 判斷勝敗 / 畫面渲染
    def run(self):
        tick = 0
        running=True
        while running:
            self.clock.tick(FPS)
            running=self.handle_events()

            # spawn logic
            if self.wave_idx < len(WAVES):
                tick += 1
                if tick >= self.spawn_delay:
                    tick = 0
                    if self.queue:
                        self.spawn_monster()
                    elif not self.monsters:
                        self.next_wave()

            # update sprites
            self.towers.update(self.monsters, self.bullets)
            self.monsters.update()
            self.bullets.update()

            # collisions
            hits = pygame.sprite.groupcollide(self.monsters, self.bullets, False, True)
            for monster, blts in hits.items():
                for b in blts:
                    monster.hit(b.dmg)
                if getattr(monster, "dead", False):
                    self.money += 10

            # goal check
            for m in list(self.monsters):
                if getattr(m, "reached_goal", False):
                    self.lives -= 1
                    m.kill()
            if self.lives <= 0:
                self.game_over(False)
                return
            if self.wave_idx >= len(WAVES) and not self.monsters and not self.bullets:
                self.game_over(True)
                return

            self.render()

    # ---------------- render -----------------------
    def render(self):
        self.screen.fill(WHITE)
        pygame.draw.line(self.screen, (180,180,180), self.path[0], self.path[-1],4)
        self.towers.draw(self.screen)
        self.monsters.draw(self.screen)
        self.bullets.draw(self.screen)

        hud1=self.font.render(f"Wave {min(self.wave_idx+1,len(WAVES))}/{len(WAVES)}   $ {self.money}   Lives: {self.lives}",True,BLACK)
        self.screen.blit(hud1,(10,10))
        sel=self.font.render(f"Selected: {self.selected} (${TOWER_COST[self.selected]})",True,BLACK)
        self.screen.blit(sel,(10,34))
        guide=self.font.render("[1] PeaShooter($50)  [2] RapidFox($80)",True,BLACK)
        self.screen.blit(guide,(10,58))
        pygame.display.flip()

    # ---------------- events -----------------------
    ##處理事件，包含了鍵盤、滑鼠、關閉視窗等
    ##切換塔的類型(按數字鍵1、2)，按esc是退出遊戲
    ##滑鼠點擊左鍵放塔，放塔的時候會檢查錢夠不夠
    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return False
                if e.key == pygame.K_1:
                    self.selected = "PeaShooter"
                if e.key == pygame.K_2:
                    self.selected = "RapidFox"
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                self.place_tower(pygame.mouse.get_pos())
        return True

    # ---------------- end --------------------------
    def game_over(self, win):
        txt = "YOU WIN!" if win else "GAME OVER"
        surf = load_font(60).render(txt, True, BLACK)
        self.screen.blit(surf, surf.get_rect(center=(SCREEN_W//2, SCREEN_H//2)))
        pygame.display.flip()
        pygame.time.wait(3000)

if __name__ == "__main__":
    Game().run()
    pygame.quit()
