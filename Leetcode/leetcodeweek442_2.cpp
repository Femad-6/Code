#include <bits/stdc++.h>
using namespace std;

class Solution
{
public:
    int intersect(vector<int> a, vector<int> b)
    {
        int cnt = 0;
        unordered_set<int> mp;
        for (int num : a)
        {
            mp.insert(num);
        }
        for (int num : b)
        {
            if (mp.count(num))
            {
                mp.erase(num);
                cnt++;
            }
        }
        return cnt;
    }

    int numberOfComponents(vector<vector<int>> &properties, int k)
    {
        int n = properties.size();
        vector<int> parent(n);
        for (int i = 0; i < n; i++)
        {
            parent[i] = i;
        }

        function<int(int)> find = [&](int x)
        {
            return parent[x] == x ? x : parent[x] = find(parent[x]);
        };

        auto unite = [&](int x, int y)
        {
            int px = find(x);
            int py = find(y);
            if (px != py)
            {
                parent[px] = py;
            }
        };

        for (int i = 0; i < n; i++)
        {
            for (int j = i + 1; j < n; j++)
            {
                if (intersect(properties[i], properties[j]) >= k)
                {
                    unite(i, j);
                }
            }
        }

        int ans = 0;
        for (int i = 0; i < n; i++)
        {
            if (parent[i] == i)
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
    vector<vector<int>> properties = {{1, 2}, {2, 3}, {3, 4}};
    int k = 1;
    cout << s.numberOfComponents(properties, k) << endl;
    return 0;
}