/*
 * @lc app=leetcode.cn id=2062 lang=cpp
 *
 * [2062] 统计字符串中的元音子字符串
 */
#include <bits/stdc++.h>
using namespace std;
// @lc code=start
class Solution
{
public:
    int countVowelSubstrings(string word)
    {
        set<char> vowels = {'a', 'e', 'i', 'o', 'u'};
        int len = word.size();
        int ans = 0;

        for (int i = 0; i < len; i++)
        {
            map<char, int> occur;
            for (int j = i; j < len; j++)
            {
                if (vowels.count(word[j]))
                {
                    occur[word[j]]++;
                }
                else
                {
                    break;
                }
                if (occur.size() == 5)
                {
                    ans++;
                }
            }
        }
        return ans;
    }
};
// @lc code=end
