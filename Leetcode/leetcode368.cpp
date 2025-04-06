#include <bits/stdc++.h>
using namespace std;
class Solution
{
public:
    vector<int> largestDivisibleSubset(vector<int> &nums)
    {
        // 排序保证后续只需比较前序元素
        sort(nums.begin(), nums.end());
        int n = nums.size();
        int maxi = 0; // 记录最长子集末尾索引

        // f[i] 表示以nums[i]结尾的最大子集长度
        // from[i] 记录前驱节点索引
        vector<int> f(n), from(n, -1);

        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < i; j++)
            {
                // 当满足整除条件且可以延长子序列时
                if (nums[i] % nums[j] == 0 && f[j] > f[i])
                {
                    f[i] = f[j]; // 继承子序列长度
                    from[i] = j; // 记录来源索引
                }
            }
            f[i]++; // 包含当前元素自身
            if (f[i] > f[maxi])
                maxi = i; // 更新最长子集末尾索引
        }

        // 回溯构造结果路径
        vector<int> path;
        for (int i = maxi; i >= 0; i = from[i])
        {
            path.push_back(nums[i]);
        }
        return path;
    }
};
int main()
{
    Solution s;
    vector<int> nums = {1, 2, 4, 8};
    vector<int> path = s.largestDivisibleSubset(nums);
    for (int i = 0; i < path.size(); i++)
    {
        cout << path[i] << " ";
    }
    return 0;
}