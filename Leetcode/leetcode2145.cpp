#include <iostream>
#include <vector>
#include <unordered_set>
#include <algorithm>
using namespace std;

class Solution
{
public:
    int numberOfArrays(vector<int> &differences, int lower, int upper)
    {
        int n = differences.size();
        vector<long long> arr(n + 1);             // 存储原数组
        arr[0] = lower;                           // 假设原数组的第一个元素为0
        long long minVal = lower, maxVal = lower; // 记录原数组的最小值和最大值
        int ans = 0;
        for (int i = 1; i <= n; i++)
        {
            arr[i] = arr[i - 1] + differences[i - 1]; // 计算原数组的第i个元素
        }
        minVal = *min_element(arr.begin(), arr.end()); // 计算原数组的最小值
        maxVal = *max_element(arr.begin(), arr.end()); // 计算原数组的最大值
        maxVal += lower - minVal;
        while (maxVal <= upper)
        {
            ans++;
            maxVal++;
        }
        return ans; // 返回符合条件的原数组的个数
    }
};

int main()
{
    Solution sol;
    vector<int> differences = {4, -7, 2};
    int lower = 3, upper = 6;
    cout << sol.numberOfArrays(differences, lower, upper) << endl; // Example test case
    return 0;
}