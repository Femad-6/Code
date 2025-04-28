#include <bits/stdc++.h>
using namespace std;
class Solution
{
public:
    long long countSubarrays(vector<int> &nums, long long k)
    {
        long long sum = 0;   // 用于存储当前子数组的和
        long long count = 0; // 用于存储满足条件的子数组数量
        int left = 0;        // 左指针，用于收缩窗口
        for (int right = 0; right < nums.size(); ++right)
        {
            sum += nums[right]; // 将当前元素加入子数组和
            while (sum * (right - left + 1) >= k)
            {                      // 检查当前子数组是否满足条件
                sum -= nums[left]; // 移除左指针指向的元素
                left++;            // 收缩窗口
            }
            count += right - left + 1; // 累加满足条件的子数组数量
        }
        return count; // 返回满足条件的子数组数量
    }
};
int main()
{
    Solution sol;
    vector<int> nums = {1, 2, 3, 4};             // Example input
    long long k = 10;                            // Example input
    cout << sol.countSubarrays(nums, k) << endl; // Output the result
    return 0;
}