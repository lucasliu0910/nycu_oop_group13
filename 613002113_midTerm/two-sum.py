class Solution:
    def twoSum(self, nums: List[int], target: int):
        answer = []
        for i in range(len(nums)):
            for j in range(len(nums)):
                if i==j:
                    continue
                elif nums[i]+nums[j]==target:
                    answer.append(i)
                    answer.append(j)
                    return answer