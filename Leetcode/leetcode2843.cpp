#include <bits/stdc++.h>
using namespace std;
class Solution
{
public:
    int countSymmetricIntegers(int low, int high)
    {
        int ans = 0;
        for (int i = low; i <= high; i++)
        {
            string s = to_string(i);
            int n = s.size();
            if (n % 2 == 0)
            {
                int sum = 0;
                for (int j = 0; j < n / 2; j++)
                {
                    sum += s[j] - '0';
                }
                for (int j = n / 2; j < n; j++)
                {
                    sum -= s[j] - '0';
                }
                if (sum == 0)
                {
                    ans++;
                }
            }
        }
        return ans;
    }
};
int main()
{
    Solution s;
    int low = 1200, high = 1230;
    cout << s.countSymmetricIntegers(low, high) << endl;
    return 0;
}