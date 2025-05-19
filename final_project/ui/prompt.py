# ui/prompt.py
import pygame
from constants import WIDTH, HEIGHT

def draw_choices(screen, font, choices, topleft=None):
    """
    在畫面上顯示一組選項列表 choices = [(label, text), ...]。
    topleft: (x,y) 決定起始位置，若 None，則預設放右上。
    """
    padding = 8
    # 計算起始座標
    if topleft is None:
        x0 = WIDTH - padding
        y0 = padding
    else:
        x0, y0 = topleft

    for label, txt in choices:
        line_surf = font.render(f"{label}. {txt}", True, (255,255,255))
        bg = pygame.Surface((line_surf.get_width()+padding, line_surf.get_height()+padding))
        bg.set_alpha(150)
        bg.fill((0,0,0))
        # 貼背景和文字
        screen.blit(bg, (x0 - bg.get_width(), y0))
        screen.blit(line_surf, (x0 - line_surf.get_width(), y0 + padding//2))
        y0 += line_surf.get_height() + padding


def draw_prompt(screen, font, text, feedback=False):
    """
    畫一行提示文字，預設置底部中央，可透過 feedback 參數將位置提升。
    feedback=True 時文字顯示在畫面上方 20%。
    """
    surf = font.render(text, True, (255,255,255))
    bg = pygame.Surface((surf.get_width()+10, surf.get_height()+10))
    bg.set_alpha(150)
    bg.fill((0,0,0))
    x = (WIDTH - surf.get_width()) // 2
    if feedback:
        y = int(HEIGHT * 0.2)
    else:
        y = HEIGHT - surf.get_height() - 50
    screen.blit(bg, (x-5, y-5))
    screen.blit(surf, (x, y))
    

def draw_end(screen, font, msg1, msg2, bg=(200,200,200)):
    screen.fill(bg)
    # 先處理第一段 msg1
    lines1 = msg1.split("\n")
    y = HEIGHT // 4
    for line in lines1:
        surf = font.render(line, True, (255,0,0))
        x = (WIDTH - surf.get_width()) // 2
        screen.blit(surf, (x, y))
        y += surf.get_height() + 5

    # 再處理第二段 msg2
    lines2 = msg2.split("\n")
    y += 10  # 兩段中點補點縫隙
    for line in lines2:
        surf = font.render(line, True, (0,0,0))
        x = (WIDTH - surf.get_width()) // 2
        screen.blit(surf, (x, y))
        y += surf.get_height() + 5

    pygame.display.flip()
    return y  