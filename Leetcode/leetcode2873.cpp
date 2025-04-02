#include <bits/stdc++.h>
using namespace std;
class Solution
{
public:
    long long maximumTripletValue(vector<int> &nums)
    {

        int n = nums.size();
        long long ans = 0, imax = 0, dmax = 0;
        for (int k = 0; k < n; k++)
        {
            imax = max(imax, (long long)nums[k]);
            dmax = max(dmax, imax - nums[k]);
            ans = max(ans, dmax * nums[k]);
        }
        return ans;
    }
};
int main()
{
    Solution s;
    vector<int> nums = {1000000, 1, 1000000};
    cout << s.maximumTripletValue(nums) << endl;
    return 0;
}