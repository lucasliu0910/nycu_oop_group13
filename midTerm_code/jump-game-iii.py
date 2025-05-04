class Solution:
    def canReach(self, arr: List[int], start: int) -> bool:
        n = len(arr)
        visited = [False] * n
        def dfs(index):
            if index < 0 or index >= n or visited[index] == True:
                return False
            if arr[index] == 0:
                return True
            visited[index] = True
            jump_right = dfs(index+arr[index])
            jump_left = dfs(index-arr[index])
            return jump_right or jump_left
        return dfs(start)