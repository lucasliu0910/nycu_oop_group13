class Solution:
    def numEnclaves(self, grid: List[List[int]]) -> int:
        m,n = len(grid),len(grid[0])

        def dfs(row: int, col: int):
            if (row < 0) or (row >= m) or (col < 0) or (col >= n):
                return None
            if grid[row][col] == 0:
                return None
            grid[row][col] = 0
            dfs(row+1,col) #往下走
            dfs(row-1,col) #往上走
            dfs(row,col+1) #往右走
            dfs(row,col-1) #往左走
        
        #從邊界上的１開始走起
        for i in range(m):
            if grid[i][0] == 1:
                dfs(i,0)
            if grid[i][n-1] == 1:
                dfs(i,n-1)
        for j in range(1,n-1):
            if grid[0][j] == 1:
                dfs(0,j)
            if grid[m-1][j] == 1:
                dfs(m-1,j)
        
        #數剩下１的數量
        count = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    count += 1
        
        return count