#include <bits/stdc++.h>
using namespace std;
class Solution
{
public:
    // 计算子集的异或和
    // 1. 计算子集的个数为2^n
    // 2. 每个元素在子集中出现的次数为2^(n-1)
    // 深度优先搜索函数，用于计算所有子集的异或和
    // nums: 输入的整数数组
    // start: 当前处理的起始索引，避免重复处理元素
    // xorSum: 当前路径(子集)的异或累计值
    // ans: 引用参数，用于累加所有子集的异或和
    void dfs(vector<int> &nums, int start, int xorSum, int &ans)
    {
        ans += xorSum; // 将当前子集的异或和累加到总和中

        // 遍历数组中从start开始的所有元素
        for (int i = start; i < nums.size(); i++)
        {
            // 递归处理下一个元素：
            // 1. i+1 确保不会重复使用同一个元素
            // 2. xorSum ^ nums[i] 更新当前子集的异或值
            dfs(nums, i + 1, xorSum ^ nums[i], ans);
        }
    }

    // 主函数，计算数组所有子集的异或和总和
    // nums: 输入的整数数组
    // 返回值: 所有子集异或和的总和
    int subsetXORSum(vector<int> &nums)
    {
        int ans = 0;          // 存储结果
        dfs(nums, 0, 0, ans); // 从第一个元素开始计算
        return ans;
    }
};
int main()
{
    Solution s;
    vector<int> nums = {5, 1, 6};
    cout << s.subsetXORSum(nums) << endl;
    return 0;
}