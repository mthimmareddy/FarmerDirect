"""
Leetcode problems and Solution.
Created on:29 May 2020
Created By:Manjula
"""
import numpy
from collections import Counter


class Solution(object):
    def __init__(self):
        my_dict = {}
        my_list = []

    def lengthOfLongestSubstring(self, s):
        """
        :type s: str
        :rtype: int
        """

        tempS = ''
        maxL = 0

        if len(s) == 1:
            return s
        for i in range(len(s) - 1):
            tempS = s[i]

            for j in range(i + 1, len(s)):
                tempS += s[j]
                print('counter',Counter(tempS))
                for k,v in Counter(tempS).items():
                    if v<=1 and len(tempS) > maxL:
                        maxL = len(tempS)
        return maxL

    def longestPalindrome(self, s):
        """
       Given a string s, find the longest palindromic substring in s. You may assume that the maximum length of s is 1000.

Example 1:

Input: "babad"
Output: "bab"
Note: "aba" is also a valid answer.
Example 2:

Input: "cbbd"
Output: "bb"
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

    def shuffle(self, nums, n):
        """
        :type nums: List[int]
        :type n: int
        :rtype: List[int]
        """
        s=[]
        n1=nums[0:n]
        n2=nums[n:(2*n)]
        print(n1,n2)
        for i in range(0,n):
            s.append(n1[i])
            s.append(n2[i])
        return s


    def largestUniqueNumber(self, nums):
        """
       Given an array of integers A, return the largest integer that only occurs once.

If no integer occurs once, return -1.

 

Example 1:

Input: [5,7,3,9,4,9,8,3,1]
Output: 8
Explanation: 
The maximum integer in the array is 9 but it is repeated. The number 8 occurs only once, so it's the answer.
Example 2:

Input: [9,9,8,8]
Output: -1
Explanation: 
There is no number that occurs only once.
 
        """
        s = {}
        maxEle=0
        for ele in nums:
            if ele not in s:
                s[ele] = 1
            else:
                s[ele] += 1
        print(s)
        for k, v in s.items():
            if v == 1 and k>maxEle:
                maxEle=k
                #print('max',maxEle)
        return maxEle

    def flipAndInvertImage(self, A):
        """
        Given a binary matrix A, we want to flip the image horizontally, then invert it, and return the resulting image.

To flip an image horizontally means that each row of the image is reversed.  For example, flipping [1, 1, 0] horizontally results in [0, 1, 1].

To invert an image means that each 0 is replaced by 1, and each 1 is replaced by 0. For example, inverting [0, 1, 1] results in [1, 0, 0].

Example 1:

Input: [[1,1,0],[1,0,1],[0,0,0]]
Output: [[1,0,0],[0,1,0],[1,1,1]]
Explanation: First reverse each row: [[0,1,1],[1,0,1],[0,0,0]].
Then, invert the image: [[1,0,0],[0,1,0],[1,1,1]]
Example 2:

Input: [[1,1,0,0],[1,0,0,1],[0,1,1,1],[1,0,1,0]]
Output: [[1,1,0,0],[0,1,1,0],[0,0,0,1],[1,0,1,0]]
Explanation: First reverse each row: [[0,0,1,1],[1,0,0,1],[1,1,1,0],[0,1,0,1]].
Then invert the image: [[1,1,0,0],[0,1,1,0],[0,0,0,1],[1,0,1,0]]
        """
        print("A",A)

        for i in range(0,len(A)):
            A[i] = A[i][::-1]
            j=0
            print('A[i]',A[i])
            for ele in A[i]:

                if ele==0:
                    A[i][j]=1
                else:
                    A[i][j]=0
                j=j+1
        print('A:',A)
        return A
            #for j in range(0,len(A[0])):


    def moveZeroes(self, nums):
        """
       Given an array nums, write a function to move all 0's to the end of it while maintaining the relative order of the non-zero elements.

Example:

Input: [0,1,0,3,12]
Output: [1,3,12,0,0]
        """
        nonzeroindex=0
        for ele in nums:
            if ele!=0:
                nums[nonzeroindex]=ele
                nonzeroindex+=1
        for i in range(nonzeroindex,len(nums)):
            nums[i]=0
        return nums


    def searchRange(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        mylist=[]
        for index,value in enumerate(nums):
            if target==value:
                mylist.append(index)
            else:
                continue
        print(mylist)



    def rob(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        prevMax = 0
        currMax = 0
        for x in nums:
            temp = currMax
            currMax = max(prevMax + x, currMax)
            prevMax = temp

        return currMax

    def missingNumber(self, nums):
        """
       Given an array containing n distinct numbers taken from 0, 1, 2, ..., n, find the one that is missing from the array.

        Example 1:
        
        Input: [3,0,1]
        Output: 2
        Example 2:
        
        Input: [9,6,4,2,3,5,7,0,1]
        Output: 8
        """
        nums=sorted(nums)
        print(nums)


        if nums[0]!=0:
            return 0
        elif len(nums)!=nums[-1]:
            return len(nums)

        for i in range(1,len(nums)):
            expected=nums[i-1]+1
            if nums[i]!=expected:
                return expected

    def majorityElement(self, nums,target):
        """
        Given an array of size n, find the majority element. The majority element is the element that appears more than ⌊ n/2 ⌋ times.

You may assume that the array is non-empty and the majority element always exist in the array.

Example 1:

Input: [3,2,3]
Output: 3
Example 2:

Input: [2,2,1,1,1,2,2]
Output: 2
        """

        s = {}
        for ele in nums:
            if ele not in s:
                s[ele] = 1
            else:
                s[ele] += 1

        print(s)
        for k, v in s.items():
            if k == target and v > int(len(nums) / 2):
                return True
        return False

    def findTheDifference(self, s, t):
        """
       Given two strings s and t which consist of only lowercase letters.

        String t is generated by random shuffling string s and then add one more letter at a random position.
        
        Find the letter that was added in t.
        
        Example:
        
        Input:
        s = "abcd"
        t = "abcde"
        
        Output:
        e
        
        Explanation:
        'e' is the letter that was added.
        """
        my_string=s+t
        s = {}
        for ele in my_string:
            if ele not in s:
                s[ele] = 1
            else:
                s[ele] += 1
        for k, v in s.items():
            if v % 2 != 0:
                return k


    def singleNumber(self, nums):
        """
       Given a non-empty array of integers, every element appears twice except for one. Find that single one.

        Note:
        
        Your algorithm should have a linear runtime complexity. Could you implement it without using extra memory?
        
        Example 1:
        
        Input: [2,2,1]
        Output: 1
        Example 2:
        
        Input: [4,1,2,1,2]
        Output: 4
        """
        s = {}
        for ele in nums:
            if ele not in s:
                s[ele] = 1
            else:
                s[ele] += 1
        for k, v in s.items():
            if v == 1:
                return k





    def combinationTarget(self,nums,target):
        #sum=0
        list1=[]

        for i in range(0,len(nums)-1):
            sum = 0
            my_list = []
            for j in range(i+1,len(nums)):
                #print(nums[i],nums[j])
                sum +=nums[i]+nums[j]
                print(sum)

                if sum>target:
                    continue
                else:
                    my_list.append(nums[i])
                    my_list.append(nums[j])
                    if sum==target:
                        list1.append(my_list)
                        break

        return list1

    def get_key(self, my_dict, val):
        for key, value in my_dict.items():
            if val == value:
                return True, key

        return False

    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        Given an array of integers, return indices of the two numbers such that they add up to a specific target.

        You may assume that each input would have exactly one solution, and you may not use the same element twice.

        Example:

        Given nums = [2, 7, 11, 15], target = 9,

        Because nums[0] + nums[1] = 2 + 7 = 9,
        return [0, 1].
        """
        my_dict = {}
        my_list = []
        for i in range(0, len(nums)):
            my_dict[i] = nums[i]

        for i in range(0, len(nums)):
            compliment = target - my_dict[i]
            num2 = self.get_key(my_dict=my_dict, val=compliment)
            if compliment in nums and num2 != i:
                return (num2, i)
        return None

    def twoSumLessThanK(self, A, K):
        """
        Given an array A of integers and integer K, return the maximum S such that there exists i < j 
        with A[i] + A[j] = S and S < K. If no i, j exist satisfying this equation, return -1.
        :type A: List[int]
        :type K: int
        :rtype: int
        """
        my_dict = {}
        my_list = []
        for i in range(0, len(A)):
            my_dict[i] = A[i]

        for target in range(K - 1, 0, -1):
            for i in range(0, len(A)):
                compliment = target - my_dict[i]
                print('compliment', my_dict[i], compliment, target)
                if compliment in A and compliment != my_dict[i]:
                    print('inside')
                    print('compliment', my_dict[i], compliment, target)
                    # condition,num2 = self.get_key(my_dict=my_dict, val=compliment)
                    # if condition :
                    return (target)

        return -1

    def lengthOfLongestSubstring(self, s):
        """
        Given a string, find the length of the longest substring without repeating characters.

        Example 1:

        Input: "abcabcbb"
        Output: 3 
        Explanation: The answer is "abc", with the length of 3. 
        Example 2:

        Input: "bbbbb"
        Output: 1
        Explanation: The answer is "b", with the length of 1.
        Example 3:

        Input: "pwwkew"
        Output: 3
        Explanation: The answer is "wke", with the length of 3. 
                     Note that the answer must be a substring, "pwke" is a subsequence and not a substring.
                :param s: 
                :return: 


        :type s: str
        :rtype: int
        """
        dicts = {}
        str1 = ""
        start_index = 0
        list1 = []
        i = 0
        while (i != len(s)):
            if s[i] not in dicts:
                dicts[s[i]] = 1
                str1 += s[i]
                list1.append(str1)
                i += 1
            else:
                start_index += 1
                i = start_index
                dicts = {}
                str1 = ""
        max = 0
        for ele in list1:
            if len(ele) > max:
                max = len(ele)
        return max

    def reverse(self, x):
        """
        :type x: int
        :rtype: int
        """
        reverse = 0
        if (x <= 0):
            return -1
        while (x > 0):
            print(reverse)
            remainder = x % 10
            # print(val)
            reverse = (reverse * 10) + remainder
            print(reverse)
            x = x // 10
        return reverse

    def isPalindrome(self, x):
        """
        :type x: int
        :rtype: bool
        """
        reverse = 0
        num = x
        if (x <= 0):
            return False
        while (x > 0):
            # print(reverse)
            remainder = x % 10
            # print(val)
            reverse = (reverse * 10) + remainder
            # print(reverse)
            x = x // 10
        if reverse == num:
            return True
        else:
            return False

    def maximumProduct(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        nums = sorted(nums)
        s = len(nums)
        product = max(nums[s - 1] * nums[1] * nums[0],
                      nums[s - 1] * nums[s - 2] * nums[s - 3])  # for negative numbers first hold true
        return product

    def maxProduct(self, nums):
        """
        Given an integer array nums, find the contiguous subarray within an array (containing at least one number) which has the largest product.

Example 1:

Input: [2,3,-2,4]
Output: 6
Explanation: [2,3] has the largest product 6.
Example 2:

Input: [-2,0,-1]
Output: 0
Explanation: The result cannot be 2, because [-2,-1] is not a subarray.
        :type nums: List[int]
        :rtype: int
        """
        maxpro = nums[0]
        for i in range(0, len(nums) - 1):
            if nums[i] * nums[i + 1] > maxpro:
                maxpro = nums[i] * nums[i + 1]
        return maxpro

    def threeSum(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        Given an array nums of n integers, are there elements a, b, c in nums such that a + b + c = 0? Find all unique triplets in the array which gives the sum of zero.

        Note:

        The solution set must not contain duplicate triplets.

        Example:

        Given array nums = [-1, 0, 1, 2, -1, -4],

        A solution set is:
        [
          [-1, 0, 1],
          [-1, -1, 2]
        ]
        """
        res = []
        found = set()
        for i, val1 in enumerate(nums):
            seen = set()
            for j, val2 in enumerate(nums[i + 1:]):
                complement = -val1 - val2
                if complement in seen:
                    min_val = min((val1, val2, complement))
                    max_val = max((val1, val2, complement))
                    if (min_val, max_val) not in found:
                        found.add((min_val, max_val))
                        res.append([val1, val2, complement])
                seen.add(val2)
        return res

    def checkRecord(self, s):
        """
        :type s: str
        :rtype: bool
        """
        i = 0
        j = 0
        check = None
        c = 0
        absent = 0
        # A=1,L=2
        while (j < len(s)):
            if (s[j] == 'A'):
                absent += 1
            j = j + 1

        while (i + 2 < len(s)):

            if (s[i] == 'L' and s[i + 1] == 'L' and s[i + 2] == 'L'):

                check = False
                break
            else:
                check = True
            i = i + 1

        if absent >= 2:
            check = False

        return check

    def searchRange(self, nums, target):
        """
       Given an array of integers nums sorted in ascending order, find the starting and ending position of a given target value.

Your algorithm's runtime complexity must be in the order of O(log n).

If the target is not found in the array, return [-1, -1].

Example 1:

Input: nums = [5,7,7,8,8,10], target = 8
Output: [3,4]
Example 2:

Input: nums = [5,7,7,8,8,10], target = 6
Output: [-1,-1]
        """
        mylist = []
        start_index = -1
        last_index = -1
        for i, val in enumerate(nums):
            if val == target and len(mylist) == 0:
                mylist.append(i)
                start_index = i
            elif val == target and len(mylist) != 0 and len(mylist) <= len(nums):
                mylist.append(i)
                last_index = i
        if start_index != -1:
            last_index = start_index

        return [start_index, last_index]

    def smallestCommonElement(self, mat):
        """
        Given a matrix mat where every row is sorted in increasing order, return the smallest common element in all rows.

If there is no common element, return -1.



Example 1:

Input: mat = [[1,2,3,4,5],[2,4,5,8,10],[3,5,7,9,11],[1,3,5,7,9]]
Output: 5

        """
        mylist = []
        dict1 = {}
        for i in range(0, len(mat)):
            for j in range(0, len(mat[0])):
                ele = mat[i][j]
                if ele not in dict1:
                    dict1[ele] = 1
                else:
                    dict1[ele] += 1
        for key, val in dict1.items():
            if dict1[key] == len(mat):
                mylist.append(key)
        mylist.sort()
        if len(mylist) != 0:
            return mylist[0]
        else:
            return -1

    def combinationSum(self, nums, target):
        """
                       Given a set of candidate numbers (candidates) (without duplicates) and a target number (target), find all unique combinations in candidates where the candidate numbers sums to target.

            The same repeated number may be chosen from candidates unlimited number of times.

            Note:

            All numbers (including target) will be positive integers.
            The solution set must not contain duplicate combinations.
            Example 1:

            Input: candidates = [2,3,6,7], target = 7,
            A solution set is:
            [
              [7],
              [2,2,3]
            ]
            Input: candidates = [2,3,5], target = 8,
            A solution set is:
            [
              [2,2,2,2],
              [2,3,3],
              [3,5]
            ]
        """
        mylist = []
        list1 = []
        ans = set()
        for item in nums:
            # ans = set()

            compliment = target - item
            if compliment in nums:
                t = tuple([item, compliment])
                ans.add(t)
                mylist.append([item, compliment])
                # list1.append(compliment)

            ans = set()
            val = target % item
            if val == 0:
                times = int(target / item)
                for i in range(times):
                    list1.append(item)
                ans.add(tuple(list1))
                print('ans', ans)
                # mylist.append(list1)

            if val != 0 and val in nums:
                times = int(target / item)
                for i in range(times):
                    list1.append(item)
                    ans.add(item)
                list1.append(val)
                ans.add(val)
                print('ans', ans)
            mylist.append(list1)
            print(ans)

        return mylist


class MinStack(object):
    def __init__(self,data):
        """
        initialize your data structure here.
        """
        self._mylist = data

    def __len(self):
        return len(self._mylist)

    def is_empty(self):
        return len(self._mylist) == 0

    def push(self, x):
        """
        :type x: int
        :rtype: None
        """
        try:
           self._mylist.append(x)
                # print("value inserted",self.mylist)
                # return self.mylist
        except Exception:
            raise AssertionError("Push operation failed")

    def pop(self):
        """
        :rtype: None
        """
        try:
            if not self.is_empty():
                x = self.mylist.pop()
                # self.mylist.pop(0) implements queue,FIFO
                #The method pop() can be used to remove and return the last value from the list or the given index value.
                # If the index is not given, then the last element is popped out and removed.
                print('Element removed is:{0}'.format(x))
            else:
                raise Exception('Popping from empty list')
                # print("value poped is",x)

        except Exception:
            raise AssertionError("Pop operation failed")

    def top(self):
        """
        :rtype: int
        """
        if len(self._mylist) != 0:
            return self._mylist[-1]
        else:
            raise AssertionError('Empty list')

    def getMin(self):
        """
        :rtype: int
        """
        return min(self._mylist)

    @property
    def mylist(self):
        return self._mylist

    '''
    Implementation using collections.deque
    Queue in Python can be implemented using deque class from the collections module. Deque is preferred over list in the cases where we need quicker append and pop operations from both the ends of container, as deque provides an O(1) time complexity for append and pop operations as compared to list which provides O(n) time complexity. 
    Instead of enqueue and deque, append() and popleft() functions are used
    '''
    from collections import deque

    # Initializing a queue
    q = deque()

    # Adding elements to a queue
    q.append('a')
    q.append('b')
    q.append('c')





    # Uncommenting q.popleft()
    # will raise an IndexError
    # as queue is now empty

class Node(object):

    def __init__(self, data):

        self.left = None
        self.right = None
        self.data = data

    def insert(self, data):
        # Compare the new value with the parent node
        if self.data:
            if data < self.data:
                if self.left is None:
                    self.left = Node(data)
                else:
                    self.left.insert(data)
            elif data > self.data:
                if self.right is None:
                    self.right = Node(data)
                else:
                    self.right.insert(data)
        else:
            self.data = data

            # Print the tree

    def PrintTree(self):
        if self.left:
            self.left.PrintTree()
        print(self.data),
        if self.right:
            self.right.PrintTree()


if __name__ == "__main__":
    '''
    from collections import Counter
    p="abbc"
    l=[1,2,3,4,4]
    pCounter=[0]*26
    print(ord('d'))
    pCounter[ord('a') - ord('a')] += 1
    print(pCounter)

    root = Node(12)

    root.insert(6)
    root.insert(14)
    root.insert(3)

    root.PrintTree()
    
    t = MinStack([45,56,59])
    # ["MinStack", "push", "push", "push", "getMin", "pop", "top", "getMin"]
    # [[], [-2], [0], [-3], [], [], [], []]
    t.push(x=10)

    print(t.top())
    t.push(x=20)
    t.push(x=30)
    t.push(x=40)
    print(t.top())
    t.pop()
    print(t.mylist)
    
    s = Solution()

    # print(s.checkRecord(s="ALLAPPL"))
    mat = [[1, 2, 3, 4, 5], [2, 4, 5, 8, 10], [3, 12, 7, 9, 11], [1, 3, 5, 7, 9]]
    # print(s.combinationSum(nums=[2,3,5],target=8))
    mylist = [[3, 5], [5, 3], [5, 3], [2, 3, 2, 2]]

    # print(s.smallestCommonElement(mat=mat))
    # print(s.searchRange([8,7,7,8,8,8],target=8))

    #print(s.threeSum([-1, 0, 1, 2, -1, -4]))
    # print(s.maxProduct([2,3,-2,4]))
    # print(s.maximumProduct([-4,-3,-2,-1,60]))
    # print(s.twoSum(nums=[3,3],target=6))
    # print(s.twoSumLessThanK(A=[358,898,450,732,672,672,256,542,320,573,423,543,591,280,399,923,920,254,135,952,115,536,143,896,411,722,815,635,353,486,127,146,974,495,229,21,733,918,314,670,671,537,533,716,140,599,758,777,185,549], K=1800))
    # print(s.reverse(234))
    # print(s.isPalindrome(121))
    #print(s.combinationTarget(nums=[1,2,3,4,5,6],target=8))
    #print(s.missingNumber(nums=[9,6,4,2,3,5,7,0,1]))
    #print(s.rob([2,6,6,2]))
    #print(s.moveZeroes(nums=[0,7,0,8,8,10,0,12,3,4,8]))
    #print(s.flipAndInvertImage(A=[[1,1,0,0],[1,0,0,1],[0,1,1,1],[1,0,1,0]]))
    #print(s.largestUniqueNumber(nums=[5,7,3,9,4,9,8,3,1]))
    #print(s.shuffle(nums = [1,2,3,4,4,3,2,1], n = 4))
    '''
    s=Solution()
    print(s.lengthOfLongestSubstring(s="abcabcbb"))
