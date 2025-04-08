#include <bits/stdc++.h>
using namespace std;
class Solution
{
public:
    int minimumOperations(vector<int> &nums)
    {
        unordered_set<int> s;
        for (int i = nums.size() - 1; i >= 0; i--)
        {
            if (!s.insert(nums[i]).second)
            {
                return i / 3 + 1;
            }
        }
        return 0;
    }
};
int main()
{
    Solution s;
    vector<int> nums = {1, 2, 3, 4};
    cout << s.minimumOperations(nums) << endl;
    return 0;
}
