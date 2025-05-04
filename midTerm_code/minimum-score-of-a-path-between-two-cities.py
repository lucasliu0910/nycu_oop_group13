import math
class Solution:
    def __init__(self):
        self.graph = {}
    def build_graph(self,n,roads):
        self.graph = {i: [] for i in range(1,n+1)}
        for a,b,distance in roads:
            self.graph[a].append([b,distance])
            self.graph[b].append([a,distance])
    def dfs(self,current,visited,min_dist):
        visited.add(current)
        for neighbor,distance in self.graph[current]:
            min_dist = min(min_dist,distance)
            if neighbor not in visited:
                min_dist = self.dfs(neighbor,visited,min_dist)
        return min_dist
    def minScore(self, n: int, roads: List[List[int]]) -> int:
        self.build_graph(n,roads)
        min_dist = math.inf
        visited = set()
        return self.dfs(1,visited,min_dist)