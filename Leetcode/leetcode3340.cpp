#include <vector>
#include <algorithm>
#include <iostream>
#include <string>
using namespace std;

class Solution
{
public:
    bool isBalanced(string num)
    {
        int ans = 0;
        int x;
        for (int i = 0; i < num.size(); i += 2)
        {
            x = num[i] - '0';
            ans += x;
        }
        for (int i = 1; i < num.size(); i += 2)
        {
            x = num[i] - '0';
            ans -= x;
        }
        if (ans == 0)
        {
            return true;
        }
        return false;
    }
};
int main()
{
    Solution s;
    string str = "24123";
    cout << s.isBalanced(str) << endl;
    return 0;
}