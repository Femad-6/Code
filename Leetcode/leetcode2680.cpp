#include <bits/stdc++.h>
using namespace std;
class Solution
{
public:
    using ll = long long;
    long long maximumOr(vector<int> &nums, int k)
    {
        int n = nums.size();
        ll or_sum = 0;
        ll multi_bits = 0;
        for (int x : nums)
        {
            multi_bits |= x & or_sum;
            or_sum |= x;
        }

        ll res = 0;
        for (int x : nums)
        {
            res = max(res, (or_sum ^ x) | (1ll * x << k) | multi_bits);
        }
        return res;
    }
};
int main()
{
    Solution s;
    vector<int> nums = {12, 9};
    int k = 1;
    cout << s.maximumOr(nums, k);
    return 0;
}