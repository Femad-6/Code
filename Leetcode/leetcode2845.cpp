#include <bits/stdc++.h>
using namespace std;
class Solution
{
public:
    long long countInterestingSubarrays(vector<int> &nums, int modulo, int k)
    {
        long long ans = 0;            // Initialize the result variable to store the count of interesting subarrays.
        int n = nums.size();          // Get the size of the input array.
        vector<int> prefix(n + 1, 0); // Create a prefix array to store cumulative counts of elements divisible by modulo.
        for (int i = 0; i < n; i++)
        {                                                                   // Iterate through the array.
            prefix[i + 1] = (prefix[i] + (nums[i] % modulo == k)) % modulo; // Calculate the cumulative count of elements divisible by modulo.
        }
        unordered_map<int, int> count; // Create a map to store the count of each prefix value.
        for (int i = 0; i <= n; i++)
        {                                                   // Iterate through the prefix array.
            int target = (prefix[i] - k + modulo) % modulo; // Calculate the target value to find in the map.
            ans += count[target];                           // Add the count of the target value to the result.
            count[prefix[i]]++;                             // Increment the count of the current prefix value in the map.
        }
        return ans; // Return the total count of interesting subarrays.
    }
};
int main()
{
    Solution sol;
    vector<int> nums = {3, 1, 9, 6}; // Example input
    int modulo = 3, k = 0;
    cout << sol.countInterestingSubarrays(nums, modulo, k) << endl; // Output the result
}