#include <iostream>
#include <map>
#include <string>

using namespace std;

void solve()
{
    string s, t;
    int k;
    cin >> s >> t >> k;

    if (k == 0)
    {
        if (s.empty())
        {
            if (t.empty())
            {
                cout << "0\n";
            }
            else
            {
                cout << "-1\n";
            }
            return;
        }
        else
        {
            if (t.size() != s.size())
            {
                cout << "-1\n";
                return;
            }
            char c = t[0];
            for (char ch : t)
            {
                if (ch != c)
                {
                    cout << "-1\n";
                    return;
                }
            }
            cout << "1\n";
            cout << "" << " " << c << "\n";
            return;
        }
    }

    int s_len = s.size();
    int t_len = t.size();

    if (k - 1 > s_len || k - 1 > t_len)
    {
        cout << "-1\n";
        return;
    }

    for (int i = 0; i < k - 1; ++i)
    {
        if (i >= s_len || i >= t_len || s[i] != t[i])
        {
            cout << "-1\n";
            return;
        }
    }

    int pos_t = k - 1;
    map<string, string> rules;

    for (int i = k - 1; i < s_len; ++i)
    {
        int start = i - k + 1;
        string lambda = s.substr(start, k);

        if (rules.find(lambda) != rules.end())
        {
            string gamma = rules[lambda];
            if (gamma.empty())
            {
                continue;
            }
            else
            {
                if (pos_t >= t_len || t[pos_t] != gamma[0])
                {
                    cout << "-1\n";
                    return;
                }
                ++pos_t;
            }
        }
        else
        {
            if (pos_t >= t_len)
            {
                rules[lambda] = "";
            }
            else
            {
                rules[lambda] = string(1, t[pos_t]);
                ++pos_t;
            }
        }
    }

    if (pos_t != t_len)
    {
        cout << "-1\n";
        return;
    }

    cout << rules.size() << "\n";
    for (auto &entry : rules)
    {
        cout << entry.first << " " << entry.second << "\n";
    }
}

int main()
{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;
    while (T--)
    {
        solve();
    }

    return 0;
}