#include <iostream>
#include <vector>
using namespace std;
class Solution
{
public:
    int minimizedStringLength(string s)
    {
        int n = s.length();
        vector<int> cnt(26, 0);
        for (int i = 0; i < n; i++)
            cnt[s[i] - 'a']++;
        int res = 0;
        for (int i = 0; i < 26; i++)
        {
            if (cnt[i] > 0)
                res++;
        }
        return res;
    }
};
int main()
{
    Solution s;
    cout << s.minimizedStringLength("aaabc") << endl;
    return 0;
}