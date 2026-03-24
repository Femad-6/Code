#include<vector>
#include<string>
#include<iostream>
using namespace std;
class Solution {
    public:
        vector<vector<string>> res;
        vector<string> path;
        bool isPalindrome(string s,int start,int end) {
            for(int i=start,j=end;i<j;i++,j--) {
                if(s[i]!=s[j]) {
                    return false;
                }
            }
            return true;
        }
        void backtracking(string s,int startIndex) {
            // 终止条件：起始位置超出字符串长度
            if(startIndex>=s.size()) {
                res.push_back(path);
                return;
            }
            // 遍历所有可能的结束位置
            for(int i=startIndex;i<s.size();i++) {
                if(isPalindrome(s,startIndex,i)) {  // 判断子串是否是回文
                    string str=s.substr(startIndex,i-startIndex+1);
                    path.push_back(str);  // 记录当前回文子串
                } 
                else {
                    continue;  // 非回文直接跳过
                }
                
                backtracking(s,i+1);  // 
                path.pop_back();      // 回溯，移除当前子串
            } 
        }
        vector<vector<string>> partition(string s) {
            backtracking(s,0);
            return res;
            
        }
    };
int main() {
    Solution s;
    vector<vector<string>> res;
    res=s.partition("aab");
    for(int i=0;i<res.size();i++) {
        for(int j=0;j<res[i].size();j++) {
            cout<<res[i][j]<<" ";
        }
        cout<<endl;
    }
    return 0; 
}