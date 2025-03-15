/*
 * @lc app=leetcode.cn id=3306 lang=cpp
 *
 * [3306] 元音辅音字符串计数 II
 */
#include <bits/stdc++.h>
using namespace std;
// @lc code=start
class Solution
{
public:
    long long countOfSubstrings(string word, int k)
    {
        set<char> vowels = {'a', 'e', 'i', 'o', 'u'};
        auto count = [&](int m) -> long long
        {
            int n = word.size(), a = 0;
            long long ans = 0;
            map<char, long long> occur;
            for (int i = 0, j = 0; i < n; i++)
            {
                while (j < n && (a < m || occur.size() < vowels.size()))
                {
                    if (vowels.count(word[j]))
                        occur[word[j]]++;
                    else
                        a++;
                    j++;
                }
                if (a >= m && occur.size() == vowels.size())
                {
                    ans += n - j + 1;
                }
                if (vowels.count(word[i]))
                {
                    occur[word[i]]--;
                    if (occur[word[i]] == 0)
                    {
                        occur.erase(word[i]);
                    }
                }
                else
                    a--;
            }
            return ans;
        };
        return count(k) - count(k + 1);
    }
};
// @lc code=end
