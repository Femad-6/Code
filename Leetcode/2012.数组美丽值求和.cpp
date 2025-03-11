/*
 * @lc app=leetcode.cn id=2012 lang=cpp
 *
 * [2012] 数组美丽值求和
 */
#include <iostream>
#include <vector>
using namespace std;
// @lc code=start
class Solution
{
public:
    int sumOfBeauties(vector<int> &nums)
    {
        int n = nums.size();
        vector<int> max(n);
        vector<int> min(n);
        max[0] = nums[0];
        min[n - 1] = nums[n - 1];
        for (int i = 1; i < n; i++)
        {
            max[i] = max[i - 1] > nums[i] ? max[i - 1] : nums[i];
        }
        for (int i = n - 2; i >= 0; i--)
        {
            min[i] = min[i + 1] < nums[i] ? min[i + 1] : nums[i];
        }
        int ans = 0;
        for (int i = 1; i <= n - 2; i++)
        {
            if (nums[i] > max[i - 1] && nums[i] < min[i + 1])
            {
                ans += 2;
            }
            else if (nums[i] > nums[i - 1] && nums[i] < nums[i + 1])
            {
                ans += 1;
            }
        }
        return ans;
    }
};
// @lc code=end
