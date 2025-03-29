#include <bits/stdc++.h>
using namespace std;
class Solution
{
public:
    int longestCycle(vector<int> &edges)
    {
        int n = edges.size();
        vector<int> label(n);
        int ans = -1, cur = 0;
        for (int i = 0; i < n; i++)
        {
            if (label[i])
                continue;
            int pos = i, start = cur;
            while (pos != -1)
            {
                cur++;
                if (label[pos])
                {
                    if (start < label[pos])
                        ans = max(ans, cur - label[pos]);
                    break;
                }
                label[pos] = cur;
                pos = edges[pos];
            }
        }
        return ans;
    }
};
int main()
{
    Solution s;
    vector<int> edges{3, 3, 4, 2, 3};
    cout << s.longestCycle(edges) << endl; // Output: 3
    return 0;
}