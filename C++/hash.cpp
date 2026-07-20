/******************************************************************************
 * 实验名称：基于哈希函数的RFID标签认证系统
 * 实验目的：模拟物联网中RFID标签与读写器的认证过程
 * 方案描述：
 *   本方案采用简单的哈希取模算法实现RFID标签的快速认证。
 *   系统包含三个核心组件：
 *   1. RFID标签（ElecTag）：存储标签ID和哈希值metalID
 *   2. 后台数据库（DataBase）：存储所有合法标签的信息
 *   3. 读写器（Reader）：负责标签检测、数据库查询和身份验证
 *
 *   认证流程：
 *   步骤1：读写器检测标签，获取标签的metalID
 *   步骤2：读写器在数据库中查找匹配的metalID
 *   步骤3：验证标签的hash(key)是否等于metalID
 *   步骤4：确认标签ID与数据库记录一致
 *
 *   模拟三种情况：
 *   ① 成功解锁：标签合法且信息完整正确
 *   ② 标签不存在：标签的metalID在数据库中找不到（可能标签被篡改或伪造）
 *   ③ 数据库不匹配：找到记录但验证失败（可能数据库记录被篡改）
 ******************************************************************************/

#include <stdio.h>
#include <math.h>
#include <time.h>
#include <stdlib.h>
#include <string.h>

#define Tag_N 3       // 合法标签数量（不少于3个）
#define Data_N 8      // 数据库记录数量（不少于5个）
#define Hash_core 17  // 哈希模数

// RFID电子标签结构
struct ElecTag
{
    int ID;       // 标签唯一标识号
    int metalID;  // 标签的哈希值（由key经hash函数计算得到）
};

// 后台数据库记录结构
struct DataBase
{
    int ID;       // 标签ID
    int metalID;  // 哈希值（用于快速匹配）
    int key;      // 原始密钥（用于验证标签真实性）
};

ElecTag tag[Tag_N];      // 标签数组
DataBase Data[Data_N];   // 数据库数组

// ==================== 核心算法：哈希函数 ====================
/**
 * 哈希函数：将密钥映射到固定范围
 * 算法：简单取模运算 hash(key) = key % Hash_core
 * 作用：快速定位，减少数据库搜索范围
 */
int hash(int key)
{
    return key % Hash_core;
}

// ==================== 初始化函数 ====================
/**
 * 初始化系统：
 * 1. 生成3个合法标签，并在数据库中注册
 * 2. 生成额外的数据库记录（模拟其他合法标签）
 * 3. 设置随机种子
 */
void Init()
{
    srand((unsigned)time(NULL));

    // 生成3个合法RFID标签，并同步写入数据库
    for (int i = 0; i < Tag_N; i++)
    {
        int key = rand();                          // 随机生成密钥
        tag[i].metalID = hash(key);                // 计算哈希值
        int id_val = rand();
        while (id_val == 0)
        {
            id_val = rand();                       // 确保ID不为0
        }
        tag[i].ID = id_val;                        // 设置标签ID

        // 在数据库中注册该合法标签
        Data[i].ID = id_val;
        Data[i].metalID = tag[i].metalID;
        Data[i].key = key;                         // 保存原始密钥用于验证
    }

    // 生成额外的数据库记录（模拟系统中其他合法但不在场的标签）
    for (int i = Tag_N; i < Data_N - 2; i++)
    {
        int key = rand();
        Data[i].ID = rand();
        Data[i].metalID = hash(key);
        Data[i].key = key;
    }

    // 生成2条异常记录（模拟被篡改的数据库记录）
    for (int i = Data_N - 2; i < Data_N; i++)
    {
        Data[i].ID = rand();
        Data[i].metalID = rand();      // 随机metalID，与任何标签都不匹配
        Data[i].key = rand();          // 随机key，无法通过验证
    }
}

// ==================== 显示函数 ====================
/**
 * 显示数据库和标签的当前状态
 */
void display()
{
    printf("================= 后台数据库列表 =================\n");
    printf("序号\tMetaID\t\tID\t\tKey\n");
    printf("------------------------------------------------\n");
    for (int i = 0; i < Data_N; i++)
    {
        printf("[%d]\t%d\t\t%d\t\t%d\n", i, Data[i].metalID, Data[i].ID, Data[i].key);
    }
    printf("\n================= RFID标签列表 =================\n");
    printf("序号\tMetalID\t\tID\n");
    printf("------------------------------------------------\n");
    for (int i = 0; i < Tag_N; i++)
    {
        printf("[%d]\t%d\t\t%d\n", i, tag[i].metalID, tag[i].ID);
    }
    printf("\n");
}

// ==================== 核心功能函数 ====================

/**
 * 步骤1：读写器检测标签
 * 模拟RFID读写器感知到标签信号，获取标签的metalID
 */
int Query(ElecTag *tag)
{
    printf("\n【步骤1】读写器检测标签...\n");
    printf("  -> 检测到标签信号，获取metalID = %d\n", tag->metalID);
    return tag->metalID;
}

/**
 * 步骤2：在数据库中查找匹配记录
 * 根据metalID搜索数据库，返回匹配的记录
 * 情况②：如果找不到匹配记录，说明标签不存在（可能被篡改或伪造）
 */
DataBase GetData(int RmetalID, int *found)
{
    printf("\n【步骤2】在数据库中查找metalID = %d...\n", RmetalID);
    for (int i = 0; i < Data_N; i++)
    {
        if (RmetalID == Data[i].metalID)
        {
            printf("  -> 找到匹配记录！数据库索引[%d]\n", i);
            *found = 1;
            return Data[i];
        }
    }
    printf("  -> 【失败】数据库中未找到匹配的metalID！\n");
    printf("  -> 原因：标签不存在或标签信息被篡改！\n");
    *found = 0;
    DataBase d = {-1, -1, -1};
    return d;
}

/**
 * 步骤3：验证标签真实性
 * 使用数据库中的key重新计算hash，验证是否等于metalID
 * 情况③：如果验证失败，说明数据库记录与标签不匹配（可能数据库被篡改）
 */
int GetTagID(DataBase *RevData, ElecTag *tag, int *auth_success)
{
    printf("\n【步骤3】验证标签真实性...\n");
    printf("  -> 数据库key = %d, 计算hash(%d) = %d\n", 
           RevData->key, RevData->key, hash(RevData->key));
    printf("  -> 标签metalID = %d\n", tag->metalID);

    if (hash(RevData->key) == tag->metalID)
    {
        printf("  -> 哈希验证通过！标签认证成功！\n");
        *auth_success = 1;
        return tag->ID;
    }
    else
    {
        printf("  -> 【失败】哈希验证不通过！\n");
        printf("  -> 原因：数据库记录与标签不匹配，可能数据库被篡改！\n");
        *auth_success = 0;
        return 0;
    }
}

/**
 * 步骤4：最终确认标签身份
 * 比对数据库中的ID与标签ID是否一致
 */
void ReaderVer(int RevDataID, int TagID, int auth_success)
{
    printf("\n【步骤4】最终身份确认...\n");
    if (!auth_success)
    {
        printf("  -> 【认证失败】标签无法解锁！\n");
        return;
    }

    if (RevDataID == TagID && TagID != 0)
    {
        printf("  -> ID比对成功！数据库ID = %d, 标签ID = %d\n", RevDataID, TagID);
        printf("  -> 【认证成功】标签解锁！\n");
    }
    else
    {
        printf("  -> 【失败】ID不匹配！数据库ID = %d, 标签ID = %d\n", RevDataID, TagID);
        printf("  -> 标签解锁失败！\n");
    }
}

// ==================== 三种情况模拟函数 ====================

/**
 * 情况①：成功解锁标签
 * 使用合法的、未篡改的标签进行认证
 */
void case1_success()
{
    printf("\n╔══════════════════════════════════════════════════════════════╗\n");
    printf("║  情况①：成功解锁标签（合法标签，信息完整正确）                ║\n");
    printf("╚══════════════════════════════════════════════════════════════╝\n");

    int rand_tag = rand() % Tag_N;  // 随机选择一个合法标签
    int found = 0, auth_success = 0;

    int RmetalID = Query(&tag[rand_tag]);
    DataBase RevData = GetData(RmetalID, &found);

    if (!found)
    {
        printf("\n【结果】认证失败：标签不存在！\n");
        return;
    }

    int RevID = GetTagID(&RevData, &tag[rand_tag], &auth_success);
    ReaderVer(RevData.ID, RevID, auth_success);
}

/**
 * 情况②：感知器搜索标签不存在
 * 模拟标签被篡改，metalID在数据库中找不到
 */
void case2_tag_not_found()
{
    printf("\n╔══════════════════════════════════════════════════════════════╗\n");
    printf("║  情况②：标签不存在（标签信息被篡改，metalID无法匹配）        ║\n");
    printf("╚══════════════════════════════════════════════════════════════╝\n");

    // 创建一个伪造的标签（metalID与数据库中任何记录都不匹配）
    ElecTag fake_tag;
    fake_tag.ID = 99999;
    fake_tag.metalID = 999;  // 确保这个metalID不在数据库中

    int found = 0, auth_success = 0;

    int RmetalID = Query(&fake_tag);
    DataBase RevData = GetData(RmetalID, &found);

    if (!found)
    {
        printf("\n【结果】认证失败：标签不存在或已被篡改！\n");
        printf("  -> 可能原因：\n");
        printf("     1. 标签是伪造的\n");
        printf("     2. 标签的metalID被篡改\n");
        printf("     3. 标签未在系统中注册\n");
        return;
    }

    int RevID = GetTagID(&RevData, &fake_tag, &auth_success);
    ReaderVer(RevData.ID, RevID, auth_success);
}

/**
 * 情况③：数据库不匹配
 * 模拟数据库记录被篡改，导致验证失败
 */
void case3_database_mismatch()
{
    printf("\n╔══════════════════════════════════════════════════════════════╗\n");
    printf("║  情况③：数据库不匹配（数据库记录被篡改，验证失败）            ║\n");
    printf("╚══════════════════════════════════════════════════════════════╝\n");

    // 修改一个合法标签的metalID，使其与数据库记录不匹配
    ElecTag modified_tag = tag[0];  // 复制第一个标签
    modified_tag.metalID = (tag[0].metalID + 1) % Hash_core;  // 篡改metalID

    printf("  -> 【模拟】标签metalID被篡改：%d -> %d\n", tag[0].metalID, modified_tag.metalID);

    int found = 0, auth_success = 0;

    int RmetalID = Query(&modified_tag);
    DataBase RevData = GetData(RmetalID, &found);

    if (!found)
    {
        printf("\n【结果】认证失败：标签不存在！\n");
        return;
    }

    int RevID = GetTagID(&RevData, &modified_tag, &auth_success);
    ReaderVer(RevData.ID, RevID, auth_success);
}

// ==================== 主函数 ====================

int main()
{
    printf("============================================================\n");
    printf("     RFID标签认证系统 - 基于哈希函数的物联网安全实验        \n");
    printf("============================================================\n\n");

    // 初始化系统
    Init();

    // 显示系统初始状态
    display();

    // 模拟三种情况
    case1_success();           // 情况①：成功解锁
    case2_tag_not_found();     // 情况②：标签不存在
    case3_database_mismatch(); // 情况③：数据库不匹配

    printf("\n============================================================\n");
    printf("     实验结束                                                \n");
    printf("============================================================\n");

    return 0;
}
