
n,m=map(int,input().split())
s1=input()
s2=input()
l=len(s1)
same=0
for i in range(l):
  if s1[i]==s2[i]:
    same+=1

if m>same:
    ans=n-(m-same)
else:
    ans=n-(same-m)
ans=ans if ans < n else n
print(ans)
#17  3  10    