def qpow(a,b,mod):
  res=1
  while b:
    if b&1:
      res=res*a%mod
      a=a*a%mod
      b>>=1
  return res

ans=qpow(3,3,90)
print(ans)