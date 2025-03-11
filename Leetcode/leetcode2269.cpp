#include <bits/stdc++.h>
using namespace std;
class Solution
{
public:
    int solve(int i, string s, int k)
    {

        string a = s.substr(i, k);
        return stoi(a);
    }
    int divisorSubstrings(int num, int k)
    {
        int ans = 0;
        string s = to_string(num);
        int n = s.size();
        for (int i = 0; i <= n - k; i++)
        {
            if (num % solve(i, s, k) == 0)
            {
                ans++;
            }
        }
        return ans;
    }
};
int main()
{
    Solution s;
    int num = 430043;
    int k = 2;
    cout << s.divisorSubstrings(num, k) << endl;
}