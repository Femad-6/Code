import os
import sys

a = [0]*128
b = [0]*128
str1 = input()
str2 = input()

for i in range(len(str1)):
    a[ord(str1[i])] += 1

for i in range(len(str2)):
    b[ord(str2[i])] += 1

for i in range(128):
    if a[i]!= b[i]:
        print("No")
        sys.exit()

print("Yes")