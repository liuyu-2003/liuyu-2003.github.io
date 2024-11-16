# Java

## 基本数据类型

|      | byte | short | int  | long | float | double | char | boolean |
| ---- | ---- | ----- | ---- | ---- | ----- | ------ | ---- | ------- |
| 字节 | 1    | 2     | 4    | 8    | 4     | 8      | 2    |         |
| 位数 | 8    | 16    | 32   | 64   | 16    | 32     | 16   | 1       |

### String

String是被声明为final的，所以只要对String操作，就会产生新的String对象

StringBuffer解决了String在拼接的时候产生的无用对象，线程安全

StringBuilder线程不安全，但是性能好

## final关键字

不能再改变这个引用了，编译器会检查，变了就报编译错

放在类，方法，成员变量，局部变量上

1. 放类上：说明类的功能完备了，不允许被继承

2. 放方法上：说明方法的功能完备了，不允许子类的方法去重写，编译更快

3. 放变量上：通常和static关键字一起用，作为常量

## 成员变量和局部变量

规范：定义变量的时候，作用域尽可能的小。

### 成员变量在**类**中定义

成员变量包含**静态变量**和**实例变量**

1. 静态变量使用static修饰，访问的时候直接“类.变量名”

2. 实例变量，访问的时候需要先new一个实例才能用，"实例.变量名"

3. 静态方法中不能使用非静态变量或方法

### 局部变量在**方法**中定义

局部变量包含形参、方法局部变量、代码块局部变量

局部变量可以和成员变量重名，如果想用成员变量，就用"this."或者"类名."

## Java异常

![Java异常类结构图](/Users/liuyu/noteBook/assets/Java异常类结构图.png)

1. RuntimeException(Unchecked Exception)：编译时不强制处理，程序错误，比如空指针访问
2. 非RuntimeException(检查性异常Checked Exception)：编译时**强制**让程序员处理，通常是外部错误，比如文件找不到

错误(Error)不属于异常：栈溢出、内存耗尽等

### 异常处理

对于非运行时异常，必须使用throws

throw：抛出异常
`throw new IllegalArgumentException("Number must be positive");`

throws：声明可能会抛出什么异常，让使用该方法的对象去处理
`public void readFile(String filePath) throws IOException {`

try-catch：处理异常

注意：

不要再finally里面写return，因为try里面return的返回值是先暂存到本地变量里面，然后执行finally，就给覆盖了

```java
try{return a;} finally{return b;} //return b
```

对于需要关闭资源的使用：try-with-resources

```java
try(t1;t2;t3) {
...
} catch (xxx e){
...
}
```

## I/O流

用于内存和硬盘的交互

### 分为字节流和字符流

字节流通过 byte ，即8位传输，字符流通过 char ，即16位传输，最小传输单位都是字节

### 字节流输入输出

1. InputStream，是一个抽象类

FileInputStream 是它的常用子类

使用`read()`控制输入

```java
while ((n = input.read()) != -1) {
            System.out.println(n);
        }
```

2. OutputStream

FileOutputStream 是它的常用子类

使用`write()`控制输出`output.write("Hello".getBytes("UTF-8"));`

### 字符流输入输出

1. Reader

FileReader 是它的常用子类

2. Writer

FileWriter 是它的常用子类

### Files 工具类

对于简单的小文件读写操作，可以使用`Files`工具类简化代码。不可一次读入几个G的大文件。

使用`readString()`和`writeString()`

### BIO->NIO->AIO

1. BIO，同步阻塞，面向流的。处理不了高并发，读写都在一个线程里面
2. NIO，同步非阻塞，面向缓冲区的。核心是Channel(通道)，Buffer(缓冲区)，Selector（多路复用器）
   （成熟的基于 NIO 的网络编程框架：Netty）
3. AIO，异步非阻塞，回调机制，干完就返回

## 深浅拷贝

实现深浅拷贝有两个方法：

1. 实现Cloneable接口，重写clone方法
2. 实现Serializable接口，通过序列化和反序列化克隆

![深浅拷贝](/Users/liuyu/noteBook/assets/深浅拷贝.png)

浅拷贝就是创建一个新的对象，把原来的引用赋给它，共享引用

```java
public class Address implements Cloneable{
    private String name;
    // 省略构造函数、Getter&Setter方法
    @Override
    public Address clone() {
        try {
            return (Address) super.clone();
        } catch (CloneNotSupportedException e) {
            throw new AssertionError();
        }
    }
}

public class Person implements Cloneable {
    private Address address;
    // 省略构造函数、Getter&Setter方法
    @Override
    public Person clone() {
        try {
            Person person = (Person) super.clone();
            return person;
        } catch (CloneNotSupportedException e) {
            throw new AssertionError();
        }
    }
}
```

深拷贝会完全复制整个对象

```java
public class Person implements Cloneable {
    private Address address;
    // 构造函数和 Getter & Setter 省略
    @Override
    public Person clone() {
        try {
            Person person = (Person) super.clone();
            // 深拷贝 Address 对象,this（可选）就是当前要深拷贝的对象
            person.address = this.address.clone();
          	// 或者下面这个方法也可以
          	person.setAddress(person.getAddress().clone());
            return person;
        } catch (CloneNotSupportedException e) {
            throw new AssertionError();
        }
    }
}
```

## 反射

在程序运行的时候，可以知道任意类的所有信息，可以随便调用任意对象的属性和方法，非常动态

1. 用`Class.forName()`传入类的全路径可以得到类
2. 如果有对象了，可以通过`对象.getClass()`得到类

```java
//方法1
try {
    Class<?> clazz = Class.forName("com.example.MyClass"); // 替换为你的类的全路径
    System.out.println("类名: " + clazz.getName());
} catch (ClassNotFoundException e) {
    e.printStackTrace();
}
//方法2
MyClass myObject = new MyClass();
Class<?> clazz = myObject.getClass();
System.out.println("类名: " + clazz.getName());

```

1. 用Class类的`newInstance()`或者Constructor对象的`newInstance()`可以**创建对象**，编译时不知道类名也行
2. 用Method类的`getMethod()`可以**得到方法**，再使用`invoke()`可以**执行对象的方法**
3. 用Field类的`getFields()`或者`getDeclaredFields()`可以**得到属性**，再使用`get()`和`set()`可以**访问和修改对象的属性**

注：

1. Class类的`newInstance()`只能使用无参构造函数，而后者可以传入参数。
2. `getFields()`能获取类及其父类的**公共属性**，`getDeclaredFields()`**仅**对类本身的属性有效果

```java
// 用处1
try {
    Class<?> clazz = Class.forName("com.example.MyClass");
    MyClass myObject = (MyClass) clazz.newInstance(); // 只能使用无参构造函数
} catch (Exception e) {
    e.printStackTrace();
}

try {
    Class<?> clazz = Class.forName("com.example.MyClass");
    Constructor<?> constructor = clazz.getConstructor(String.class); // 获取有参构造函数
    MyClass myObject = (MyClass) constructor.newInstance("parameter"); // 创建对象并传入参数
} catch (Exception e) {
    e.printStackTrace();
}
// 用处2
try {
    MyClass myObject = new MyClass();
    Method method = myObject.getClass().getMethod("myMethod"); // 替换为你的方法名
    method.invoke(myObject); // 调用方法
} catch (Exception e) {
    e.printStackTrace();
}
// 用处3
try {
    MyClass myObject = new MyClass();
    Field field = myObject.getClass().getDeclaredField("myField"); // 替换为你的字段名
    field.setAccessible(true); // 如果字段是私有的，设置可访问性
    // 获取字段值
    Object value = field.get(myObject);
    System.out.println("字段值: " + value);
    
    // 修改字段值
    field.set(myObject, "newValue");
    System.out.println("修改后的字段值: " + field.get(myObject));
} catch (Exception e) {
    e.printStackTrace();
}
```

### 应用场景

1. 有时候用MySQL有时候用SQL Server，就可以动态的加载驱动类
2. 配置文件加载

## 面向对象

什么是面向对象？

​	将事物封装成对象，事物有特征和行为，对应对象的属性和方法

​	通过对象之间的交互来完成程序的功能

为什么要面向对象？

​	对于需求的变化，封装和继承可以很好的解决

面向对象的三大特性：封装继承多态

​	封装：将属性和方法封装到对象里面，通过接口进行交互，简化编程

​	继承：子类共享父类的数据结构和方法，这样就代码复用了，建立了类与类的层级结构，代码结构更清晰

​	多态：也就是重载和重写，这样如果有新功能代码就很容易拓展了

## 接口和抽象类

```java
//抽象类
abstract class Person {
    public abstract void run();
}

//接口：一个抽象类没有字段，所有方法全部都是抽象方法
```

接口被实现，抽象类被继承

接口可以定义方法但是不能写方法的实现，抽象类可以写方法的实现

接口强调约束，你实现了我，就具有了对应的行为；抽象类强调从属关系，就是提高代码复用的

接口的成员变量在子类里面不能改，因为变量类型只能是`public static final`

抽象类的成员变量类型随意，并且可以在子类里面重新定义和赋值

## 包装类

### 装箱拆箱

装箱：基本数据类型赋值到包装类上

拆箱：包装类的实例对象赋值到基础数据类型的变量上

自动装箱：

1. 赋值时
2. 方法调用时：如果方法声明的形参是包装类对象，而调用的时候传入的是基本数据类型，就自动装箱了

自动拆箱：如果方法的返回值是包装类对象，但是在调用它的方法中赋值到了基本数据类型的变量上，就自动拆箱了

### 包装类用途

1. 很多方法需要包装类对象才能用，也就是把数据和处理数据的方法包装了起来，比如`Integer.parseInt();`

2. Java很多方法或者类处理的是类，比如`new ArrayList<Integer>();`

### 和基本数据类型的不同

**用途**：除了定义一些常量和局部变量之外，在其他地方比如方法参数、对象属性中很少会使用基本类型来定义变量。
并且，包装类型可用于泛型，而基本类型不可以。

**存储方式**：基本数据类型的局部变量存放在 Java 虚拟机栈中的局部变量表中，基本数据类型的成员变量（未被 `static` 修饰 ）存放在 Java 虚拟机的堆中。包装类型属于对象类型，几乎所有对象实例都存在于堆中。

**占用空间**：相比于包装类型（对象类型）， 基本数据类型占用的空间往往非常小。

**默认值**：成员变量包装类型不赋值就是 `null` ，而基本类型有默认值且不是 `null`。

**比较方式**：对于基本数据类型来说，`==` 比较的是值。对于包装数据类型来说，`==` 比较的是对象的内存地址。
所有整型包装类对象之间值的比较，全部使用 `equals()` 方法。

## Super和This

情况1: 在构造函数里用时

​	super: 调用父类的构造函数。

​	this: 调用同一类的其他构造函数。

​	他们必须写在构造函数的第一行

情况2: 在方法里用时

​	super: 引用当前对象的直接父类中的成员

​	this: 方法中的参数与成员变量的名字相同的时候，使用this来引用成员变量

## StreamAPI

`.stream`：负责Stream流的开启

`.collect`：负责Stream流的关闭和获取最终结果

```
Collectors.toList()：将流中的元素收集到一个 List 中。
Collectors.toSet()：将流中的元素收集到一个 Set 中。
Collectors.toMap()：将流中的元素收集到一个 Map 中。
```

`.map`：接收一个函数，对流中每一个元素执行操作，并返回一个元素。最终返回一个新的流，返回转换后的元素们

可以用于把一种类型的对象转换成另一种类型的对象，比如把实体对象转换成DTO就能传输了。

```java

public class UserMappingExample {
    public static void main(String[] args) {
        List<User> users = Arrays.asList(
                new User("Alice", 30),
                new User("Bob", 25)
        );

        List<UserDTO> userDTOs = users.stream()
                .map(user -> new UserDTO(user.getName(), user.getAge())) // 转换为 UserDTO
                .collect(Collectors.toList());

        System.out.println(userDTOs);
    }
}
```
