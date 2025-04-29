#include <bits/stdc++.h>
using namespace std;
class Solution
{
public:
    long long countSubarrays(vector<int> &nums, int k)
    {
        int mx = *max_element(nums.begin(), nums.end());
        long long ans = 0;
        int cnt = 0, left = 0;
        for (int x : nums)
        {
            if (x == mx)
            {
                cnt++;
            }
            while (cnt == k)
            {
                if (nums[left] == mx)
                {
                    cnt--;
                }
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
    vector<int> nums = {1, 3, 2, 3, 3}; // Example input
    long long k = 2;
    cout << sol.countSubarrays(nums, k) << endl; // Output the result
    return 0;
}