T=int(input())
for i in range (T):
  n,m=map(int,input().split())
  ans=m*(m+1)//2

  print(int((ans+1)%n))