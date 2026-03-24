from collections import deque

print("=" * 50)
print("例 1: 基本用法 - 双端队列的添加和移除")
print("=" * 50)

d = deque()
d.append('a')
d.append('b')
d.append('c')
print("append 后:", d)

d.appendleft('z')
print("appendleft 后:", d)

right = d.pop()
print("pop 出:", right)
print("pop 后:", d)

left = d.popleft()
print("popleft 出:", left)
print("popleft 后:", d)

print("\n" + "=" * 50)
print("例 2: 初始化 deque")
print("=" * 50)

d1 = deque([1, 2, 3])
print("从列表初始化:", d1)

d2 = deque(range(5))
print("从 range 初始化:", d2)

d3 = deque('hello')
print("从字符串初始化:", d3)

print("\n" + "=" * 50)
print("例 3: 固定大小的 deque（滑动窗口）")
print("=" * 50)

d = deque(maxlen=3)
for i in range(1, 6):
    d.append(i)
    print(f"添加 {i} 后:", d)

print("\n" + "=" * 50)
print("例 4: 队列基本操作（FIFO）")
print("=" * 50)

queue = deque()
queue.append('任务1')
queue.append('任务2')
queue.append('任务3')
print("队列:", queue)

print("处理:", queue.popleft())
print("处理:", queue.popleft())
print("剩余队列:", queue)

print("\n" + "=" * 50)
print("例 5: 栈操作（LIFO）")
print("=" * 50)

stack = deque()
stack.append('页面A')
stack.append('页面B')
stack.append('页面C')
print("栈:", stack)

print("返回:", stack.pop())
print("返回:", stack.pop())
print("剩余栈:", stack)

print("\n" + "=" * 50)
print("例 6: 旋转操作")
print("=" * 50)

d = deque([1, 2, 3, 4, 5])
print("原始:", d)

d.rotate(2)
print("向右旋转 2:", d)

d.rotate(-3)
print("向左旋转 3:", d)

print("\n" + "=" * 50)
print("例 7: 扩展 deque")
print("=" * 50)

d = deque([1, 2, 3])
d.extend([4, 5, 6])
print("extend 后:", d)

d.extendleft([0, -1, -2])
print("extendleft 后:", d)
