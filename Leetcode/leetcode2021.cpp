#include <iostream>
#include <algorithm>
#include <vector>
using namespace std;
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
int main()
{
    Solution s;
    vector<int> nums = {1, 2, 3};
    cout << s.sumOfBeauties(nums) << endl;
    return 0;
}