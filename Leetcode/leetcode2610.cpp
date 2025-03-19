#include <bits/stdc++.h>
using namespace std;
class Solution
{
public:
    vector<vector<int>> findMatrix(vector<int> &nums)
    {
        unordered_map<int, int> cnt;
        for (int x : nums)
        {
            cnt[x]++;
        }

        vector<vector<int>> ans;
        while (!cnt.empty())
        {
            vector<int> a;
            for (auto it = cnt.begin(); it != cnt.end();)
            {
                it->second--;
                a.emplace_back(it->first);
                if (it->second == 0)
                {
                    it = cnt.erase(it);
                }
                else
                {
                    it++;
                }
            }
            ans.push_back(a);
        }
        return ans;
    }
};
int main()
{
    Solution s;
    vector<int> nums = {1, 3, 4, 1, 2, 3, 1};
    vector<vector<int>> result = s.findMatrix(nums);
    for (int i = 0; i < result.size(); i++)
    {
        for (int j = 0; j < result[i].size(); j++)
        {
            cout << result[i][j] << " ";
        }
        cout << endl;
    }
    return 0;
}