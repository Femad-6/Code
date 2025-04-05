#include <bits/stdc++.h>
using namespace std;
class Solution
{
public:
    // 计算子集的异或和
    // 1. 计算子集的个数为2^n
    // 2. 每个元素在子集中出现的次数为2^(n-1)
    void dfs(vector<int> &nums, int start, int xorSum, int &ans)
    {
        ans += xorSum; // 累加当前子集的异或和
        for (int i = start; i < nums.size(); i++)
        {
            dfs(nums, i + 1, xorSum ^ nums[i], ans); // 递归计算下一个元素
        }
    }
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