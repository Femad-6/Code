#include <bits/stdc++.h>
using namespace std;
class Solution
{
public:
    int percentageLetter(string s, char letter)
    {
        int n = s.length();
        int ans = 0;
        for (int i = 0; i < n; i++)
        {
            if (s[i] == letter)
            {
                ans++;
            }
        }
        return ans * 100 / n;
    }
};
int main()
{
    Solution s;
    string str = "foobar";
    char letter = 'o';
    cout << s.percentageLetter(str, letter) << endl;
    return 0;
}