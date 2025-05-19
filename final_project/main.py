import pygame, sys
from pygame.locals import *
from constants import *
from utils.font_loader import get_font
from entities.player import Player
from entities.building import Building
from ui.hud import draw_hud
from ui.prompt import draw_prompt, draw_end
from endings import check_game_over
from levels import LEVELS      # ← 這一行就是「main import 也要改」！


##====參數====##
MAX_INTERACTIONS=10
PLAYER_SPEED=3
pygame.mixer.init()
CAT_SOUND = pygame.mixer.Sound(CAT_SOUND_PATH)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Campus RPG MVP")
    clock = pygame.time.Clock()

    # 載入字型
    font_big   = get_font(32)
    font_small = get_font(24)

    # buildings = [
    #     Building(100, 100, "restaurant"),
    #     Building(WIDTH-100-BUILDING_SIZE[0], HEIGHT-100-BUILDING_SIZE[1], "classroom"),
    # ]
    # 建立角色
    player = Player(WIDTH//2, HEIGHT//2)

    # 用目前關卡的函式產生建築清單
    current_level = 0
    buildings = LEVELS[current_level](WIDTH, HEIGHT)
    
    interactions = 0
    game_over    = False
    reason       = ""

    # 主迴圈
    while True:
        # ——— 1. 事件處理 ———
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

            # 互動：按 Y 或 N
            if not game_over and event.type == KEYDOWN:
                # 先找出是否正靠近某棟建築
                near = next((b for b in buildings if player.rect.colliderect(b.detect_rect)), None)
                if near:
                    if event.key == K_y:
                        interactions += 1
                        result=near.interact(player)         # 更新 player 屬性interactions += 1

                        game_over,  ending = check_game_over(player, interactions)
                        if result == "meow":
                            CAT_SOUND.play()                    # 播放貓叫
                            # player 數值完全不變，interactions 仍會 +1
                        # else:
                        #     game_over, ending = check_game_over(player, interactions)
                        # # 檢查結束條件
                        # if player.fullness <= 0:
                        #     game_over = True; reason = "飢餓"
                        # elif player.sleepiness <= -10:
                        #     game_over = True; reason = "疲倦"
                        # elif interactions >= MAX_INTERACTIONS:
                        #     game_over = True; reason = "完成"
                    elif event.key == K_n:
                        pass  # 放棄互動

        # 若遊戲結束，跳出主迴圈繪製結束畫面
        if game_over:
            break

        # ——— 2. 移動邏輯 ———
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[K_LEFT]  or keys[K_a]: dx = -PLAYER_SPEED
        if keys[K_RIGHT] or keys[K_d]: dx =  PLAYER_SPEED
        if keys[K_UP]    or keys[K_w]: dy = -PLAYER_SPEED
        if keys[K_DOWN]  or keys[K_s]: dy =  PLAYER_SPEED

        player.move(dx, dy, screen.get_rect(), buildings)

        # ——— 3. 畫面繪製 ———
        screen.fill(BG_COLOR)

        # 繪製所有建築
        for b in buildings:
            b.draw(screen)

        # 繪製玩家
        player.draw(screen)

        # 繪製左上 HUD
        draw_hud(screen, font_small, player, interactions)

        # 如果靠近建築，顯示互動提示
        near = next((b for b in buildings if player.rect.colliderect(b.detect_rect)), None)
        if near:
            if   near.kind == "restaurant":
                txt = "進入餐廳？ (Y/N)"
            elif near.kind == "classroom":
                txt = "進入教室？ (Y/N)"
            elif near.kind == "cat":            # ★ 新增
                txt = "要摸摸可愛的貓咪嗎？ (Y/N)"
            else:
                txt = "要互動嗎？ (Y/N)"
            draw_prompt(screen, font_big, txt)

        pygame.display.flip()
        clock.tick(FPS)

    
# ---------- 跳出主迴圈後 ----------
    msg1 = f"結局：{ending['key']}"
    msg2 = f"最終 社交:{player.social}  成績:{player.grade}"

    # 1. 先讀圖片、拿到高寬
    img = None
    i_w = i_h = 0
    if ending["image"]:
        img = pygame.image.load(ending["image"]).convert_alpha()
        
        # 🔹 1A. 等比例縮圖（上限：螢幕 75% × 75%）
        max_w = int(WIDTH  * 0.75)
        max_h = int(HEIGHT * 0.75)
        w, h  = img.get_size()
        scale = min(max_w / w, max_h / h, 1)   # 不放大 → <=1
        if scale < 1:
            new_size = (int(w * scale), int(h * scale))
            img = pygame.transform.smoothscale(img, new_size)
            w, h = new_size
        i_w, i_h = w, h

    # 2. 估計兩行文字高度
    t1 = font_big.render(msg1, True, (0,0,0))
    t2 = font_big.render(msg2, True, (0,0,0))
    text_block_h = t1.get_height() + 10 + t2.get_height()

    # 3. 整塊高度（文字 + 空隙 20px + 圖片）
    total_h = text_block_h + 20 + i_h

    SAFE_MARGIN = 5
    spare = (HEIGHT - SAFE_MARGIN) - total_h
    shift_up = max(0, -spare)

    # 🔹 2A. 文字起始 y 往上調到 5% 高度
    y1 = int(HEIGHT * 0.05) - shift_up

    # ---------- draw ----------
    screen.fill((200, 200, 200))

    # 1) 兩行文字
    screen.blit(t1, ((WIDTH - t1.get_width()) // 2, y1))
    y2 = y1 + t1.get_height() + 10
    screen.blit(t2, ((WIDTH - t2.get_width()) // 2, y2))

    # 2) 圖片
    if img:
        img_rect = img.get_rect()
        img_rect.midtop = (WIDTH // 2, y2 + t2.get_height() + 20)
        screen.blit(img, img_rect)

    pygame.display.flip()

    # 等玩家按鍵或關閉
    while True:
        e = pygame.event.wait()
        if e.type in (QUIT, KEYDOWN):
            pygame.quit()
            sys.exit()

    
if __name__ == "__main__":
    main()