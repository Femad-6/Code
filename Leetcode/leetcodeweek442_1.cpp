#include <bits/stdc++.h>
using namespace std;
class Solution
{
public:
    int maxContainers(int n, int w, int maxWeight)
    {
        int mx = n * n;
        int ans = maxWeight / w;
        if (ans > mx)
            ans = mx;
        return ans;
    }
};
int main()
{
    Solution s;
    int n = 10, w = 5, maxWeight = 10;
    cout << s.maxContainers(n, w, maxWeight) << endl;
    return 0;
}