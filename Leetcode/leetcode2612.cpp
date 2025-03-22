#include <bits/stdc++.h>
using namespace std;
class Solution
{
public:
    vector<int> minReverseOperations(int n, int p, vector<int> &banned, int k)
    {
        unordered_set<int> ban{banned.begin(), banned.end()};
        set<int> indices[2];
        for (int i = 0; i < n; i++)
        {
            if (i != p && !ban.count(i))
            {
                indices[i % 2].insert(i);
            }
        }
        indices[0].insert(n);
        indices[1].insert(n);
        vector<int> ans(n, -1);
        ans[p] = 0;
        queue<int> q;
        q.push(p);
        while (!q.empty())
        {
            int i = q.front();
            q.pop();
            int mn = max(i - k + 1, k - i - 1);
            int mx = min(i + k - 1, 2 * n - k - i - 1);
            auto &st = indices[mn % 2];
            for (auto it = st.lower_bound(mn); *it <= mx; it = st.erase(it))
            {
                ans[*it] = ans[i] + 1;
                q.push(*it);
            }
        }
        return ans;
    }
};
int main()
{
    Solution s;
    int n = 4, p = 0, k = 4;
    vector<int> banned = {1, 2};
    vector<int> ans = s.minReverseOperations(n, p, banned, k);
    for (int i = 0; i < ans.size(); i++)
    {
        cout << ans[i] << " ";
    }
    return 0;
}