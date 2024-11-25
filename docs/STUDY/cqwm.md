# 苍穹外卖笔记

## 介绍一下整个项目

使用场景是一个点餐系统。
在店家的管理端，前端使用VUE框架搭建，后端使用SpringBoot框架搭建，数据库采用的MySQL；
在顾客的用户端，是一个微信小程序。

从实际使用流程来串一下这个项目以及用到的技术。

首先从前端网页上登录，这里涉及到JWT、拦截器、ThreadLocal等技术。
现在成功登陆进管理系统页面，可以做到对菜品、套餐、订单、员工的增删改查，
这方面我操作数据是使用的MyBatis，用它的分页组件PageHelper，用它的动态SQL。

整个项目还使用了全局异常处理、AOP、Redis缓存等技术

为了避免写（“创建人修改人是谁”这样每个表都有的）重复的代码，运用AOP来实现公共字段的自动填充。
同时使用Redis来进行缓存菜品，可以提高性能。（比如新增了菜，就需要把缓存删了。）

然后再说用户那边，从微信小程序登陆，需要和微信官方的接口收发数据，也就涉及到了HttpClient以及拦截器技术。
登录进来浏览菜单（对菜品、套餐的查操作），添加购物车（插入购物车表）

支付完成后，对管理端页面进行来单提醒，使用WebSocket，此外还有订单状态的定时处理，使用的是Spring Task组件。

## 后端具体功能

### 登录功能--JWT、ThreadLocal、拦截器

登录成功后，生成JWT令牌，返回给前端。

后续请求b中，拦截器中校验JWT令牌，成功就放行，并且把员工id放进ThreadLocal

这个请求b中如果有需要用到员工id，可以直接从Threadlocal中获取，不需要校验令牌了

如果没有使用ThreadLocal，如果有需要用到员工id，需要再解析一遍JWT才能得到员工id

这就是所谓的“通过ThreadLocal优化鉴权逻辑”。不是说在第一次登录后，后面就不用解析JWT了，创新新品的请求过来，还是要先解析JWT确定当前用户的登录状态，只不过在完成具体业务的时候就可以不再解析JWT了，在拦截器中验证好JWT后，可以往threadlocal里面存具体业务需要的变量。

### 员工管理-- JWT、全局异常处理器

1. 添加员工时重名怎么处理？
   员工表的username列是加了唯一约束的，不允许重复。当重名的时候后端会返回SQL异常

   ```bash
   Duplicate entry 'zhangsan' for key 'employee.idx_username'
   ```

   那我就返给前端一个提示信息“xxx已存在”，让他换个username
   所以通过全局异常处理器处理：
   创建了一个 GlobalExceptionHandler 类
   类上加 @RestControllerAdvice 可以实现全局的异常处理
   
   方法上加 @ExceptionHandler 会捕获指定的异常
   
   ex.getMessage -> contains -> split[2] -> return msg
   
   ```java
   @RestControllerAdvice
   public class GlobalExceptionHandler {
       /**
        * 捕获业务异常
        */
       @ExceptionHandler
       public Result exceptionHandler(SQLIntegrityConstraintViolationException ex){
   ```
   
2. 添加员工时怎样动态标明创建人和修改人id
   流程如下：因为我当前是登录状态才能添加员工，所以我有一个JWT，那我先解析JWT得出当前人的id，再用ThreadLocal传给Service的save方法

### 员工分页查询--PageHelper

1. 使用PageHelper分页插件
   本质上就是查询操作，Controller->Service->ServiceImpl->Mapper
   DTO对象里面是员工姓名、页码、每页显示记录数
   封装返回一个PageResult对象，里面是总记录数 和 当前页的数据（这是一个集合List）
   其中，在ServiceImpl里面用到PageHelper分页插件

   ```java
   public PageResult pageQuery(EmployeePageQueryDTO employeePageQueryDTO) {
       // select * from employee limit 0,10
       //开始分页查询
     // PageHelper.startPage(页码，每页显示的记录数)
       PageHelper.startPage(employeePageQueryDTO.getPage(), employeePageQueryDTO.getPageSize());
   // Page<记录类型> page = 要查的对象的Mapper.方法(DTO)
       Page<Employee> page = employeeMapper.pageQuery(employeePageQueryDTO);//后续定义
     //page.getTotal()
       long total = page.getTotal();
     //page.getResult()
       List<Employee> records = page.getResult();
   
       return new PageResult(total, records);
   }
   ```

2. 可以根据姓名查询员工，SQL语句如下

```xml
<mapper namespace="com.sky.mapper.EmployeeMapper">
    <select id="pageQuery" resultType="com.sky.entity.Employee">
        select * form employee
        <where>
            <if test="name != null and name != ''">
                and name like concat('%',#{name},'%')
            </if>
        </where>
        order by create_time desc
    </select>
</mapper>
```

### 公共字段自动填充--AOP

在 新建、修改员工，新建、修改菜品分类 的时候，都有设置当前时间和设置当前用户id的代码，把它抽出来统一处理，简化代码。这里使用的就是AOP切面编程

1. 写了一个自定义注解x，只要标注了这个注解就自动填充。
2. 写了一个切面类，声明好只对加了注解x的方法生效。切面类里面通过反射获取对象修改对象，完成自动填充

### 新增菜品--OSS

技术点：

1. 菜品有图片，使用OSS
2. 菜品有口味，有dish和dish_flavor两个表
   new dish对象，dishDTO拷贝进dish，insert进dish表
   此时dish表完事儿了，该dishFlavor表了，从DTO取出从前端传入的口味列表
   插数据需要三个值：dishId、口味名、口味值，缺少dishId
   （因为之前insert的时候用了useGenerateKey，此刻不需要再从数据库中查）直接取出dishId，foreach进去
   insert进dishFlavor表
   
   ```java
   public void saveWithFlavor(DishDTO dishDTO) {
   
           Dish dish = new Dish();
           BeanUtils.copyProperties(dishDTO, dish);
   
           //向菜品表插入1条数据
           dishMapper.insert(dish);
   
           //获取insert语句生成的主键值
           Long dishId = dish.getId();
   
           List<DishFlavor> flavors = dishDTO.getFlavors();
           if (flavors != null && flavors.size() > 0) {
               flavors.forEach(dishFlavor -> {
                   dishFlavor.setDishId(dishId);
               });
   
               //向口味表插入n条数据
               dishFlavorMapper.insertBatch(flavors);
           }
       }
   ```
3. 口味有多个类（温度、辣度等），需要批量插入，for-each
   Mybatis可以批量插入

```xml
<insert id="insertBatch">
        insert into dish_flavor(dish_id, name, value) VALUES
        <foreach collection="flavors" item="df" separator=",">
            (#{df.dishId}, #{df.name}, #{df.value})
        </foreach>
    </insert>
```

### 删除菜品

删除一个菜品和批量删除菜品使用同一个接口

1. 起售中的菜品不能删除

2. 当菜品属于某个套餐的时候，是不允许被删除的

3. 删除菜品后，关联的口味数据也需要删除掉

那么在“根据菜品id查询对应的套餐id”接口中，会用到foreach

```xml
<select id="getSetmealIdsByDishIds" resultType="java.lang.Long">
    select setmeal_id from setmeal_dish where dish_id in
    <foreach collection="dishIds" item="dishId" separator="," open="(" close=")">
        #{dishId}
    </foreach>
</select>
```

### 删除套餐

可以批量删除

起售中的套餐不能删除

### 修改套餐

先根据id查套餐，用于回显，需要用到套餐表和套餐菜品表

id查套餐，id查套餐菜品，全倒给VO

```java
public SetmealVO getByIdWithDish(Long id) {
    Setmeal setmeal = setmealMapper.getById(id);
    List<SetmealDish> setmealDishes = setmealDishMapper.getBySetmealId(id);

    SetmealVO setmealVO = new SetmealVO();
    BeanUtils.copyProperties(setmeal, setmealVO);
    setmealVO.setSetmealDishes(setmealDishes);
    
    return setmealVO;
}
```

然后就可以修改套餐了。

1. update套餐表
2. 根据套餐id删套餐菜品表
3. 把id赋值给套餐菜品表中的每个菜品（foreach）
4. 把菜品列表插入套餐菜品表

```java
@Transactional
    public void update(SetmealDTO setmealDTO) {
        Setmeal setmeal = new Setmeal();
        BeanUtils.copyProperties(setmealDTO, setmeal);

        //1、修改套餐表，执行update
        setmealMapper.update(setmeal);

        //套餐id
        Long setmealId = setmealDTO.getId();

        //2、删除套餐和菜品的关联关系，操作setmeal_dish表，执行delete
        setmealDishMapper.deleteBySetmealId(setmealId);

        List<SetmealDish> setmealDishes = setmealDTO.getSetmealDishes();
        setmealDishes.forEach(setmealDish -> {
            setmealDish.setSetmealId(setmealId);
        });
        //3、重新插入套餐和菜品的关联关系，操作setmeal_dish表，执行insert
        setmealDishMapper.insertBatch(setmealDishes);
    }
```

### 起售停售套餐

起售套餐时，判断套餐内是否有停售菜品，有停售菜品不行。

用套餐id查菜品列表出来，foreach每个菜

### 营业状态设置--Redis

使用到Redis的String。虽然，可以通过一张表来存储营业状态数据，但整个表中只有一个字段，所以意义不大。

### 微信登录--HttpClient、拦截器

流程：小程序端发一个code给后端，后端把code+appid+appsecret发给微信官方服务器，官方返给我openid和session_key，在后端把openid+token给小程序端，小程序端放threadlocal存好，再发带着token，后端解析证明真身。

```java
public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        //判断当前拦截到的是Controller的方法还是其他资源
        if (!(handler instanceof HandlerMethod)) {
            //当前拦截到的不是动态方法，直接放行
            return true;
        }

        //1、从请求头中获取令牌
        String token = request.getHeader(jwtProperties.getUserTokenName());

        //2、校验令牌
        try {
            log.info("jwt校验:{}", token);
            Claims claims = JwtUtil.parseJWT(jwtProperties.getUserSecretKey(), token);
            Long userId = Long.valueOf(claims.get(JwtClaimsConstant.USER_ID).toString());
            log.info("当前用户的id：", userId);
            BaseContext.setCurrentId(userId);
            //3、通过，放行
            return true;
        } catch (Exception ex) {
            //4、不通过，响应401状态码
            response.setStatus(401);
            return false;
        }
    }
```

```java
@Autowired
private JwtTokenUserInterceptor jwtTokenUserInterceptor;

/**
 * 注册自定义拦截器
 * @param registry
 */
protected void addInterceptors(InterceptorRegistry registry) {
    log.info("开始注册自定义拦截器...");
    //.........

    registry.addInterceptor(jwtTokenUserInterceptor)
        .addPathPatterns("/user/**")
        .excludePathPatterns("/user/user/login")
        .excludePathPatterns("/user/shop/status");
}
```

### 缓存菜品--Redis

使用Redis，缓存规则：dish_分类id。

存的String类型，是序列化后的对象

```java
@Autowired
private RedisTemplate redisTemplate;

/**
 * 根据分类id查询菜品
 * @param categoryId
 * @return
 */
@GetMapping("/list")
@ApiOperation("根据分类id查询菜品")
public Result<List<DishVO>> list(Long categoryId) {
    log.info("根据分类id查询菜品：{}",categoryId);

    //构造redis中的key，规则：dish_分类id
    String key = "dish_" + categoryId;

    //查询redis中是否存在菜品数据
    List<DishVO> list = (List<DishVO>) redisTemplate.opsForValue().get(key);
    if(list != null && list.size() > 0){
        //如果存在，直接返回，无须查询数据库
        return Result.success(list);
    }

    //如果不存在，查询数据库，将查询到的数据放入redis中
    Dish dish = new Dish();
    dish.setCategoryId(categoryId);
    dish.setStatus(StatusConstant.ENABLE);//查询起售中的菜品

    list = dishService.listWithFlavor(dish);
    redisTemplate.opsForValue().set(key, list);

    return Result.success(list);
}
```

### 清理缓存--Redis与MySQL一致性

为了Redis和MySQL的一致性，清理缓存。

新增、修改、删除、起售停售

比如新增，修改Controller方法，在新增之后，不需要把所有缓存全清了，把当前菜品的**分类下的**缓存清掉就好了

```java
@PostMapping
@ApiOperation("新增菜品")
public Result save(@RequestBody DishDTO dishDTO) {
    log.info("新增菜品：{}", dishDTO);
    dishService.saveWithFlavor(dishDTO);

    //清理缓存数据
    String key = "dish_" + dishDTO.getCategoryId();
    cleanCache(key);
    
    return Result.success();
}
```

```java
@Autowired
private RedisTemplate redisTemplate;

/**
 * 清理缓存数据
 * @param pattern
 */
private void cleanCache(String pattern){
    Set keys = redisTemplate.keys(pattern);
    redisTemplate.delete(keys);
}
```

删除菜品的话就需要把所有菜品的缓存全删了，在删掉菜品的时候，套餐需不需要删？

既然能删，代表着任何套餐里都没有该菜品，所以套餐不用删！所以删掉dish_*即可



修改菜品的话，为什么要把所有菜品缓存全清掉

因为有可能修改了菜品的分类，那么就会有两个分类下的菜品变了，干脆全删



起售停售也是省得从菜品id再查菜品分类id，干脆全删

### 缓存套餐-- Spring Cache

Spring Cache 提供了一层抽象，底层可以切换不同的缓存实现，例如：

- EHCache
- Caffeine
- Redis（常用）

@EnableCaching 开启缓存注解功能，通常加在启动类上

@Cacheable 在方法执行前先查询缓存中是否有数据，如果有数据，则直接返回缓存数据；如果没有缓存数据，调用方法并将方法返回值放到缓存中

@CacheEvict 清理指定缓存

`{cacheName}::{key}` 是默认的键格式，但可以通过 `key` 属性进行自定义

```java
//key: setmealCache_传入的id
@Cacheable(cacheNames = "setmealCache", key = "'setmeal_' + #categoryId")
```

在用户端接口 SetmealController 的 list 方法上加入 @Cacheable注解

```java
//key: setmealCache::传入的id
@Cacheable(cacheNames = "setmealCache",key = "#categoryId") 
public Result<List<Setmeal>> list(Long categoryId) {
```

在管理端接口 SetmealController 的 save、delete、update、startOrStop 等方法上加入 CacheEvict 注解

```java
//key: setmealCache::传入的id
@CacheEvict(cacheNames = "setmealCache",key = "#setmealDTO.categoryId")
public Result save(@RequestBody SetmealDTO setmealDTO) {
```

```java
@CacheEvict(cacheNames = "setmealCache",allEntries = true)//删除userCache下所有的缓存数据
public Result delete(@RequestParam List<Long> ids) {
```

### 用户下单

用户下单后生成订单表orders和订单明细表order_detail

当一个订单下有多个商品的时候，没必要给每个商品都写上地址簿，餐具数量等等，所以开一个明细表

### 添加购物车

购物车需要保存到MySQL的shopping_cart表

### 微信支付--内网穿透

微信官方返回给后端的预支付交易单 和 支付成功后微信官方返回给后端的消息 这两个接口需要很高的安全性

微信官方给出了解决方案：使用 微信支付平台证书、商户私钥文件 加密

那么微信官方怎样连接到我本地的后端呢？

内网穿透，使用cpolar软件获得一个临时域名

### 再来一单--Java8流式API

```java
/**
 * 再来一单
 * @param id
 */
public void repetition(Long id) {
    // 查询当前用户id
    Long userId = BaseContext.getCurrentId();

    // 根据订单id查询当前订单详情
    List<OrderDetail> orderDetailList = orderDetailMapper.getByOrderId(id);

    // 将订单详情对象转换为购物车对象
    List<ShoppingCart> shoppingCartList = orderDetailList.stream().map(x -> {
        ShoppingCart shoppingCart = new ShoppingCart();

        // 将原订单详情里面的菜品信息重新复制到购物车对象中
        BeanUtils.copyProperties(x, shoppingCart, "id");
        shoppingCart.setUserId(userId);
        shoppingCart.setCreateTime(LocalDateTime.now());

        return shoppingCart;
    }).collect(Collectors.toList());

    // 将购物车对象批量添加到数据库
    shoppingCartMapper.insertBatch(shoppingCartList);
}
```

用到了Java8的流式API操作

### 校验收货地址是否超出配送范围

使用的百度地图开放平台的API

### 订单状态定时处理-- Spring Task

- 通过定时任务每分钟检查一次是否存在支付超时订单（下单后超过 15 分钟仍未支付则判定为支付超时订单），如果存在则修改订单状态为 “已取消”
- 通过定时任务每天凌晨 1 点检查一次是否存在 “派送中” 的订单，如果存在则修改订单状态为 “已完成”

使用Spring Task

启动类上加注解@EnableScheduling，

自定义定时任务类，类上加@Component，方法上加@Scheduled(cron = "0/5 * * * * ?")

其中，Cron表达式[在线生成网址](https://cron.qqe2.com/)，可以定义定义任务触发的时间

### 来单提醒--WebSocket

语音播报+弹出提示框

流程：使用WebSocket建立连接，客户交完钱，后端就往网页上发消息，网页解析消息，判断是来单提醒还是催单，然后发出相应的播报

```java
//通过websocket向客户端浏览器推送消息
    Map map = new HashMap();
    map.put("type", 2);//1表示来单提醒，2代表用户催单
    map.put("orderId", id);
    map.put("content", "订单号：" + orders.getNumber());
    webSocketServer.sendToAllClient(JSON.toJSONString(map));
```



