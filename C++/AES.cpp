#include <iostream>
#include <iomanip>
#include <vector>
#include <array>
#include <cstdint>
#include <string>
using namespace std;

// AES S盒
static const uint8_t S_BOX[256] = {
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16};

// 轮常数
static const uint8_t RCON[10] = {
    0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36};

using State = array<array<uint8_t, 4>, 4>;

// GF(2^8) 乘法
uint8_t gmul(uint8_t a, uint8_t b)
{
    uint8_t p = 0;
    for (int i = 0; i < 8; ++i)
    {
        if (b & 1)
            p ^= a;
        bool highBit = a & 0x80;
        a <<= 1;
        if (highBit)
            a ^= 0x1B;
        b >>= 1;
    }
    return p;
}

// 16字节 -> 状态矩阵（按列优先）
State bytesToState(const array<uint8_t, 16> &input)
{
    State state{};
    int idx = 0;
    for (int col = 0; col < 4; ++col)
    {
        for (int row = 0; row < 4; ++row)
        {
            state[row][col] = input[idx++];
        }
    }
    return state;
}

void printKeyBlock(const array<uint8_t, 16> &data)
{
    for (int row = 0; row < 4; ++row)
    {
        for (int col = 0; col < 4; ++col)
        {
            int idx = row * 4 + col;
            cout << uppercase << hex << setw(2) << setfill('0') << (int)data[idx];
        }
        cout << endl;
    }
    cout << nouppercase << dec << endl;
}

void printRoundKeys(const vector<array<uint8_t, 16>> &roundKeys)
{
    for (size_t round = 1; round < roundKeys.size(); ++round)
    {
        const auto &rk = roundKeys[round];
        for (int word = 0; word < 4; ++word)
        {
            for (int byte = 0; byte < 4; ++byte)
            {
                int idx = word * 4 + byte;
                cout << uppercase << hex << setw(2) << setfill('0') << (int)rk[idx];
            }
            if (word != 3)
                cout << ' ';
        }
        cout << endl;
    }
    cout << nouppercase << dec << endl;
}

// 状态矩阵 -> 16字节
array<uint8_t, 16> stateToBytes(const State &state)
{
    array<uint8_t, 16> output{};
    int idx = 0;
    for (int col = 0; col < 4; ++col)
    {
        for (int row = 0; row < 4; ++row)
        {
            output[idx++] = state[row][col];
        }
    }
    return output;
}

void printState(const State &state, const string &tag)
{
    cout << tag << endl;
    for (int i = 0; i < 4; ++i)
    {
        for (int j = 0; j < 4; ++j)
        {
            cout << hex << setw(2) << setfill('0') << (int)state[i][j] << " ";
        }
        cout << endl;
    }
    cout << dec << endl;
}

// 字节代换
void subBytes(State &state)
{
    for (int i = 0; i < 4; ++i)
    {
        for (int j = 0; j < 4; ++j)
        {
            state[i][j] = S_BOX[state[i][j]];
        }
    }
}

// 行移位
void shiftRows(State &state)
{
    for (int row = 1; row < 4; ++row)
    {
        array<uint8_t, 4> temp = state[row];
        for (int col = 0; col < 4; ++col)
        {
            state[row][col] = temp[(col + row) % 4];
        }
    }
}

// 列混淆
void mixColumns(State &state)
{
    for (int col = 0; col < 4; ++col)
    {
        uint8_t a0 = state[0][col];
        uint8_t a1 = state[1][col];
        uint8_t a2 = state[2][col];
        uint8_t a3 = state[3][col];

        state[0][col] = gmul(a0, 0x02) ^ gmul(a1, 0x03) ^ a2 ^ a3;
        state[1][col] = a0 ^ gmul(a1, 0x02) ^ gmul(a2, 0x03) ^ a3;
        state[2][col] = a0 ^ a1 ^ gmul(a2, 0x02) ^ gmul(a3, 0x03);
        state[3][col] = gmul(a0, 0x03) ^ a1 ^ a2 ^ gmul(a3, 0x02);
    }
}

// 轮密钥加
void addRoundKey(State &state, const array<uint8_t, 16> &roundKey)
{
    int idx = 0;
    for (int col = 0; col < 4; ++col)
    {
        for (int row = 0; row < 4; ++row)
        {
            state[row][col] ^= roundKey[idx++];
        }
    }
}

array<uint8_t, 4> rotWord(array<uint8_t, 4> word)
{
    return {word[1], word[2], word[3], word[0]};
}

array<uint8_t, 4> subWord(array<uint8_t, 4> word)
{
    for (auto &b : word)
    {
        b = S_BOX[b];
    }
    return word;
}

// 密钥扩展
vector<array<uint8_t, 16>> keyExpansion(const array<uint8_t, 16> &key)
{
    vector<array<uint8_t, 4>> w(44);

    for (int i = 0; i < 4; ++i)
    {
        for (int j = 0; j < 4; ++j)
        {
            w[i][j] = key[4 * i + j];
        }
    }

    for (int i = 4; i < 44; ++i)
    {
        array<uint8_t, 4> temp = w[i - 1];
        if (i % 4 == 0)
        {
            temp = subWord(rotWord(temp));
            temp[0] ^= RCON[i / 4 - 1];
        }
        for (int j = 0; j < 4; ++j)
        {
            w[i][j] = w[i - 4][j] ^ temp[j];
        }
    }

    vector<array<uint8_t, 16>> roundKeys(11);
    for (int round = 0; round <= 10; ++round)
    {
        int idx = 0;
        for (int col = 0; col < 4; ++col)
        {
            for (int row = 0; row < 4; ++row)
            {
                roundKeys[round][idx++] = w[4 * round + col][row];
            }
        }
    }
    return roundKeys;
}

// AES-128 加密函数
array<uint8_t, 16> aesEncrypt(const array<uint8_t, 16> &plaintext,
                              const array<uint8_t, 16> &key)
{
    State state = bytesToState(plaintext);
    vector<array<uint8_t, 16>> roundKeys = keyExpansion(key);

    addRoundKey(state, roundKeys[0]);

    for (int round = 1; round <= 9; ++round)
    {
        subBytes(state);
        shiftRows(state);
        mixColumns(state);
        addRoundKey(state, roundKeys[round]);
    }

    subBytes(state);
    shiftRows(state);
    addRoundKey(state, roundKeys[10]);

    return stateToBytes(state);
}

void printHex(const array<uint8_t, 16> &data, const string &tag)
{
    cout << tag;
    for (auto b : data)
    {
        cout << ' ' << uppercase << hex << setw(2) << setfill('0') << (int)b;
    }
    cout << dec << endl;
}

int main()
{
    string keyStr = "A1B2C3D4E5F6G7H8";
    string ptStr = "HELLO WORLD!lsq";

    array<uint8_t, 16> key{};
    array<uint8_t, 16> plaintext{};

    for (int i = 0; i < 16; ++i)
    {
        key[i] = static_cast<uint8_t>(keyStr[i]);
        plaintext[i] = static_cast<uint8_t>(ptStr[i]);
    }

    printKeyBlock(key);

    vector<array<uint8_t, 16>> roundKeys = keyExpansion(key);
    printRoundKeys(roundKeys);

    cout << "明文：" << endl;
    cout << ptStr << endl;

    array<uint8_t, 16> ciphertext = aesEncrypt(plaintext, key);

    cout << "密文：" << endl;
    printHex(ciphertext, "data[16]:");

    return 0;
}
