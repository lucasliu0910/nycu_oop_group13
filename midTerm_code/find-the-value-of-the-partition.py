class Solution:
    def findValueOfPartition(self, nums: List[int]) -> int:
        nums.sort()
        values = []
        for i in range(len(nums)-1):
            values.append(nums[i+1]-nums[i])
        return min(values)