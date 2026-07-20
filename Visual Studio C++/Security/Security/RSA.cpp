#include <iostream>
#include <string>
#include <vector>
#include <cmath>
#include <algorithm>
using namespace std;

// 快速幂取模：计算 (base^exponent) % mod，防止大数溢出
long long mod_pow(long long base, long long exponent, long long mod) {
    long long result = 1;
    base = base % mod;
    while (exponent > 0) {
        if (exponent % 2 == 1) {
            result = (result * base) % mod;
        }
        base = (base * base) % mod;
        exponent /= 2;
    }
    return result;
}

// 扩展欧几里得算法：求模逆元（用于验证密钥正确性）
long long exgcd(long long a, long long b, long long& x, long long& y) {
    if (b == 0) {
        x = 1;
        y = 0;
        return a;
    }
    long long d = exgcd(b, a % b, y, x);
    y -= a / b * x;
    return d;
}

// 将单个字符转换为数字（使用ASCII码支持大小写、数字及其他符号）
int char_to_num(char c) {
    return (unsigned char)c;
}

// 将数字转换回字符
char num_to_char(int num) {
    return (char)num;
}

// 加密单个数字（对应单个字符/空格）
long long encrypt_num(int num, long long e, long long n) {
    return mod_pow(num, e, n);
}

// 解密单个密文数字
int decrypt_num(long long cipher_num, long long d, long long n) {
    long long num = mod_pow(cipher_num, d, n);
    return (int)num;
}

// 加密字符串：逐字符加密，返回密文数字列表
vector<long long> encrypt_string(const string& plain_text, long long e, long long n) {
    vector<long long> cipher_nums;
    for (char c : plain_text) {
        int num = char_to_num(c);
        if (num != -1) {
            cipher_nums.push_back(encrypt_num(num, e, n));
        }
    }
    return cipher_nums;
}

// 解密密文数字列表：返回明文字符串
string decrypt_string(const vector<long long>& cipher_nums, long long d, long long n) {
    string plain_text;
    for (long long num : cipher_nums) {
        int dec_num = decrypt_num(num, d, n);
        plain_text += num_to_char(dec_num);
    }
    return plain_text;
}

int main() {
    // 1. 输入初始明文（匹配截图：THIS IS A TEST）
    string plain_text;
    cout << "请输入初始明文：";
    getline(cin, plain_text);

    // 2. 输入素数p和q
    long long p, q;
    cout << "请输入素数p和q:";
    cin >> p >> q;

    // 3. 自动生成密钥
    long long n = p * q;
    long long phi = (p - 1) * (q - 1);

    // 寻找与 φ(n) 互质的公钥 e
    long long e = 2;
    long long x, y;
    while (e < phi) {
        if (exgcd(e, phi, x, y) == 1) {
            break;
        }
        e++;
    }

    // 计算私钥 d，利用扩展欧几里得算法求 e 模 φ(n) 的逆元
    long long d = (x % phi + phi) % phi;

    // 输出生成后的密钥
    cout << "自动生成公钥PU={e=" << e << ",n=" << n << "}" << endl;
    cout << "自动生成私钥PR={d=" << d << ",n=" << n << "}" << endl;

    // 存储密文的全局变量
    vector<long long> cipher_nums;

    while (true) {
        // 4. 菜单功能（匹配截图）
        cout << "-----------------------------" << endl;
        cout << "        欢迎进入RSA算法" << endl;
        cout << "        1--加密" << endl;
        cout << "        2--解密" << endl;
        cout << "        3--退出" << endl;
        cout << "-----------------------------" << endl;

        int choice;
        cout << "请输入要选择的功能号：";
        cin >> choice;

        if (choice == 1) {
            // 加密功能：输出密文（空格分隔，匹配截图）
            cipher_nums = encrypt_string(plain_text, e, n);
            cout << "密文是：";
            for (size_t i = 0; i < cipher_nums.size(); i++) {
                cout << cipher_nums[i];
                if (i != cipher_nums.size() - 1) cout << "  ";
            }
            cout << endl;
        }
        else if (choice == 2) {
            // 解密功能：输出明文（匹配截图）
            if (cipher_nums.empty()) {
                cout << "请先执行加密操作！" << endl;
                continue;
            }
            string decrypted_text = decrypt_string(cipher_nums, d, n);
            cout << "明文：" << decrypted_text << endl;
        }
        else if (choice == 3) {
            // 退出功能
            cout << "退出程序..." << endl;
            break;
        }
        else {
            cout << "输入错误！请选择1/2/3" << endl;
        }
    }

    return 0;
}
