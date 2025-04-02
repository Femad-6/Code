#include <bits/stdc++.h>
using namespace std;
class Solution
{
public:
    int arithmeticTriplets(vector<int> &nums, int diff)
    {
        int n = nums.size();
        int ans = 0;
        vector<int> dp(n, 0);
        for (int i = 0; i < n; i++)
        {
            int x = 0;
            int m = nums[i];
            for (int j = i + 1; j < n; j++)
            {

                if (nums[j] - m == diff)
                {
                    x++;
                    m = nums[j];
                }
            }
            dp[i] = x;
        }
        for (int i = 0; i < n; i++)
        {
            cout << dp[i] << " ";
            if (dp[i] >= 2)
            {
                ans++;
            }
        }
        return ans;
    }
};
int main()
{
    Solution s;
    vector<int> nums = {1, 5, 6, 9};
    int diff = 4;
    cout << s.arithmeticTriplets(nums, diff) << endl;
    return 0;
}