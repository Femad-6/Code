#include <bits/stdc++.h>
using namespace std;
class Solution
{
public:
    long long countSubarrays(vector<int> &nums, int minK, int maxK)
    {

        long long ans = 0;                                      // Initialize the result variable to store the count of subarrays.
        int minPosition = -1, maxPosition = -1, leftBound = -1; // Initialize variables to track positions of minK, maxK, and the left boundary of the current subarray.
        for (int i = 0; i < nums.size(); i++)
        { // Iterate through the array.
            if (nums[i] < minK || nums[i] > maxK)
            { // If the current number is outside the range [minK, maxK], reset positions and left boundary.
                minPosition = -1;
                maxPosition = -1;
                leftBound = i; // Update the left boundary to the current index.
            }
            if (nums[i] == minK)
            { // If the current number is equal to minK, update its position.
                minPosition = i;
            }
            if (nums[i] == maxK)
            { // If the current number is equal to maxK, update its position.
                maxPosition = i;
            }
            ans += max(0, min(minPosition, maxPosition) - leftBound); // Calculate the count of valid subarrays ending at index i and add it to ans.
        }
        return ans; // Return the total count of valid subarrays.
    }
};
int main()
{
    Solution sol;
    vector<int> nums = {1, 3, 5, 2, 7, 5};                // Example input
    int minK = 1, maxK = 5;                               // Example input
    cout << sol.countSubarrays(nums, minK, maxK) << endl; // Output the result
    return 0;
}