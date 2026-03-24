#include <bits/stdc++.h>
using namespace std;
int main()
{
    string s;
    cin >> s;
    int n = s.length();
    for (int j = 0; j <= 1; j++)
    {
        int start = 0;
        int des = 0;
        while (s[start] == 'a')
        {
            start++;
        }
        if (start >= n)
        {
            s[n - 1] = 'z';
        }
        for (int i = start; i < n; i++)
        {
            if (s[i] == 'a')
            {
                break;
            }
            des++;
        }
        for (int i = start; des > 0; i++, des--)
        {
            int d = s[i] - 'a' - 1;
            s[i] = 'a' + d;
        }
    }
    cout << s << endl;
    return 0;
}