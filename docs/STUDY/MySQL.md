# MySQL

## Terminal启动指令

```bash
export PATH=$PATH:/usr/local/mysql/bin
source ~/.bash_profile
mysql --version
mysql -u root -p


sudo /usr/local/mysql/support-files/mysql.server start
```

## 基础指令

### SELECT

字句顺序

1. select
2. from
3. where
4. group by
5. having
6. order by
7. limit

LIMIT：限制输出行数

```mysql
select prod_name
from products
limit 3, 4;
-- 意思相同，都是从行3开始往下取4行
select prod_name
from products
limit 4 offset 3;
```

（select的操作符）DISTINCT：不要重复的

```mysql
select distinct vend_id
from products;
```

ORDER BY：根据xxx排序。默认是ASC（升序），可以加DESC改成降序

```mysql
select prod_id, prod_price, prod_name
from products
order by prod_price desc, prod_name;
```

（where的操作符）先计算AND，再计算OR

```mysql
select prod_name, prod_price
from products
where (vend_id = 1002 or vend_id = 1003) and prod_price >= 10;
```

（where的操作符）IN 和NOT IN后面加()一个范围

```mysql
select prod_name, prod_price
from products
where vend_id not in (1002, 1003)
order by prod_name;
```

（where的操作符）LIKE：使用通配符，如%、_

```mysql
select prod_id, prod_name
from products
where prod_name like 'jet%';
```

（where的操作符）REGEXP：使用正则表达式

```mysql
select prod_name
from products
where prod_name regexp '\\([0-9] sticks?\\)'
order by prod_name;
```

（select的操作符）Concat()：拼接串

RTrim()：去除右边空格 

LTrim() ：去除左边空格

Trim()：去除两边空格

```mysql
select concat(vend_name, '(', vend_country, ')')
from vendors
order by vend_name;
```

（select的操作符）聚集函数：AVG(), COUNT(), MAX(), MIN(), SUM()

```mysql
select avg(distinct prod_price) as avg_price
from products
where vend_id = 1003;
```

### `count(*)`，`count(1)`，`count(列名)`

show warings指令可以看出，`count(*)`会被优化成`count(0)`；`count(1)`不变，所以他俩效率相同，只不过在 InnoDB 引擎中，对`count(*)`做了特别优化，会去从统计数据里面找，所以`count(*)`会更快。

`count(列名)`会逐行对比每一条记录中的该列名是否为 NULL，会剔除掉这些列名，所以效率最慢

GROUP BY, HAVING：分组，过滤分组

```mysql
select vend_id, count(*) as num_prods
from products
where prod_price >= 10
group by vend_id
having count(*) >= 2;
```

### 子查询

常见在where子句的in操作符中

```mysql
select cust_id
from orders
where order_num in 
(select order_num
from orderitems
where prod_id = 'TNT2');
```

### 联结

INNER JOIN：内部联结

```mysql
select vend_name, prod_name, prod_price
from vendors inner join products
on vendors.vend_id = products.vend_id;
```

联结多个表用where and

子联结：表p1和表p2是同一张表，用as。筛选的条件在where的and里面写

```mysql
select p1.prod_id, p1.prod_name
from products as p1, products as p2
where p1.prod_id = p2.prod_id 
and p2.prod_id = 'DTNTR';
```

使用自然联结可以排除连表时候重复出现的列，select的时候把要输出的列都写上，第一个表可以使用t1.*把它的列都带上

LEFT OUTER JOIN    RIGHT OUTER JOIN：外部联结

```mysql
select customer.cust_id, orders.order_num
from customers left outer join orders
on customers.cust_id = orders.cust_id;
```

### 组合查询

UNION / UNION ALL

union和where一样，union all会返回重复的行（where做不到）

只能在最后一个块儿中使用order by

### 全文本查询

默认的搜索引擎InnoDB用不了，MyISAM可以用

match(被搜索的列)，against(要搜的东西)

可以放在where里，会输出包含against的东西

也可以放在select里，会输出等级值

```mysql
select note_text
from productnotes
where match(note_text) against('rabbit');
```

```mysql
select note_text, match(note_text) against('rabbit') as ranks
from productnotes;
```

### INSERT

```mysql
insert into customers(cust_name,
                     cust_address,
                     cust_city,
                     cust_state,
                     cust_zip,
                     cust_country,
                     cust_contact,
                     cust_email)
values('Pep E. LaPew',
     '100 Main Street',
     'Los Angeles',
     'CA',
     '90046',
     'USA',
     NULL,
     NULL);
```

插入多个行

```mysql
insert into t1(x1,x2,x3)
values(y1, y2, y3),
			(y11,y22,y33);
```

插入检索出来的数据

```mysql
insert into t1(x1, x2, x3)
-- 列名可以不同，看的是位置
select x1, x2, x3
from t2;
```

### UPDATE

```mysql
update customers
set cust_name = 'The Fudds',
		cust_email = 'elmer@fudd.com'
where cust_id = 10005;
```

**没有写where子句的话，就全变了**

想要删除某个列的值就把它set成null

### DELETE

```mysql
delete from customers
where cust_id = 10006;
```

**没有写where子句的话，就全删除了**

## 索引

```mysql
CREATE INDEX idx_name ON employees(name);  -- 创建一个普通索引
SHOW INDEX FROM employees;  -- 查看索引信息
```

索引底层结构是B+树

优点：减少 IO 次数->加快数据的检索速度

缺点：当对表中的数据进行增删改的时候，如果数据有索引，那么索引也需要动态的修改，会降低 SQL 执行效率

### 为什么用B+树

B+ 树的非叶子节点不存放实际的记录数据，**仅存放索引**，因此数据量相同的情况下，相比存储即存索引又存记录的 B 树，B+树的**非叶子节点可以存放更多的索引**，因此 B+ 树可以比 B 树更**「矮胖」**，查询底层节点的磁盘 **I/O次数会更少**。

B+ 树有大量的冗余节点（**所有非叶子节点都是冗余索引**），这些冗余索引让 B+ 树在**插入、删除的**效率都更高，比如删除根节点的时候，不会像 B 树那样会发生**复杂的树的变化**；

B+ 树叶子节点之间用链表连接了起来，**有利于范围查询**，而 B 树要实现范围查询，因此只能通过树的遍历来完成范围查询，这会涉及多个节点的磁盘 I/O 操作，范围查询效率不如 B+ 树。

### B树和B+树的异同

1. B树的节点 = key + data
   B+树的叶子节点 = key + data ， 其他内部节点 = key
2. B树的叶子节点是孤立的，B+树的叶子节点有一条引用链指向与它相邻的叶子节点。

### 分类

主键索引（聚簇索引）：叶子节点存的是记录的完整数据

![索引](/Users/liuyu/noteBook/assets/索引.png)

普通索引（二级索引）：叶子节点存的是**一个**索引列+主键值，然后拿着主键值去回表。

![二级索引](/Users/liuyu/noteBook/assets/二级索引.png)

联合索引：叶子节点存的是**多个**索引列+主键值，然后拿着主键值去回表。

![联合索引](/Users/liuyu/noteBook/assets/联合索引.png)

### 什么时候需要加索引

频繁查询

作为where条件的

需要排序的：因为索引排好序了

### 索引优化

前缀索引优化：只使用字段的前几个字符做索引，减小索引字段大小

覆盖索引优化：二级索引列中有我select的所有信息了，不需要再回表了

1. select id from t where name = 'tom'，最后就是要id，二级索引列中，就有id，不用回表了
2. select id, price from t where name = 'banana'，有联合索引(id,name,price)，二级索引列中，需要的都在，不用回表了

主键索引最好是自增的：叶子节点是按主键顺序存放的，自增的话，如果当前索引页满了，直接新开页就好了。
如果不是自增，当前索引页满了，可能需要移动很多索引来保证顺序存放

防止索引失效

### 什么时候索引失效

1. 使用!=这种全局扫描的
2. LIKE里面%开头的
3. 对索引列函数计算的
4. 最左前缀原则。像 `(col1, col2, col3)` 这样的联合索引只有在查询条件在索引树左侧时才能够被用到。比如查询 `col1` 或 `col1, col2`，索引是起效的。但当查询 `col2` 或者 `col3` 或者 `col2, col3`这样，该索引就不起作用了。

### 行锁

只有**通过索引条件检索数据**，MySQL 才使用行级锁，否则，MySQL 将使用表锁。

MySQL 的行锁有两种模式：**共享锁**（Shared Locks，简称S锁）**和排他锁**（Exclusive Locks，简称X锁）。

当一个事务已经持有了某行数据的S锁，其他事务可以继续获取该行的S锁，但不能获取X锁，直到已经持有S锁的事务释放锁。
当一个事务已经持有了某行数据的X锁，其他事务不能再获取该行的任何锁，直到已经持有X锁的事务释放锁。

如果一个操作符合索引，则 InnoDB 只给符合条件的索引记录加锁；如果不符合索引，InnoDB 则会对表中所有的记录加锁，此时的行锁就升级为表锁了。

## 事务

### 事务隔离级别

1. 读未提交 (READ UNCOMMITTED): 最低的隔离级别，事务未提交时，其他事务能看到其改动，容易导致脏读。
2. 读已提交 (READ COMMITTED): 不同的事务之间可以看到对方已提交的改动，但并不能看到未提交的改动，可以防止脏读，但可能导致不可重复读。
3. 可重复读 (REPEATABLE READ): MySQL默认的隔离级别，在同一事务里的查询结果是一致的，解决了“不可重复读”问题，但可能出现幻读。
4. 串行化 (SERIALIZABLE): 最高的隔离级别，所有的事务将串行执行，能防止所有并发问题，但性能低下。

### MVCC

代替了锁机制，它基于时间戳的概念，为每个数据版本都分配了一个唯一的时间戳。

当一个事务开始时，它会读取当前的数据版本，并将该版本的时间戳作为自己的”读取时间戳”。
在事务执行期间，它只能看到在该时间戳之前已经提交的数据版本。
对于写操作，事务会创建一个新的数据版本，并将其时间戳设置为当前时间戳。

**事务可以看到自己做的更改**，包括未提交的。

对于其他事务的更改，`Read View`的可见性规则如下：

- 如果记录的`trx_id`小于`min_trx_id`，则记录可见。
- 如果记录的`trx_id`大于等于`max_trx_id`，则记录不可见。
- 如果记录的trx_id介于min_trx_id和max_trx_id之间，则：
  - 如果`trx_id`在`m_ids`中，则不可见。
  - 如果`trx_id`不在`m_ids`中，则可见。

### 脏读、不可重复读、幻读

如果一个事务「读到」了另一个「未提交事务修改过的数据」，就意味着发生了「脏读」现象。

在一个事务内多次查询某个符合查询条件的「记录数量」，如果出现前后两次查询到的记录数量不一样的情况，就意味着发生了「幻读」现象。

- 脏读：读到其他事务未提交的数据；
- 不可重复读：前后读取的数据不一致；
- 幻读：前后读取的记录**数量**不一致。

幻读无法解决 insert 问题：虽然锁了读好的数据，但是抵挡不住 insert 进来的数据

### 可重复读

可重复读使用快照读和当前读来尽量避免幻读。

快照读，使用MVCC：第一个查询语句后，创建Read View

当前读，使用临键锁：当前语句执行前，就查询最新版本的数据

但是仍然无法彻底避免：

情况1:

| 事务A                                   | 事务B                                          |
| --------------------------------------- | ---------------------------------------------- |
| begin;                                  |                                                |
| select * from t where id = 5;           |                                                |
|                                         | begin;<br />insert into t values(5, 'bob',18); |
| update t set name = 'tom' where id = 5; |                                                |
| select * from t where id = 5;           |                                                |

两次select得到的结果不一样。

事务A的更新操作，使得id=5的这条记录的trx_id变成了事务A的create_trx_id，所以就能查到了。

情况2:

事务a先快照读，事务b插入，事务a再当前读

彻底避免：在开启事务之后，立刻使用select...for update这样的当前读，就会加临键锁，其他事务就插不了了

## Delete和Truncate的区别

```mysql
# 这俩都能删除清空表里全部数据
delete from tablename;
truncate table tablename;

# 清除一部分只能用delete
delete FROM table1 WHERE ?;
```

如果表中有自增的字段，又希望删全表，如果使用前面的两种方法，自增的字段会变回从1开始。
但如果使用`delete FROM table1 WHERE 1;`就从字段原先最大的值继续增加。但是这样扫描了所有的记录，会慢得多。

当表很大的时候，用truncate删得快。因为它是将表结构重新建一次，delete是一行一行的删

Delete 存日志了，可以回溯，Truncate 不能回溯

## 分库分表

分库：分库就是将一个数据库分解为多个较小的数据库。

分表：分表就是将一个大表分解为多个较小的表。

## 数据库三大范式

第一范式原子性：数据表中字段值不可再分割
第二范式唯一性：消除非主键部分对**联合主键中部分字段**的依赖
第三范式独立性：消除传递依赖，每一列数据都和主键直接相关，而不能间接相关。

举例：

第一范式：字段「地址」根据需求，可以再细分成「省份」、「城市」、「详细地址」三个字段

第二范式：一个表中有「订单编号」「商品编号」作为联合主键，此时「订购客户名」和「商品编号」无关

第三范式：尽可能使用外键，然后连表查询，这样减少了数据冗余

## 数据库Object对象

九个

表、索引、视图、图表、缺省值、规则、触发器、存储过程、用户

## 数据库表与视图的关系

视图是虚拟的表，本身不包含数据，也就不能对其进行索引操作。对视图的操作和对普通表的操作一样。

视图：行和列数据来自由定义视图的查询所引用的表，并且在引用视图时动态生成。

视图的作用类似于筛选。

```mysql
CREATE VIEW top_10_user_view AS
SELECT id, username
FROM user
WHERE id < 10;
```

## 数据库约束有哪些

`NOT NULL` - 指示某列不能存储 NULL 值。

`UNIQUE` - 保证某列的每行必须有唯一的值。

`PRIMARY KEY` - NOT NULL 和 UNIQUE 的结合。确保某列（或两个列多个列的结合）有唯一标识，有助于更容易更快速地找到表中的一个特定的记录。

`FOREIGN KEY` - 保证一个表中的数据匹配另一个表中的值的参照完整性。

`CHECK` - 保证列中的值符合指定的条件。

`DEFAULT` - 规定没有给列赋值时的默认值。

讲一下外键约束。

外键约束的作用是维护表与表之间的关系，确保数据的完整性和一致性。让我们举一个简单的例子

```mysql
CREATE TABLE students (
  id INT PRIMARY KEY,
  name VARCHAR(50),
  course_id INT,
	FOREIGN KEY (course_id) REFERENCES courses(id)
);
```

`students`表中的`course_id`字段是一个外键，它指向`courses`表中的`id`字段。

这个外键约束确保了每个学生所选的课程在`courses`表中都存在

## 慢sql

先定位再分析后解决

### 定位

使用慢查询日志定位

`show variables like '%slow_query_log%'`看看是否开启了慢查询日志，默认关，同时也能看到日志文件地址

方法1:`set global slow_query_log=on;`可以开启，针对全局session生效，重启后失效

`show variables like "long_query_time";`查询慢查询的时间限制

`set long_query_time = 0.01`可以设置慢查询的时间限制

方法2:在mysql配置文件 /etc/my.cnf 开启慢查询日志，可以永久生效

```
# 开启MySQL慢日志查询开关
slow_query_log=1
# 设置慢日志的时间为2秒，SQL语句执行时间超过2秒，就会视为慢查询，记录慢查询日志
long_query_time=2
```

查询日志

`cat xxxxx-slow.log`

### 分析

使用 explain

通过type查看是否存在**全索引扫描或全盘扫描**，通过key和key_len检查是否命中了**索引**，通过extra检查是否**回表**了

### 解决

不查了，数据直接放redis里

加索引，优化索引

优化sql（索引失效）

修改表结构（反范式--->加冗余字段）

## EXPALIN

type:

| system         | const        | eq_ref                     | ref                                     | range                   | index        | all      | null |
| -------------- | ------------ | -------------------------- | --------------------------------------- | ----------------------- | ------------ | -------- | ---- |
| 查询系统中的表 | 根据主键查询 | 唯一索引或主键进行等值连接 | 非唯一索引进行等值连接,可能匹配多行记录 | BETWEEN、>、<进行查询时 | 遍历整个索引 | 遍历全表 |      |

extra:

| using index                                                | using index condition    |
| ---------------------------------------------------------- | ------------------------ |
| 使用了索引，直接在索引列就能找到值，不需要回表（覆盖索引） | 使用了索引下推，需要回表 |

举例：select id from product where name like 't%';

id是主键索引，name是普通索引（二级索引），直接在二级索引就有id了（因为二级索引列就是放的主键索引）

所以此时extra就显示：using where; using index

## 执行SQL语句过程

### 执行器

**主键索引查询：**

举例：`select * from product where id = 1;`

id是主键，所以type为const

执行器查询流程：

1. 先调用read_first_record 函数指针指向的函数，**这里是const，所以指向 InnoDB 引擎索引查询的接口**
   并把条件`id = 1`给存储引擎，让存储引擎定位到符合条件的记录。
2. 存储引擎通过主键索引的B+树定位记录，返回给执行器
3. 执行器查询是while循环，继续查，不过现在不是第一次查询了，所以调用的是read_record，那么因为是const类型，所以这次查询中，read_record指向的是-1，也就退出循环了

**全表扫描**

举例：`select * from product where name = 'iphone';`

没有加索引，索引type是all

执行器查询流程：

1. 调用read_first_record，**这里是all，所以指向 InnoDB 引擎全扫描的接口**，并把条件给存储引擎
2. 存储引擎判断name是否等于iphone，不是就跳过，是则返回给客户端
3. 调用read_record，因为是all类型，所以指向的**还是 InnoDB 引擎全扫描的接口**，所以继续读下一条记录，直到全扫一遍。

**索引下推**

可以减少回表！因为将server层该干的事情，交给存储引擎去做了

举例：`select * from t_user where age > 20 and reward = 100000;`

有索引(age, reward)，但是因为使用`>`，所以reward=100000无法命中

如果不使用索引下推：

1. server层调存储引擎定位到这个二级索引：age>20的第一条记录
2. 存储引擎根据age>20定位到之后，得到主键值，**回表**，得到完整记录，返回给server层
3. server层判定reward是否等于100000，成立就返给客户端，不成立就跳过
4. 重复2和3，直到全扫一遍

使用索引下推

1. 同上，server层调存储引擎定位到这个二级索引：age>20的第一条记录
2. 存储引擎根据age>20定位到之后，**因为是联合索引，直接在这个二级索引列上其实就有reward，那么可以直接查看是否reward = 100000，**不成立就不用回表，成立再回表，然后返给server层
3. server层拿到记录后，再看看其他没有命中索引的条件是否成立（此例没有），成立就给客户端，不成立就跳过
4. 重复2和3，直到全扫一遍





