#include <bits/stdc++.h>
using namespace std;
class Solution
{
public:
    string addSpaces(string s, vector<int> &spaces)
    {
        for (int i = 0; i < spaces.size(); i++)
        {
            s.insert(spaces[i] + i, " ");
        }
        return s;
        //
    }
};

int main()
{
    Solution s;
    string s1 = "LeetcodeHelpsMeLearn";
    vector<int> spaces = {8, 13, 15};
    cout << s.addSpaces(s1, spaces) << endl;
    return 0;
}