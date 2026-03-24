def solve():
    L=int(input())
    l,h=1,2*10**9
    while l<h:
        m=(l+h)//2
        S=m*(m+1)//2
        if S>=L*2:
            h=m
        else:
            l=m+1

    x=l
    S=x*(x+1)//2
    if (S-L)%2==0:
        print(x)
    else:
        if (x+1)%2==1:
            print(x+1)
        else:
            print(x+2)