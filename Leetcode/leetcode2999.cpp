#include <bits/stdc++.h>
using namespace std;
class Solution
{
public:
    long long numberOfPowerfulInt(long long start, long long finish, int limit, string s)
    {
        string starts = to_string(start - 1), finishs = to_string(finish);
        return calculate(finishs, s, limit) - calculate(starts, s, limit);
    }
    long long calculate(string x, string s, int limit)
    {
        // 当目标数字位数小于后缀长度时，不可能满足条件
        if (x.size() < s.size())
            return 0;
        // 当位数相等时直接比较整个字符串
        if (x.size() == s.size())
            return x >= s ? 1 : 0;

        // 截取目标数字的后缀部分
        string sff = x.substr(x.size() - s.size(), s.size());
        long long cnt = 0;
        int pre = x.size() - s.size(); // 前缀部分的长度

        // 处理前缀部分的每个数字位
        for (int i = 0; i < pre; i++)
        {
            // 当前位超过限制值时，计算剩余位的最大组合数并退出
            if (limit < x[i] - '0')
            {
                cnt += (long)pow(limit + 1, pre - i);
                return cnt;
            }
            // 累加当前位可取值的组合数（当前位数字 × 后面位的可能组合）
            cnt += (long)(x[i] - '0') * pow(limit + 1, pre - i - 1);
        }

        // 最后检查后缀是否符合要求
        if (sff >= s)
            cnt++;
        return cnt;
    }
};
int main()
{
    Solution s;
    long long start = 1, finish = 6000, limit = 4;
    string t = "124";
    cout << s.numberOfPowerfulInt(start, finish, limit, t) << endl;
    return 0;
}