#include <bits/stdc++.h>
using namespace std;
class Solution
{
public:
    vector<vector<int>> differenceOfDistinctValues(vector<vector<int>> &grid)
    {
        int m = grid.size(), n = grid[0].size();
        vector<vector<int>> ans(m, vector<int>(n, 0));
        for (int i = 0; i < m; i++)
        {
            for (int j = 0; j < n; j++)
            {
                set<int> s1;
                int x = i + 1;
                int y = j + 1;
                while (x < m && y < n)
                {
                    s1.insert(grid[x][y]);
                    x += 1;
                    y += 1;
                }
                x = i - 1;
                y = j - 1;
                set<int> s2;
                while (x >= 0 && y >= 0)
                {
                    s2.insert(grid[x][y]);
                    x -= 1;
                    y -= 1;
                }
                ans[i][j] = abs((int)s1.size() - (int)s2.size());
            }
        }
        return ans;
    }
};
int main()
{
    Solution s;
    vector<vector<int>> grid{{1, 2, 3}, {3, 1, 5}, {3, 2, 1}};
    vector<vector<int>> ans = s.differenceOfDistinctValues(grid);
    for (auto i : ans)
    {
        for (auto j : i)
        {
            cout << j << " ";
        }
        cout << endl;
    }

    return 0;
}