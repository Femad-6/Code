#include <bits/stdc++.h>
using namespace std;
class Solution
{
public:
    bool canBeValid(string s, string locked)
    {
        int n = s.size();
        if (n % 2)
            return false;
        int mn = 0, mx = 0;
        for (int i = 0; i < n; i++)
        {
            if (locked[i] == '1')
            {
                if (s[i] == '(')
                    mx++, mn++;
                if (s[i] == ')')
                {
                    if (--mn < 0)
                        mn = 1;
                    if (--mx < 0)
                        return false;
                }
            }
            else
            {
                mx++;
                if (--mn < 0)
                    mn = 1;
            }
        }
        return mn == 0;
    }
};
int main()
{
    Solution s;
    string str = "))()))";
    string locked = "010100";
    cout << s.canBeValid(str, locked) << endl;
}