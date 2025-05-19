# endings.py
MAX_INTERACTIONS = 10

EARLY_FAILS = [
    {"key": "餓暈校園", "condition": lambda p, i: p.fullness <= 0,  "image": None},
    {"key": "累到虛脫", "condition": lambda p, i: p.sleepiness <= -10, "image": None},
]

FINAL_ENDINGS = [
    {"key": "教授這裡風很大", 
     "condition": lambda p, i: p.grade < 3,
     "image": "final_project/pictures/1662286848503.jpg"},
    # {"key": "平凡的一頁", "condition": lambda p, i: True, "image": None},   # default
]

def check_game_over(player, interactions):
    # 1) 即時失敗
    for e in EARLY_FAILS:
        if e["condition"](player, interactions):
            return True, e

    # 2) 未達互動上限 → 遊戲繼續
    if interactions < MAX_INTERACTIONS:
        return False, None

    # 3) 期末結局
    for e in FINAL_ENDINGS:
        if e["condition"](player, interactions):
            return True, e

    return False, None
