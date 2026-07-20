#include <iostream>
#include <iomanip>
#include <sstream>
#include <cstring>
#include <cstdint>

using namespace std;

// ==================== SHA-3 (Keccak) 实现 ====================

// Keccak-f[1600] 轮常数
const uint64_t RC[24] = {
    0x0000000000000001ULL, 0x0000000000008082ULL, 0x800000000000808aULL,
    0x8000000080008000ULL, 0x000000000000808bULL, 0x0000000080000001ULL,
    0x8000000080008081ULL, 0x8000000000008009ULL, 0x000000000000008aULL,
    0x0000000000000088ULL, 0x0000000080008009ULL, 0x000000008000000aULL,
    0x000000008000808bULL, 0x800000000000008bULL, 0x8000000000008089ULL,
    0x8000000000008003ULL, 0x8000000000008002ULL, 0x8000000000000080ULL,
    0x000000000000800aULL, 0x800000008000000aULL, 0x8000000080008081ULL,
    0x8000000000008080ULL, 0x0000000080000001ULL, 0x8000000080008008ULL};

// 旋转左移
static inline uint64_t rotl64(uint64_t x, unsigned int n)
{
    return (x << n) | (x >> (64 - n));
}

// Keccak-f[1600] 置换函数
void keccak_f(uint64_t state[25])
{
    for (int round = 0; round < 24; round++)
    {
        // Theta 步骤
        uint64_t C[5], D[5];
        for (int x = 0; x < 5; x++)
        {
            C[x] = state[x] ^ state[x + 5] ^ state[x + 10] ^ state[x + 15] ^ state[x + 20];
        }
        for (int x = 0; x < 5; x++)
        {
            D[x] = C[(x + 4) % 5] ^ rotl64(C[(x + 1) % 5], 1);
        }
        for (int x = 0; x < 5; x++)
        {
            for (int y = 0; y < 5; y++)
            {
                state[x + 5 * y] ^= D[x];
            }
        }

        // Rho 和 Pi 步骤
        int x = 1, y = 0;
        uint64_t current = state[1];
        for (int t = 0; t < 24; t++)
        {
            int newX = y;
            int newY = (2 * x + 3 * y) % 5;
            uint64_t temp = state[newX + 5 * newY];
            state[newX + 5 * newY] = rotl64(current, ((t + 1) * (t + 2) / 2) % 64);
            current = temp;
            x = newX;
            y = newY;
        }

        // Chi 步骤
        for (int y = 0; y < 5; y++)
        {
            uint64_t T[5];
            for (int x = 0; x < 5; x++)
            {
                T[x] = state[x + 5 * y];
            }
            for (int x = 0; x < 5; x++)
            {
                state[x + 5 * y] = T[x] ^ ((~T[(x + 1) % 5]) & T[(x + 2) % 5]);
            }
        }

        // Iota 步骤
        state[0] ^= RC[round];
    }
}

// SHA3-256 实现 (输出 256 位 = 32 字节)
class SHA3_256
{
public:
    static const int HASH_SIZE = 32;
    static const int RATE = 136; // 1600 - 2*256 = 1088 位 = 136 字节

    void init()
    {
        memset(state, 0, sizeof(state));
        rateBits = 0;
    }

    void update(const uint8_t *data, size_t len)
    {
        while (len > 0)
        {
            size_t chunk = min(len, (size_t)(RATE - rateBits / 8));
            for (size_t i = 0; i < chunk; i++)
            {
                state[(rateBits / 8 + i) / 8] ^= (uint64_t)data[i] << (8 * ((rateBits / 8 + i) % 8));
            }
            rateBits += chunk * 8;
            data += chunk;
            len -= chunk;

            if (rateBits == RATE * 8)
            {
                keccak_f(state);
                rateBits = 0;
            }
        }
    }

    void final(uint8_t hash[HASH_SIZE])
    {
        // 添加填充
        size_t padIndex = rateBits / 8;
        state[padIndex / 8] ^= (uint64_t)0x06 << (8 * (padIndex % 8));
        state[(RATE - 1) / 8] ^= (uint64_t)0x80 << (8 * ((RATE - 1) % 8));

        keccak_f(state);

        // 输出哈希值
        for (int i = 0; i < HASH_SIZE; i++)
        {
            hash[i] = (state[i / 8] >> (8 * (i % 8))) & 0xFF;
        }
    }

private:
    uint64_t state[25];
    size_t rateBits;
};

// ==================== HMAC-SHA3-256 实现 ====================

class HMAC_SHA3_256
{
public:
    static const int BLOCK_SIZE = 136; // SHA3-256 的 rate
    static const int HASH_SIZE = 32;

    void init(const uint8_t *key, size_t keyLen)
    {
        uint8_t k_ipad[BLOCK_SIZE];
        uint8_t k_opad[BLOCK_SIZE];

        // 如果密钥太长，先进行哈希
        uint8_t keyHash[HASH_SIZE];
        if (keyLen > BLOCK_SIZE)
        {
            SHA3_256 sha3;
            sha3.init();
            sha3.update(key, keyLen);
            sha3.final(keyHash);
            key = keyHash;
            keyLen = HASH_SIZE;
        }

        // 创建 ipad 和 opad
        memset(k_ipad, 0x36, BLOCK_SIZE);
        memset(k_opad, 0x5c, BLOCK_SIZE);

        for (size_t i = 0; i < keyLen; i++)
        {
            k_ipad[i] ^= key[i];
            k_opad[i] ^= key[i];
        }

        // 保存 opad 用于最终计算
        memcpy(this->k_opad, k_opad, BLOCK_SIZE);

        // 初始化内部哈希
        inner.init();
        inner.update(k_ipad, BLOCK_SIZE);
    }

    void update(const uint8_t *data, size_t len)
    {
        inner.update(data, len);
    }

    void final(uint8_t hmac[HASH_SIZE])
    {
        uint8_t innerHash[HASH_SIZE];
        inner.final(innerHash);

        SHA3_256 outer;
        outer.init();
        outer.update(k_opad, BLOCK_SIZE);
        outer.update(innerHash, HASH_SIZE);
        outer.final(hmac);
    }

private:
    SHA3_256 inner;
    uint8_t k_opad[BLOCK_SIZE];
};

// ==================== 辅助函数 ====================

// 将字节数组转换为十六进制字符串
string toHex(const uint8_t *data, size_t len)
{
    stringstream ss;
    ss << hex << setfill('0');
    for (size_t i = 0; i < len; i++)
    {
        ss << setw(2) << (int)data[i];
    }
    return ss.str();
}

// ==================== 主程序 ====================

int main()
{
    // 消息和密钥
    const char *message = "Hello,IoT!";
    const char *key = "secret_key";

    cout << "Message: " << message << endl;

    // 计算发送方的 HMAC
    uint8_t hmacSender[32];
    HMAC_SHA3_256 hmac;
    hmac.init((const uint8_t *)key, strlen(key));
    hmac.update((const uint8_t *)message, strlen(message));
    hmac.final(hmacSender);

    cout << "发送生成的HMAC: " << toHex(hmacSender, 32) << endl;

    // 模拟接收方收到不同的 HMAC（篡改或错误的情况）
    const char *fakeKey = "secret_key"; // attacker_fake_key
    uint8_t hmacReceiver[32];
    HMAC_SHA3_256 hmac2;
    hmac2.init((const uint8_t *)fakeKey, strlen(fakeKey));
    hmac2.update((const uint8_t *)message, strlen(message));
    hmac2.final(hmacReceiver);

    cout << "接受的HMAC: " << toHex(hmacReceiver, 32) << endl;

    // 验证 HMAC
    bool authentic = (memcmp(hmacSender, hmacReceiver, 32) == 0);

    if (authentic)
    {
        cout << "Message is authentic." << endl;
    }
    else
    {
        cout << "Message is not authentic." << endl;
    }

    return 0;
}
