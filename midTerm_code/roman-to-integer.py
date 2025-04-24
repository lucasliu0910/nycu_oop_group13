class Solution:
    def romanToInt(self, s: str) -> int:
        m_2 = {'IV': 4, 'IX':9, 'XL':40, 'XC':90, 'CD':400, 'CM':900}
        m_1 = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        k = len(s)
        #print(k)
        num = 0
        while k != 0:
            if len(s) >= 2:
                try:
                    num += m_2[s[0:2]]
                    k -= 2
                    s = s[2:]
                except:
                    num += m_1[s[0]]
                    k -= 1
                    s = s[1:]
            else:
                num += m_1[s[0]]
                k -= 1
                s = s[1:]
        #print(num)
        return num