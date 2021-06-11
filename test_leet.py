from collections import Counter
class Solution(object):
    def subarraySum(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        sum=0
        list1=[]
        for i,val in enumerate(nums):
            while sum<k:
                sum+=val
                list1.append(i)
                if sum==k:
                    break
                elif sum>k:
                    pass

    def lengthOfLongestSubstring(self, s):
        """
        :type s: str
        :rtype: int
        """

        tempS = ''
        maxL = 0

        if len(s) == 1 or s==" ":
            return 1
        for i in range(len(s) - 1):
            tempS = s[i]
            for j in range(i + 1, len(s)):
                my_dict = {}
                tempS += s[j]
                my_dict=Counter(tempS)
                #print('counter',Counter(tempS))
                if all(i <= 1 for i in my_dict.values()) and len(tempS) > maxL:
                        #print('entered')
                        maxL = len(tempS)
        return maxL

    def longestPalindrome(self, s):
        """
        :type s: str
        :rtype: str
        """

        tempS = ''
        rever_string = ''
        r = ''
        maxL = 0

        if len(s) == 1:
            return s
        for i in range(len(s) - 1):
            tempS = s[i]
            r = s[i]
            for j in range(i + 1, len(s)):
                tempS += s[j]

                if tempS == tempS[::-1]:

                    if len(tempS) > maxL:
                        maxL = len(tempS)
                        rever_string = tempS
        if not len(rever_string):
            return r
        else:
            return rever_string


if __name__=="__main__":
    s=Solution()
    print(s.lengthOfLongestSubstring(s="cwpawhyxfqlpzjldyytvjfwepijociweengauexbwkqwtcbuaurlaospybfajbgpqmpktplpzentiopilgvlw"))
    #print('Sting is:',s.longestPalindrome("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"))