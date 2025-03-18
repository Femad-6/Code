#include <bits/stdc++.h>
using namespace std;
class Solution
{
public:
    int minSwaps(string s)
    {
        int cnt = 0, mincnt = 0;
        for (int i = 0; i < s.size(); i++)
        {
            if (s[i] == '[')
            {
                cnt++;
            }
            else
            {
                cnt--;
                mincnt = min(mincnt, cnt);
            }
        }
        return (-mincnt + 1) / 2;
    }
};
int main()
{
    Solution s;
    cout << s.minSwaps("]]][[[") << endl;
    return 0;
}