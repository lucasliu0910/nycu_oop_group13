class Solution:
    def minimumTime(self, time: List[int], totalTrips: int) -> int:
        
        # 創建一個檢查函數，計算在給定時間內能完成的行程總數
        def can_complete(given_time):
            # 計算在 given_time 內所有巴士能完成的行程總數
            # 如果總數 >= totalTrips，返回 True，否則返回 False
            total = 0
            for i in range(len(time)):
                total += given_time // time[i]
            if total >= totalTrips:
                return True
            else:
                return False
        
        left = 1 # 設定二分查找的上下界
        right = min(time) * totalTrips # 設定適當的上界

        # 進行二分查找
        while left < right:
            mid = (left+right) // 2 # 計算中間值，檢查是否滿足條件，並調整上下界
            if can_complete(mid):
                right = mid
            else:
                left = mid + 1

        return left