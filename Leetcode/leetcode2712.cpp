#include <bits/stdc++.h>
using namespace std;
class Solution
{
public:
    long long minimumCost(string s)
    {
        int n = s.size();
        long long ans = 0;
        for (int i = 1; i < n; i++)
        {
            if (s[i - 1] != s[i])
            {
                ans += min(i, n - i);
            }
        }
        return ans;
    }
};
int main()
{
    Solution s;
    string str = "0011";
    cout << s.minimumCost(str) << endl;
    return 0;
}