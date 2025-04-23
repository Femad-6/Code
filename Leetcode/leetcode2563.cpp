#include <bits/stdc++.h>
using namespace std;
class Solution
{
public:
    long long countFairPairs(vector<int> &nums, int lower, int upper)
    {
        sort(nums.begin(), nums.end());
        long long ans = 0;
        for (int i = 0; i < nums.size(); i++)
        {
            auto r = upper_bound(nums.begin(), nums.begin() + i, upper - nums[i]);
            auto l = lower_bound(nums.begin(), nums.begin() + i, lower - nums[i]);
            ans += r - l;
        }
        return ans;
    }
};
int main()
{
    Solution sol;
    vector<int> nums = {0, 1, 7, 4, 4, 5};
    cout << sol.countFairPairs(nums, 3, 6) << endl; // 6

    return 0;
}