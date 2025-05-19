class Solution:
    def sortPeople(self, names: List[str], heights: List[int]) -> List[str]:
        # 步驟 1: 建立名字和身高的配對
        zip_list = zip(names,heights)
        
        # 步驟 2: 根據身高降序排序
        sorted_list = sorted(zip_list, key=lambda x: x[1], reverse=True)
        
        # 步驟 3: 提取排序後的名字
        sorted_names = [i[0] for i in sorted_list]
        return sorted_names