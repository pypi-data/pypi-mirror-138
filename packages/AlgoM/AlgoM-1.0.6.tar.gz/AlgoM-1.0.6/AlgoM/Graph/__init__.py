#Adjacency list, undirected, weighted
from heapq import heappop as pop, heappush as push
class Graph:
    def __init__(self, n, adj):
        self.n = n 
        self.adj = adj


    #Djikstra
    def distance(self, s, e):
        self.vis = set()
        self.dist = [10**18]*self.n
        q = []
        self.dist[s] = 0
        push(q, (0, 0))
        while len(q) > 0:
            d, u = pop(q)
            if u in self.vis:
                continue
            self.vis.add(u)
            for v, w in self.adj[u]:
                new_dist = self.dist[u] + w
                if new_dist < self.dist[v]:
                    self.dist[v] = new_dist
                    push(q, (self.dist[v], v))
        return self.dist[e]


#----------------------------------------


#Adjacency list, directed, unweighted
class Graph2:
    def __init__(self, n, adj):
        self.n = n 
        self.adj = adj
        

    #Strongly connected components
    def scc(self):
      self.vis = [False] * self.n
      self.stack = []
      self.visited = [False] * self.n
      self.connected = []
      for i in range(self.n):
        if not self.visited[i]:
          self.fillOrder(i)
      
      curr = -1
      while self.stack:
        i = self.stack.pop()
        if not self.vis[i]:
          self.connected.append([])
          curr += 1
          self.DFS(i, curr)

      return self.connected

    def dfss(self, v, curr):
      self.vis[v] = True
      self.connected[curr].append(v)
      for i in self.adj[v]:
        if not self.vis[i]:
          self.dfss(i,curr)

    def fillOrder(self, v):
      self.visited[v] = True
      for i in self.adj[v]:
        if not self.visited[i]:
          self.fillOrder(i)
      self.stack.append(v)


    #Topological sort
    def topological_sort(self):
      self.vis = [False for _ in range(self.n)]
      self.ans = []
      for node in range(self.n):
        if not self.vis[node]:
          self.dfst(node)
      self.ans.reverse()
      return self.ans
      
    def dfst(self, node):
      self.vis[node] = True
      for neigh in self.adj[node]:
        if self.vis[neigh] == False:
          self.dfst(neigh)
      self.ans.append(node)


    #Detect cycle 
    def cyclic(self):
      self.vis = [False for _ in range(self.n)]
      self.stack = [False for _ in range(self.n)]
      for node in range(self.n):
        if self.vis[node] == False:
          if self.cycle(node):
            return True
      return False

    def cycle(self, v):
      self.visited[v] = True
      self.recStack[v] = True
      for neighbour in self.adj[v]:
        if self.vis[neighbour] == False:
          if self.cycle(neighbour):
            return True
          elif self.stack[neighbour] == True:
            return True

      self.stack[v] = False
      return False



#----------------------------------------

#Adjacency list, undirected, unweighted
#class Graph3:




#----------------------------------------


#Adjacency list, directed, weighted
#class Graph4:




#----------------------------------------

#adjacency matrix 
class Graph5:
    def __init__(self, n, adj):   
        self.adj = adj
        self.ans = [[float("inf") for _ in range(n)] for _ in range(n)]
        self.floyd_warshall()

    #Floyd Warshall
    def floyd_warshall(self):
        for k in range(self.n):
            for i in range(self.n):
                for j in range(self.n):
                  self.ans[i][j] = min(self.ans[i][j], self.adj[i][k] + self.adj[k][j])
    def dist(self, x, y):
      return self.ans[x][y]



#----------------------------------------




"""
#Find articulation points/bridges
n, m = map(int, input().split())
low = [0 for _ in range(n)]
num = [-1 for _ in range(n)]
graph = [[] for _ in range(n)]
c = 0
root = 0
root_children = 0
ans = [0 for _ in range(n)]
parent = [0] * n
bridges = []
def find(node):
  global c
  global root_children
  num[node] = c
  c += 1
  low[node] = num[node]
  for neigh in graph[node]:
    if num[neigh] == -1:
      parent[neigh] = node
      if node == root:
        root_children += 1
      find(neigh)
      if low[neigh] >= low[node]:
        ans[node] = 1
    #for bridges
      if low[neigh] > low[node]:
        bridges.append([node, neigh])
      low[node] = min(low[node], low[neigh])
    elif neigh != parent[node]:
      low[node] = min(low[u], num[neigh])


for _ in range(m):
  a, b = map(int, input().split())
  graph[a].append(b)

for u in range(n):
  if num[u] == -1:
    root = u
    root_children = 0
    find(root)
    ans[root] = (root_children > 1)

for i, j in enumerate(ans):
  if j:
    print(i)



#Min-cut (Dinic's algorithm)
from collections import deque
n, m = map(int, input().split())
graph = [[0 for _ in range(n)] for _ in range(n)]
org_graph = [[0 for _ in range(n)] for _ in range(n)]
for edge in range(m):
  a, b, c = map(int, input().split())
  graph[a-1][b-1] = c
  org_graph[a-1][b-1] = c

ans = []
def BFS(s, t, parent): 
  visited = [False] *(n) 
  queue= deque()
  queue.append(s) 
  visited[s] = True
  while queue: 
    u = queue.pop() 
    for ind, val in enumerate(graph[u]): 
      if visited[ind] == False and val > 0 : 
        queue.appendleft(ind) 
        visited[ind] = True
        parent[ind] = u 
  
  return True if visited[t] else False

def dfs(graph,s,visited):
  visited[s] = True
  for i in range(len(graph)):
    if graph[s][i]>0 and not visited[i]:
      dfs(graph,i,visited)
  
def minCut(source, sink): 
  global ans
  parent = [-1]*(n) 
  max_flow = 0 # There is no flow initially 
  while BFS(source, sink, parent) : 
    path_flow = float("inf") 
    s = sink 
    while(s != source): 
      path_flow = min(path_flow, graph[parent[s]][s]) 
      s = parent[s] 
      max_flow += path_flow 
      v = sink 
    while(v != source): 
      u = parent[v] 
      graph[u][v] -= path_flow 
      graph[v][u] += path_flow 
      v = parent[v] 
  
  visited = n * [False]
  dfs(graph,source,visited)
 
  for i in range(n): 
    for j in range(n): 
      if graph[i][j] == 0 and org_graph[i][j] > 0 and visited[i]: 
        ans.append([i, j])

minCut(0, n-1)
print(ans)
"""