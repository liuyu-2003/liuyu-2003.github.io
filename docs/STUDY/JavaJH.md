# Java集合

集合由两大接口派生而来，Collection和Map。

Collection接口存放单一元素，下面有三个子接口：List、Set、Queue

Map接口存放键值对

![集合结构图](/Users/liuyu/noteBook/assets/Java集合结构图.png)

## List（顺序）

存储的元素是有序的、可重复的。

底层数据结构

- `ArrayList`：`Object[]` 数组。
- `LinkedList`：双向链表，性能不高通常不用

### ArrayList怎么线程不安全的

添加数据步骤如下：

1. 判断数组是否需要扩容，如果需要就扩容
2. 将数组的size位置设置为添加的数据
3. 集合大小size++

情况1:

**部分值为null**：当线程1走到了扩容那里发现当前size是9，而数组容量是10，所以不用扩容，这时候cpu让出执行权，线程2也进来了，发现size是9，而数组容量是10，所以不用扩容，这时候线程1继续执行，将数组下标索引为9的位置set值了，还没有来得及执行size++，这时候线程2也来执行了，又把数组下标索引为9的位置set了一遍，这时候两个先后进行size++，导致下标索引10的地方就为null了。

流程：线程a1，线程b1，a2，b2，a3，b3

结果：size=9的地方是线程b的值，且size=10的地方为null，下一次再add的话，会扩容，然后size=11

情况2:

**索引越界异常**：线程1走到扩容那里发现当前size是9，数组容量是10不用扩容，cpu让出执行权，线程2也发现不用扩容，这时候数组的容量就是10，而线程1 set完之后size++，这时候线程2再进来size就是10，数组的大小只有10，而你要设置下标索引为10的就会越界（数组的下标索引从0开始）。

流程：a1，b1，a2，a3，b2，b3

结果：size=9是a的值，size=10本来因为容量不够放不进去，需要扩容，但是没扩，所以数组越界了

情况3:

**size与我们add的数量不符：常见**，因为size++本身就不是原子操作，可以分为三步：获取size的值，将size的值加1，将新的size值覆盖掉原来的，线程1和线程2拿到一样的size值加完了同时覆盖，就会导致一次没有加上，所以肯定不会与我们add的数量保持一致的。

流程：a1，a2，b1，b2，（a3和b3同时）

结果：假设往size=4的地方加，总容量是10，size=4是b的值，然后size只加了1，size=5了，而应该size=6

### CopyonWriteArraylist

CopyOnWriteArrayList底层也是通过一个数组保存数据，使用volatile关键字修饰数组，保证当前线程对数组对象重新赋值后，其他线程可以及时感知到。

在写入操作时，加了一把互斥锁ReentrantLock以保证线程安全。
首先会先将原来的**数组拷贝**一份并且让原来数组的**长度+1**后就得到了一个新数组，
然后将新加入的元素**放置在新数组最后一个位置**后，用新数组的**地址替换**掉老数组的地址就能得到最新的数据了。

读是没有加锁的。

## Set（独一无二）

存储的元素不可重复的。

底层数据结构

- `HashSet`(无序，唯一): 基于 `HashMap` 实现的，底层采用 `HashMap` 来保存元素。
- `LinkedHashSet`: `LinkedHashSet` 是 `HashSet` 的子类，并且其内部是通过 `LinkedHashMap` 来实现的。
- `TreeSet`(有序，唯一): 红黑树(自平衡的排序二叉树)。

## Queue（排队）

按特定的排队规则来确定先后顺序，存储的元素是有序的、可重复的。

底层数据结构

- `PriorityQueue`: `Object[]` 数组来实现小顶堆。
- `DelayQueue`:`PriorityQueue`。
- `ArrayDeque`: 可扩容动态双向数组。

## Map（用 key 来搜索）

使用键值对（key-value）存储，每个键最多映射到一个值。
key 是无序的、不可重复的
value 是无序的、可重复的

底层数据结构

- `HashMap（无序）`
- `LinkedHashMap`：`LinkedHashMap` 继承自 `HashMap`，由数组和链表或红黑树组成。另外，`LinkedHashMap` 在上面结构的基础上，增加了一条双向链表，可以保持键值对的插入顺序。
- `Hashtable`：线程安全，数组+链表组成的，数组是的主体，链表则是主要为了解决哈希冲突而存在的。
- `TreeMap（有序）`：红黑树（自平衡的排序二叉树）。

### HashMap的底层结构

1. 数组：这是 HashMap 的主体，用于存储 Node<K,V> 类型的元素，其中每一个 Node 代表了一个键值对。
2. 链表：当多个键值对的哈希值冲突时（也就是说，它们在数组中的位置是相同的），它们会以链表的形式存储。这也是为什么`HashMap`有时会被称为“链表哈希”的原因。
3. 红黑树：当一个数组位置上的链表长度超过阈值时（默认为8），（将链表转换成红黑树前会判断，如果当前数组的长度小于 64，那么会选择先进行数组扩容，而不是转换为红黑树），那么这个链表会转变为红黑树。这样，即使哈希冲突增多，`HashMap`的查询效率也仍然可以在O(log n)的复杂度内。

使用场景：力扣根据题号，对应一道题的详情

### HashMap添加数据过程

第一步：根据要添加的键的哈希码计算在数组中的位置（索引）。

第二步：检查该位置是否为空（即没有键值对存在）
如果为空，直接插入
如果有冲突，再用equals方法判断，如果有冲突就替换，如果没有冲突就挂在链表上

当链表长度>8，数组长度>64，则这个链表升级成红黑树。

当大小到了数组总长度的75%，扩容成两倍

### ConcurrentHashMap底层结构

数组+链表+红黑树，

通过 volatile + CAS + synchronized 实现线程安全

原理：对头节点加锁。

### ConcurrentHashMap添加数据过程

1. 判断容器是否为空，如果为空，则使用 volatile + CAS 来初始化
2. 如果不为空，则根据存储的元素计算该位置是否为空。
   - 如果为空，则利用 CAS 设置该节点（失败则自旋保证成功）；
   - 如果不为空，则使用 synchronized，然后，遍历桶中的数据，并替换或新增节点到桶中，最后再判断是否需要转为红黑树

## List常用方法

1. .add

   .remove

   .get		通过索引访问

   .size

   .contains

   .indexOf

2. 访问List

   ```java
   public class Main {
       public static void main(String[] args) {
           List<String> list = List.of("apple", "pear", "banana");
           for (String s : list) {
               System.out.println(s);
           }
       }
   }
   ```
   
3. List转数组

   ```java
   Integer[] array = list.toArray(new Integer[list.size()]);
   ```

4. 数组转List

   ```java
   Integer[] array = { 1, 2, 3 };
   List<Integer> list = List.of(array);
   ```

## Map常用方法

1. 用HashMap实现Map

   .put

   .get

   .size

   .containskey

2. 遍历key

   ```java
   public class Main {
       public static void main(String[] args) {
           Map<String, Integer> map = new HashMap<>();
           map.put("apple", 123);
           map.put("pear", 456);
           map.put("banana", 789);
           for (String key : map.keySet()) {
               Integer value = map.get(key);
               System.out.println(key + " = " + value);
           }
       }
   }
   ```
   
3. 遍历value

   ```java
   public class MapValuesExample {
       public static void main(String[] args) {
           Map<String, Integer> map = new HashMap<>();
           map.put("Apple", 1);
           map.put("Banana", 2);
           map.put("Cherry", 3);
   
           // 获取所有值
           Collection<Integer> values = map.values();
           
           // 遍历并打印值
           for (Integer value : values) {
               System.out.println(value);
           }
       }
   }
   ```

4. 遍历key和value

   ```java
   public class Main {
       public static void main(String[] args) {
           Map<String, Integer> map = new HashMap<>();
           map.put("apple", 123);
           map.put("pear", 456);
           map.put("banana", 789);
           for (Map.Entry<String, Integer> entry : map.entrySet()) {
               String key = entry.getKey();
               Integer value = entry.getValue();
               System.out.println(key + " = " + value);
           }
       }
   }
   ```

## Set常用方法

.add

.remove

.contains

.size

## Queue常用方法

.add		.offer

.remove	.poll

.element	.peek