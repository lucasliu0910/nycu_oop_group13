from typing import List
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
        """
        Return the minimum possible score of a path between cities 1 and n.

        Parameters:
            n (int): The number of cities.
            roads (List[List[int]]): A list of roads represented as triples of cities and distances.

        Returns:
            int: The minimum possible score of a path between cities 1 and n.

        Examples:
            >>> solution = Solution()

            # Example 1:
            >>> n1 = 4
            >>> roads1 = [[1,2,9],[2,3,6],[2,4,5],[1,4,7]]
            >>> solution.minScore(n1, roads1)
            5

            # Example 2:
            >>> n2 = 4
            >>> roads2 = [[1,2,2],[1,3,4],[3,4,7]]
            >>> solution.minScore(n2, roads2)
            2
        """
        self.build_graph(n,roads)
        min_dist = math.inf
        visited = set()
        return self.dfs(1,visited,min_dist)
        
if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)