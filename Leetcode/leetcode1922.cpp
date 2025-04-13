#include <bits/stdc++.h>
using namespace std;
class Solution
{
public:
    const int Mod = 1000000007;
    long long qpow(long long x, long long n)
    {
        long long res = 1;
        while (n)
        {
            if (n & 1)
            {
                res = res * x % Mod;
            }
            x = x * x % Mod;
            n >>= 1;
        }
        return res;
    }
    int countGoodNumbers(long long n)
    {
        return qpow(5, (n + 1) / 2) * qpow(4, n / 2) % Mod;
    }
};
int main()
{
    Solution sol;
    cout << sol.countGoodNumbers(1) << endl;
    return 0;
}