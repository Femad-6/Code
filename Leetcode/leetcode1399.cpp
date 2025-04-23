#include <bits/stdc++.h>
using namespace std;
class Solution
{
public:
    int solve(int x)
    {
        int ans = 0;
        while (x)
        {
            ans += x % 10;
            x /= 10;
        }
        return ans;
    }
    int countLargestGroup(int n)
    {
        vector<int> cnt(37, 0); // 1-9的和最大为36
        for (int i = 1; i <= n; i++)
        {
            cnt[solve(i)]++;
        }
        int maxCount = *max_element(cnt.begin(), cnt.end());
        return count(cnt.begin(), cnt.end(), maxCount);
    }
};
int main()
{
    Solution sol;
    int n = 13;                               // Example input
    cout << sol.countLargestGroup(n) << endl; // Output the result 4
    return 0;
}