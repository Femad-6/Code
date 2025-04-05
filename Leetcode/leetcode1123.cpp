#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
using namespace std;

struct TreeNode
{
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode() : val(0), left(nullptr), right(nullptr) {}
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
    TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
};

class Solution
{
public:
    int depth(TreeNode *root)
    {
        if (root == nullptr)
        {
            return 0;
        }
        else
        {
            return 1 + max(depth(root->left), depth(root->right));
        }
    }
    TreeNode *lcaDeepestLeaves(TreeNode *root)
    {
        if (root == nullptr)
        {
            return nullptr;
        }
        int leftDepth = depth(root->left);
        int rightDepth = depth(root->right);
        if (leftDepth == rightDepth)
        {
            return root;
        }
        if (leftDepth > rightDepth)
        {
            return lcaDeepestLeaves(root->left);
        }
        else
        {
            return lcaDeepestLeaves(root->right);
        }
        return nullptr;
    }
};
int main()
{

    Solution s;
    TreeNode *root = new TreeNode(1);
    root->left = new TreeNode(2);
    root->right = new TreeNode(3);
    root->left->left = new TreeNode(4);
    root->left->right = new TreeNode(5);
    root->right->left = new TreeNode(6);
    root->right->right = new TreeNode(7);
    root->left->left->left = new TreeNode(8);
    TreeNode *result = s.lcaDeepestLeaves(root);
    cout << result->val << endl; // 输出结果
    return 0;
}