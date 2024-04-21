# 计算机视觉学习笔记

np.array()	定义矩阵

```python
M = np.arange(1, 13).reshape((4, 3))
a = np.array([1, 1, 0]).reshape((1, 3))

print("M = ", M)
print("The size of M is: ", M.shape)
```

np.dot()	点积

```python
np.dot(a ,b)
```

zip()	将多个可迭代对象（如列表、元组等）中对应位置的元素打包成一个元组，并返回由这些元组组成的迭代器。这个迭代器可以用于遍历同时来自多个可迭代对象的元素。

```python
squared_diff = [(a - b) ** 2 for a, b in zip(u, v)]
```

[::-1]	切片操作，数组反转

```python
arr = [1, 2, 3, 4, 5]
reversed_arr = arr[::-1]
print(reversed_arr)
```

[:k]	切片操作，取数组的前 k 个元素

```python
arr = [1, 2, 3, 4, 5]
first_k_elements = arr[:3]
print(first_k_elements)
```

