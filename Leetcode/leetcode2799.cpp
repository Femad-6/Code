#include <bits/stdc++.h>
using namespace std;
class Solution
{
public:
    int countCompleteSubarrays(vector<int> &nums)
    {
        set<int> uniqueElements(nums.begin(), nums.end());
        int uniqueCount = uniqueElements.size();
        int n = nums.size();
        int count = 0;
        for (int i = 0; i <= n - uniqueCount; i++)
        {
            set<int> currentSet;
            for (int j = i; j < n; j++)
            {
                currentSet.insert(nums[j]);
                if (currentSet.size() == uniqueCount)
                {
                    count++;
                }
            }
        }
        return count;
    }
};
int main()
{
    Solution sol;
    vector<int> nums = {1, 2, 3, 4, 5};               // Example input
    cout << sol.countCompleteSubarrays(nums) << endl; // Output the result
    return 0;
}