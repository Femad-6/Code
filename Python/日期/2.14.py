a,b=map(int,input().split())
mid=(a+b)//2
min_=min(a,b)
ans=float('inf')
for i in range(min_+1):
    ans=min(ans,abs(a+b-4*i))
print(ans)
