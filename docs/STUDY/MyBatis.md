# MyBatis

## 动态SQL

### if

有条件地包含where子句的一部分。

```mysql
<select id="findActiveBlogWithTitleLike"
     resultType="Blog">
  SELECT * FROM BLOG 
  WHERE state = ‘ACTIVE’ 
  <if test="title != null">
    AND title like #{title}
  </if>
</select>
```

意思是说，如果没有传入"title"，那么所有处于"ACTIVE"状态的BLOG都会返回；反之若传入了"title"，那么就会把模糊查找"title"内容的BLOG结果返回

如果传入了title，那么它等同于如下MySQL语句

```mysql
select * from BLOG where state = 'ACTIVE' and title like xxxx
```

如果想可选地通过"title"和"author"两个条件搜索该怎么办呢

```mysql
<select id="findActiveBlogLike"
     resultType="Blog">
  SELECT * FROM BLOG WHERE state = ‘ACTIVE’ 
  <if test="title != null">
    AND title like #{title}
  </if>
  <if test="author != null and author.name != null">
    AND author_name like #{author.name}
  </if>
</select>
```

如果传入了title和author_name，那么它等同于如下MySQL语句

```mysql
select * from BLOG where state = 'ACTIVE' and title like xxxx and author_name like xxxx
```

此时，如果传入了title和author_name，他们的条件都会被筛选到，即同时成立。

那么如果我希望传入了title和author_name的时候，只执行第一个呢，即互斥成立。

需要用到choose (when, otherwise)

### choose (when, otherwise)

`<choose>` 标签类似于 Java 中的 `switch` 语句，用于多条件判断。

`<when>`就是switch中的case，而且还是默认有break的case，即满足一个就不管后面的了

`<otherwise>`就是default

```mysql
<select id="findActiveBlogLike"
     resultType="Blog">
  SELECT * FROM BLOG WHERE state = ‘ACTIVE’
  <choose>
    <when test="title != null">
      AND title like #{title}
    </when>
    <when test="author != null and author.name != null">
      AND author_name like #{author.name}
    </when>
    <otherwise>
      AND featured = 1
    </otherwise>
  </choose>
</select>
```

意思是说，提供了"title"就按"title"查找，提供了"author"就按"author"查找，若两者都没有提供，就返回所有符合条件的BLOG

那么如果没有where中的state = ‘ACTIVE’，根据 `title` 和 `author.name` 动态添加条件，查询 `BLOG` 表。

```mysql
<select id="findActiveBlogLike" resultType="Blog">
  SELECT * FROM BLOG 
  <if test="title != null">
    WHERE title LIKE #{title}
  </if>
  <if test="author != null and author.name != null">
    AND author_name LIKE #{author.name}
  </if>
</select>
```

此时如果只传了anthor_name，SQL语法直接错误了，类似于如下SQL语句

```mysql
SELECT * FROM BLOG 
AND author_name LIKE xxxx
```

那如果想生成类似于如下的SQL语句
```mysql
SELECT * FROM BLOG 
WHERE author_name LIKE xxxx
```

应该使用<where>标签

### trim (where, set)

```mysql
<select id="findActiveBlogLike" resultType="Blog">
  SELECT * FROM BLOG
  <where>
    <if test="title != null">
      title LIKE #{title}
    </if>
    <if test="author != null and author.name != null">
      AND author_name LIKE #{author.name}
    </if>
  </where>
</select>
```

使用<where>好处有二：

1. 如果传入了条件，那么自动加where关键字；如果没传入，自动不加
2. 自动去掉多余的and和or

除了查询的where需要根据传入的多条件来动态生成SQL，更新的SET也需要根据传入的多条件来动态生成SQL。

这就用到了<set>

```mysql
<update id="updateAuthorIfNecessary">
  update Author
    <set>
      <if test="username != null">username=#{username},</if>
      <if test="password != null">password=#{password},</if>
      <if test="email != null">email=#{email},</if>
      <if test="bio != null">bio=#{bio}</if>
    </set>
  where id=#{id}
</update>
```

传进来的参数就改，没传的就不改

使用<set>好处有二：和where类似

1. 自动加set
2. 去掉多余的`,`

其实<where>和<set>是<trim>的简化版本，<trim>才是真正可以灵活地处理 SQL 中的**逻辑符号**的标签

<trim>标签的属性如下

**prefix**：指定前缀，比如 `WHERE`。

**prefixOverrides**：指定需要去掉的前缀符号，比如 `AND`、`OR`。

**suffix**：指定后缀（较少使用）。

**suffixOverrides**：指定需要去掉的后缀符号。

比如，<where>其实是
```mysql
<trim prefix="WHERE" prefixOverrides="AND |OR ">
  ... 
</trim>
```

使用起来就是

```mysql
<select id="findActiveBlogLike" resultType="Blog">
  SELECT * FROM BLOG
  <trim prefix="WHERE" prefixOverrides="AND |OR">
    <if test="title != null">
      title LIKE #{title}
    </if>
    <if test="author != null and author.name != null">
      AND author_name LIKE #{author.name}
    </if>
  </trim>
</select>
```

再比如，<set>其实是

```mysql
<trim prefix="SET" suffixOverrides=",">
  ...
</trim>
```

### foreach

将集合中的元素动态插入到 SQL 中，通常用于 `IN` 查询、批量插入和更新等需要循环操作的场景。

`<foreach>` 标签的属性如下

- **collection**：指定要迭代的集合，可以是 `List`、`Set`、数组等，还支持 `Map`。
- **item**：当前循环到的元素，可以为该元素指定一个变量名，以便在 SQL 中引用。
- **index**：可选，表示集合的当前索引值，用于访问元素的序号。
- **open**：循环开始前添加的字符串，例如用 `(`。
- **close**：循环结束后添加的字符串，例如用 `)`。
- **separator**：每个元素之间的分隔符，例如 `,` 或 `AND`。

#### IN查询

```mysql
<select id="findBlogsByIds" resultType="Blog">
  SELECT * FROM BLOG WHERE id IN 
  <foreach collection="ids" item="id" open="(" separator="," close=")">
    #{id}
  </foreach>
</select>
```

加入传入了ids集合为[1, 2, 3]相当于

```mysql
select * from BLOG where id in {1, 2, 3}
```

#### 批量插入

```mysql
<insert id="insertBlogs">
  INSERT INTO BLOG (title, author_name) VALUES
  <foreach collection="blogs" item="blog" separator=",">
    (#{blog.title}, #{blog.author_name})
  </foreach>
</insert>
```

相当于

```mysql
insert into BLOG(title, author_name)
values ('Title1', 'Author1'), ('Title2', 'Author2')
```

#### 批量更新

也可以用 `<foreach>` 动态生成 `CASE WHEN` 语句

```mysql
<update id="updateBlogAuthors">
  UPDATE BLOG
  SET author_name = 
  <foreach collection="blogs" item="blog" separator=" ">
    WHEN id = #{blog.id} THEN #{blog.author_name}
  </foreach>
  WHERE id IN 
  <foreach collection="blogs" item="blog" open="(" separator="," close=")">
    #{blog.id}
  </foreach>
</update>
```

相当于

```mysql
UPDATE BLOG
SET author_name = CASE 
  WHEN id = 1 THEN 'Author1'
  WHEN id = 2 THEN 'Author2'
  ELSE author_name
END
WHERE id IN (1, 2)
```

## useGeneratedKeys

 `insert` 标签的一个属性，用于**自动获取数据库生成的主键值**。

常见属性

**useGeneratedKeys**：是否启用主键自动生成功能，通常设置为 `true`。

**keyProperty**：指定实体类中接收生成的主键值的属性名（通常是实体类的主键字段）。

**keyColumn**（可选）：指定数据库表中的主键列名，主要用于属性名与列名不一致时。

例如
```mysql
CREATE TABLE BLOG (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255)
);
```

```mysql
<insert id="insertBlog" useGeneratedKeys="true" keyProperty="id">
  INSERT INTO BLOG (title) VALUES (#{title})
</insert>
```

```java
Blog blog = new Blog();
blog.setTitle("My First Blog");
blogMapper.insertBlog(blog);
System.out.println(blog.getId()); // 获取自动生成的主键ID
```

如果没有使用useGeneratedKeys，怎样得到主键id呢？

```java
blogMapper.insertBlog(blog);

// 获取最近插入的 ID
Long generatedId = blogMapper.getLastInsertId(); // 使用一个查询方法执行 SELECT LAST_INSERT_ID()
```

```mysql
SELECT LAST_INSERT_ID();
```

这样就多写了一个SQL语句

方法二

```java
blogMapper.insertBlog(blog);

// 根据唯一字段查找 ID
Long generatedId = blogMapper.findIdByTitle(blog.getTitle());
```

```mysql
SELECT id FROM blog WHERE title = #{title};
```

同样多写了一个SQL语句

