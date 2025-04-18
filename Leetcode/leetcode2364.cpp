#include <iostream>
#include <vector>
#include <unordered_map>
using namespace std;
class Solution
{
public:
    long long countBadPairs(vector<int> &nums)
    {
        long long ans = 0;
        unordered_map<int, int> mp;
        for (int i = 0; i < nums.size(); i++)
        {
            ans += i - mp[nums[i] - i];
            mp[nums[i] - i]++;
        }
        return ans;
    }
};
int main()
{
    Solution sol;
    vector<int> nums = {4, 1, 3, 3};
    cout << sol.countBadPairs(nums) << endl;

    return 0;
}