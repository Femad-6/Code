#include <bits/stdc++.h>
using namespace std;

class UnionFind
{
private:
    vector<int> parent;
    vector<int> rank;

public:
    UnionFind(int n)
    {
        parent.resize(n);
        rank.resize(n, 0);
        for (int i = 0; i < n; ++i)
        {
            parent[i] = i;
        }
    }

    int find(int x)
    {
        if (parent[x] != x)
        {
            parent[x] = find(parent[x]);
        }
        return parent[x];
    }

    void unite(int x, int y)
    {
        int rx = find(x);
        int ry = find(y);
        if (rx != ry)
        {
            if (rank[rx] < rank[ry])
            {
                parent[rx] = ry;
            }
            else
            {
                parent[ry] = rx;
                if (rank[rx] == rank[ry])
                {
                    rank[rx]++;
                }
            }
        }
    }

    bool connected(int x, int y)
    {
        return find(x) == find(y);
    }
};

class Solution
{
public:
    vector<bool> pathExistenceQueries(int n, vector<int> &nums, int maxDiff, vector<vector<int>> &queries)
    {
        UnionFind uf(n);
        for (int i = 0; i < n - 1; ++i)
        {
            if (nums[i + 1] - nums[i] <= maxDiff)
            {
                uf.unite(i, i + 1);
            }
        }
        vector<bool> res;
        for (const auto &q : queries)
        {
            int u = q[0];
            int v = q[1];
            res.push_back(uf.connected(u, v));
        }
        return res;
    }
};

int main()
{
    Solution sol;
    int n = 2;
    vector<int> nums = {1, 3}; // Example input
    int maxDiff = 1;           // Example input
    vector<vector<int>> queries = {{0, 0}, {0, 1}};
    vector<bool> res = sol.pathExistenceQueries(n, nums, maxDiff, queries);
    for (auto r : res)
    {
        cout << (r ? "True" : "False") << endl; // Output the result
    }
    return 0;
}
