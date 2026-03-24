from collections import deque

def bfs(start, graph,n):
  dist=[-1]*(n+1)
  dist[start]=0
  far=start
  q=deque([start])
  while q:
    a=q.popleft()
    for y in graph[a]:
      if dist[y]==-1:
        dist[y]=dist[a]+1
        q.append(y)
        if dist[y]>dist[far]:
          far=y
  return far,dist[far]

def solve():
  n=int(input())
  graph=[[] for _ in range(n+1)]
  for i in range(n-1):

    u,v=map(int,input().split())
    graph[u].append(v)
    graph[v].append(u)
  s,_=bfs(1,graph,n)
  _,d=bfs(s,graph,n)
  print(d-d%2)


if __name__=="__main__":
  solve()