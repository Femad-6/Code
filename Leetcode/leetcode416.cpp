#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
class Solution
{
public:
    bool canPartition(vector<int> &nums)
    {
        int n = nums.size();
        int sum = 0;
        for (int i = 0; i < n; i++)
        {
            sum += nums[i];
        }
        if (sum % 2 != 0)
            return false;
        int target = sum / 2;
        vector<vector<bool>> dp(n + 1, vector<bool>(target + 1, false));
        for (int i = 0; i <= n; i++)
        {
            dp[i][0] = true; // 0可以由任何元素组合而成
        }
        for (int i = 1; i <= n; i++)
        {
            for (int j = 1; j <= target; j++)
            {
                if (j < nums[i - 1])
                {
                    dp[i][j] = dp[i - 1][j]; // 不选当前元素
                }
                else
                {
                    dp[i][j] = dp[i - 1][j] || dp[i - 1][j - nums[i - 1]]; // 选或不选当前元素
                }
            }
        }
        return dp[n][target];
    }
};
int main()
{
    Solution s;
    vector<int> nums = {1, 5, 11, 5};
    cout << s.canPartition(nums) << endl;
    return 0;
}