#include <bits/stdc++.h>
using namespace std;
class Solution
{
public:
    bool validPath(int n, vector<vector<int>> &edges, int source, int destination)
    {
        vector<vector<int>> graph(n); // 初始化图，每个节点的邻居列表
        for (auto &edge : edges)
        {
            graph[edge[0]].push_back(edge[1]); // 添加边到邻居列表
            graph[edge[1]].push_back(edge[0]); // 添加反向边
        }
        vector<bool> visited(n, false); // 访问标记数组
        queue<int> q;                   // 队列用于BFS
        q.push(source);                 // 从源节点开始
        visited[source] = true;         // 标记源节点为已访问
        while (!q.empty())
        {
            int node = q.front(); // 获取当前节点
            q.pop();              // 出队
            if (node == destination)
                return true; // 如果到达目标节点，返回true
            for (int neighbor : graph[node])
            { // 遍历当前节点的邻居
                if (!visited[neighbor])
                {                             // 如果邻居未被访问
                    visited[neighbor] = true; // 标记为已访问
                    q.push(neighbor);         // 入队
                }
            }
        }
        return false; // 如果遍历完所有节点仍未找到目标节点，返回false
    }
};
int main()
{
    Solution sol;
    int n = 5;                                                                         // Example input
    vector<vector<int>> edges = {{0, 1}, {1, 2}, {2, 3}, {3, 4}};                      // Example input
    int source = 0, destination = 4;                                                   // Example input
    cout << (sol.validPath(n, edges, source, destination) ? "True" : "False") << endl; // Output the result
    return 0;
}