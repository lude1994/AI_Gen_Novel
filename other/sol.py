from collections import Counter

class Solution:
    def is_contained(self,counter1, counter2):
        return not (counter2 - counter1)

    def minWindow(self, s: str, t: str) -> str:
        c = Counter(t)
        c_t = Counter()
        c_str = ""
        al = []
        l = 0
        r = 0
        while r <= len(s) and l <= (len(s)-len(t)+1):
            if self.is_contained(c_t,c):
                al.append(c_str)
                s_tt =s[l:l+1]
                l += 1
                c_str = c_str[1:]
                c_t[s_tt] -= 1
                while l < r :
                    s_tt =s[l:l+1]
                    if c[s_tt] > 0 :
                        break
                    c_t[s_tt]-=1
                    c_str = c_str[1:]
                    l += 1
            else:
                if r == len(s):
                    break
                cur = s[r:r+1]
                if c[cur] == 0 and len(c_str) == 0 :
                    l += 1
                    r += 1
                    continue
                c_str += cur
                c_t[cur] += 1
                r += 1
        if self.is_contained(c_t,c):
            al.append(c_str)
        al.sort(key=lambda x:len(x))
        if len(al) > 0:
            return al[0]
        return ""

Solution().minWindow("ADOBECODEBANC", "ABC")