#include <bits/stdc++.h>
using namespace std;
class Solution
{
public:
    long long countGood(vector<int> &nums, int k)
    {
        long long ans = 0;
        unordered_map<int, int> cnt;
        int pairs = 0, left = 0;
        for (int x : nums)
        {
            pairs += cnt[x]++;
            while (pairs >= k)
            {
                pairs -= --cnt[nums[left]];
                left++;
            }
            ans += left;
        }
        return ans;
    }
};
int main()
{
    Solution sol;
    vector<int> nums = {1, 1, 1, 1, 1};
    cout << sol.countGood(nums, 10) << endl; // 1
    return 0;
}