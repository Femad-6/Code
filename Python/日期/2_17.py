from datetime import *
a=date(1949,10,1)
b=date(2012,10,1)
cnt=0
print(a)
while a<b:
    if a.weekday()==6 and a.month==10 and a.day==1:
        cnt+=1
    a+=timedelta(1)
print(cnt)