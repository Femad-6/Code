#include <iostream>
#include <algorithm>
using namespace std;
class Solution
{
public:
    int minimumSum(int n, int k)
    {
        int m = min(n, k / 2);
        return (m * (m + 1) + (2 * k + n - m - 1) * (n - m)) / 2;
    }
};
int main()
{
    Solution s;
    cout << s.minimumSum(2, 6) << endl;
    return 0;
}