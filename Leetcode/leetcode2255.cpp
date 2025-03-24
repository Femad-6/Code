#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
using namespace std;
class Solution
{
public:
    int countPrefixes(vector<string> &words, string s)
    {
        int ans = 0;
        vector<string> sub(s.size());
        for (int i = 0; i < s.size(); i++)
        {
            sub[i] = s.substr(0, i + 1);
        }
        for (auto word : words)
        {
            if (find(sub.begin(), sub.end(), word) != sub.end())
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
    vector<string> words = {"a", "b", "c", "ab", "bc", "abc"};
    string s1 = "abc";
    cout << s.countPrefixes(words, s1) << endl;
    return 0;
}