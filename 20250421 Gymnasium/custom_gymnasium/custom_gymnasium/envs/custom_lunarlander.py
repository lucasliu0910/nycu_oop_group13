import numpy as np
import gymnasium as gym
from typing import TYPE_CHECKING, Optional
from custom_gymnasium.utils.base_lander import BASE_LANDER

class CustomLunarLander_v1(BASE_LANDER):
    def __init__(
        self,
        render_mode: Optional[str] = None,
        continuous: bool = False,
        gravity: float = -10.0,
        enable_wind: bool = False,
        wind_power: float = 15.0,
        turbulence_power: float = 1.5,
        fuel: float = 100,):
        '''
        Task:
        - Implement a custom lunar lander environment where the lander has a fuel tank of size `fuel`.
        '''
        # =====================type your code here=====================
        super().__init__(
            render_mode=render_mode,
            continuous=continuous,
            gravity=gravity,
            enable_wind=enable_wind,
            wind_power=wind_power,
            turbulence_power=turbulence_power,
        )
        self.max_fuel = fuel
        self.fuel = fuel
        # =============================================================
    
    def reset(
        self,
        *,
        seed: Optional[int] = None,
        options: Optional[dict] = None,):
        '''
        Task:
        - Reset the fuel tank to its original size.
        '''
        # =====================type your code here=====================
        state, info = super().reset(seed=seed, options=options)
        self.fuel = self.max_fuel
        return state, info
        # =============================================================
        
    def step(self, action):
        '''
        Task:
        - The lander can only move if it has fuel left. If the fuel is exhausted, the lander can no longer move.
        
        Hint:
        - If the lander moves, the fuel tank should be decremented by 1.
        - If the lander doesn't move, the fuel tank should remain the same.
        '''
        # =====================type your code here=====================
        # 檢查是否還有燃料
        if self.fuel <= 0:
            # 如果沒有燃料，則動作設為不動作
            if self.continuous:
                action = np.array([0.0, 0.0])
            else:
                action = 0  # 不動作
        else:
            # 檢查是否執行了動作（不是不動作）
            if (self.continuous and (action[0] != 0.0 or action[1] != 0.0)) or (not self.continuous and action != 0):
                # 如果執行了動作，燃料減少
                self.fuel -= 1
        
        # 調用父類的 step 方法
        state, reward, terminated, truncated, info = super().step(action)
        
        # 在 info 中加入燃料信息
        info['fuel'] = self.fuel
        
        return state, reward, terminated, truncated, info
        # =============================================================