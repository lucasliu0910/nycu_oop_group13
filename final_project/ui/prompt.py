# ui/prompt.py
import pygame
from constants import WIDTH, HEIGHT

def draw_prompt(screen, font, text):
    surf = font.render(text, True, (255,255,255))
    bg = pygame.Surface((surf.get_width()+10, surf.get_height()+10))
    bg.set_alpha(150)
    bg.fill((0,0,0))
    x = (WIDTH - surf.get_width())//2
    y = HEIGHT - surf.get_height() - 50
    screen.blit(bg, (x-5, y-5))
    screen.blit(surf, (x, y))

def draw_end(screen, font, msg1, msg2, bg=(200, 200, 200)):
    """
    清空畫面 → 顯示兩行文字 → 回傳「第二行文字底下」的 y 座標
    方便呼叫端決定圖片要貼在哪
    """
    screen.fill(bg)                             # 1. 覆蓋原先遊戲畫面
    surf1 = font.render(msg1, True, (255, 0, 0))
    surf2 = font.render(msg2, True, (0,   0, 0))

    # 文字置中
    x1 = (WIDTH - surf1.get_width()) // 2
    y1 = HEIGHT // 4                         # 上方 1/4 畫面
    x2 = (WIDTH - surf2.get_width()) // 2
    y2 = y1 + surf1.get_height() + 10        # 第二行接續

    screen.blit(surf1, (x1, y1))
    screen.blit(surf2, (x2, y2))
    pygame.display.flip()

    return y2 + surf2.get_height() + 20      # “底線”：給圖片用
