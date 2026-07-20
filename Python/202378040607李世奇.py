def rc4_ksa(key):
    # 1. 初始化S盒，0-255线性填充
    S = list(range(256))
    key_len = len(key)
    j = 0
    # 2. 生成T表并对S盒进行置换，T表通过密钥循环填充实现，无需显式定义
    for i in range(256):
        # T[i]等价于key[i % key_len]，直接计算避免额外空间开销
        j = (j + S[i] + key[i % key_len]) % 256
        # 交换S[i]和S[j]
        S[i], S[j] = S[j], S[i]
    return S


def rc4_prga(S, plaintext_len):
    i = 0
    j = 0
    keystream = []
    for _ in range(plaintext_len):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        t = (S[i] + S[j]) % 256
        keystream.append(S[t])
    return keystream


def rc4_encrypt_decrypt(plaintext, key):
    S = rc4_ksa(key)
    keystream = rc4_prga(S, len(plaintext))
    result = bytes([p ^ k for p, k in zip(plaintext, keystream)])
    return result


if __name__ == "__main__":
    plaintext = b"Hello,World!lishiqi"
    key = b"SecretKey"

    # 加密操作
    ciphertext = rc4_encrypt_decrypt(plaintext, key)
    # 解密操作
    decrypted_text = rc4_encrypt_decrypt(ciphertext, key)

    print(f"原始明文：{plaintext.decode('utf-8')}")
    print(f"使用密钥：{key.decode('utf-8')}")
    print(f"加密后的密文（十六进制）：{ciphertext.hex()}")
    print(f"解密后的内容：{decrypted_text.decode('utf-8')}")
