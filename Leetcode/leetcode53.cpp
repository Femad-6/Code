#include <bits/stdc++.h>
using namespace std;
class Solution
{
public:
    int maxSubArray(vector<int> &nums)
    {
        // 获取数组长度
        int n = nums.size();
        // 创建DP数组，dp[i]表示以nums[i]结尾的最大子数组和
        int dp[n];
        // 初始化第一个元素
        dp[0] = nums[0];
        // 初始化结果为第一个元素
        int res = dp[0];

        // 遍历数组，计算每个位置的dp值
        for (int i = 1; i < n; i++)
        {
            // 状态转移方程：要么延续前面的子数组，要么从当前元素重新开始
            dp[i] = max(dp[i - 1] + nums[i], nums[i]);
            // 更新全局最大值
            res = max(res, dp[i]);
        }
        return res;
    }
};
int main()
{
    Solution s;
    vector<int> nums = {-2, 1, -3, 4, -1, 2, 1, -5, 4};
    cout << s.maxSubArray(nums);
    return 0;
}