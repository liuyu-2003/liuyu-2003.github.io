# Java并发

## 进程和线程

**进程**是操作系统进行**资源分配**的最小单元，**线程**是操作系统进行**运算调度**的最小单元。

main函数就是启动JVM进程，而 main 函数所在的线程就是这个进程中的一个线程，也称为主线程

## 线程

### 怎样创建线程

继承Thread类，重写其run()方法，run()方法中定义了线程执行的具体任务。创建该类的实例后，通过调用start()方法启动线程。

```java
class MyThread extends Thread{
  public void run(){
    ...
  }
  public static void main(String args[]) {
    MyThread t = new MyThread();
    t.start();
  }
}
```

可是如果该方法还想继承其他父类怎么办？

实现Runnable接口

```java
class MyThread implements Runnable{
	public void run(){
    ...
  }
  public static void main(String args[]) {
    Thread t = new Thread(new MyThread());
    t.start();
  }
}
```

前面两种都不能返回方法，所以：实现Callable接口。
需将它包装进一个FutureTask，因为Thread类的构造器只接受Runnable参数，而FutureTask实现了Runnable接口。

```java
class MyCallable implements Callable<Integer> {
    @Override
    public Integer call() throws Exception {
        // 在这里执行线程代码
        return 1;
    }

    public static void main(String[] args) {
        MyCallable task = new MyCallable();
        FutureTask<Integer> futureTask = new FutureTask<>(task);
        Thread t = new Thread(futureTask);
        t.start();

        try {
            Integer result = futureTask.get();
            System.out.println("Result" + result);
        } catch (InterruptedException | ExecutionException e) {
            e.printStackTrace();
        }
    }
}
```

这Runnable和Callable两种方法需要频繁创建和销毁线程，怎样可以提高性能呢？

使用线程池（Executor框架）。

```java
class Task implements Runnable {
    @Override
    public void run() {
        //线程执行代码
    }
}

public static void Main(String[] args) {
  	// 建议使用new ThreadPoolExecutor 手动创建线程池
  	// 不建议使用Executors工具类
    ExecutorService executor = Executors.newFixedThreadPool(10);
    for (int i = 0; i < 100; i++) {
        executor.submit(new Task());
    }
    executor.shutdown();
}
```

线程池可以重用预先创建的线程，避免了线程创建和销毁的开销。
线程池能够有效控制运行的线程数量，防止因创建过多线程导致的系统资源耗尽（如内存溢出）。

### 线程状态

- New：新创建的线程，尚未执行；
- Runnable：运行中的线程，正在执行`run()`方法的Java代码；
- Blocked：运行中的线程，因为某些操作被阻塞而挂起；
- Waiting：运行中的线程，因为某些操作在等待中；
- Timed Waiting：运行中的线程，因为执行`sleep()`方法正在计时等待；
- Terminated：线程已终止，因为`run()`方法执行完毕。

刚`new Thread()`时，线程状态为 New

当使用`t.start()`了，线程开始运行`run()`方法，则线程状态为 Runnable

线程进入`synchronized()`中，但是没有拿到锁，则 Runnable------>Blocked

当使用`Object.wait()`方法、`Thread.join()`方法，线程进入 Waiting

当使用`Object.notify()`或`Object.notifyAll()`方法，则 Waiting------>Runnable

### 线程池

ThreadPoolExecutor 的参数

![线程池结构图](/Users/liuyu/noteBook/assets/线程池结构图.png)

`corePoolSize` : 任务队列未达到队列容量时，最大可以同时运行的线程数量。

`maximumPoolSize` : 任务队列中存放的任务达到队列容量的时候，当前可以同时运行的线程数量变为最大线程数。

`workQueue`: 新任务来的时候会先判断当前运行的线程数量是否达到核心线程数，如果达到的话，新任务就会被存放在队列中。

`keepAliveTime`:线程池中的线程数量大于 `corePoolSize` 的时候，如果这时没有新的任务提交，核心线程外的线程不会立即销毁，而是会等待，直到等待的时间超过了 `keepAliveTime`才会被回收销毁。

`unit` : `keepAliveTime` 参数的时间单位。

`threadFactory` :executor 创建新线程的时候会用到。

`handler` :拒绝策略

### 如何启动线程

启动线程的通过Thread类的`start()`。

### 如何停止线程

异常法停止：线程调用`interrupt()`，run 方法中判断当前对象的`interrupt()`状态，如果是中断状态则抛出异常，就停止了。

在沉睡中停止：线程调用`sleep()`，然后调用`interrupt()`，interrupt 会将阻塞状态的线程中断。抛中断异常。

`stop()`暴力停止：线程调用`stop()`，已弃用，有可能导致清理不干净。

使用 return 停止线程：线程调用`interrupt()`，run 方法中判断当前对象的`interrupt()`状态，如果是中断状态则 return，就停止了

### 线程怎么通信

volatile

synchronized

interrupt

wait、notify、notifyall

join：比如现在在main线程中开了一个t线程，执行`t.join()`当前线程等待t线程结束

### notify和notifyAll的异同

同样是唤醒等待的线程，同样最多只有一个线程能获得锁，同样不能控制哪个线程获得锁。

区别：

notify：唤醒一个线程，其他线程依然处于wait的等待唤醒状态，
如果被唤醒的线程结束时没调用notify，其他线程就永远没人去唤醒，只能等待超时，或者被中断。

notifyAll：所有线程退出wait的状态，开始竞争锁，但只有一个线程能抢到
这个线程执行完后，其他线程又会有一个幸运儿脱颖而出得到锁。

事实上，选择控制哪个线程获得锁是由**JVM**决定的。
jvm有很多实现，比较流行的就是hotspot，它是按照“先进先出”的顺序唤醒。

## 怎样保证线程安全

### 加锁

```java
public class Main {

    public synchronized void someMethod(){}//方法

    public static void main(String[] args) {
        synchronized (someObject) {}//代码块
    }
}
```

### 原子类

Java并发库（`java.util.concurrent.atomic`）提供了原子类，如`AtomicInteger`、`AtomicLong`等，这些类提供了原子操作，可以用于更新**基本类型**的变量而无需额外的同步。

```java
AtomicInteger counter = new AtomicInteger(0);
int newValue = counter.incrementAndGet();//将counter+1
```

### ThreadLocal线程局部变量

`ThreadLocal`类可以让每个线程都拥有自己的变量。

```java
ThreadLocal<Integer> threadLocalVar = new ThreadLocal<>();
threadLocalVar.set(10);
int value = threadLocalVar.get();
```

### 并发集合和JUC工具类

这都是在`java.util.concurrent`包中的。

`ConcurrentHashMap`、`ConcurrentLinkedQueue`等
`Semaphore`和`CyclicBarrier`等

### 使用场景

原子类：每当用户登录或登出时，在线人数会更新，多个线程操作这个计数器，但无需复杂逻辑。

并发集合：与原子类相似，原子类是操作基本数据类型，并发集合是操作集合

ThreadLocal：在一个Web应用中，每个线程需要保存当前用户的身份信息。如果不用，可能用户信息被覆盖

锁：可解决所有线程安全问题。两个线程分别操作同一个银行账户，需要确保转账的原子性和数据一致性。

注：volatile并不能解决线程安全问题，只能解决可见性，不能解决原子性

## 锁

### 锁的类型

1. 内置锁synchronized，可以用于方法或代码块，不能响应中断

2. `java.util.concurrent.locks.Lock`接口提供了比`synchronized`更强大的锁。
   `ReentrantLock`是一个实现该接口的例子。

```java
private final ReentrantLock lock = new ReentrantLock();

    public void someMethod() {
        lock.lock();
        try {
            //
        } finally {
            lock.unlock();
        }
    }
```

3. 读写锁ReadWriteLock。
   允许多个读取者同时访问共享资源，但只允许一个写入者。

#### 悲观锁乐观锁

乐观锁（乐观地估计读的过程中大概率不会有写入）
不锁定资源（所以性能好），在更新数据时检查数据是否已被其他线程修改，使用CAS、版本号控制或时间戳来实现

悲观锁（读的过程中拒绝有写入）
访问数据前就锁定资源，比如synchronized和ReentrantLock

自旋锁
不放弃CPU来阻塞，而是线程在等待锁时会持续循环检查锁是否可用。使用CAS来实现。

CAS ： 包含三个操作数 —— 内存位置（V）、预期原值（A）和新值（B）。
当且仅当内存位置的值与预期原值相匹配时，才会将该位置的值更新为新值。
否则，就什么都不做。最后，CAS 操作总是返回该位置的旧值。

适用场景

1. CAS只能保证单个变量操作的原子性，当涉及到多个变量时，CAS是无能为力的，而synchronized则可以通过对整个代码块加锁来处理。
2. 再比如版本号机制，如果query的时候是针对表1，而update的时候是针对表2，也很难通过简单的版本号来实现乐观锁。
3. 竞争激烈使用悲观锁，不然乐观锁总是重试

### 死锁

![死锁](/Users/liuyu/noteBook/assets/死锁.png)

#### 形成死锁的四个条件

互斥条件：该资源任意一个时刻只由一个线程占用。

请求与保持条件：一个线程因请求资源而阻塞时，对已获得的资源保持不放。

不剥夺条件:线程已获得的资源在未使用完之前不能被其他线程强行剥夺，只有自己使用完毕后才释放资源。

循环等待条件:若干线程之间形成一种头尾相接的循环等待资源关系。

#### 怎么解除死锁

死锁发生后，没有任何机制能解除死锁，只能强制结束JVM进程。

#### 怎么检测死锁？

进入 JDK 的 bin 目录，打开 jconsole 连接程序，即可检测死锁

#### 怎么预防和避免死锁？

避免死锁就是在资源分配时，借助于算法（比如银行家算法）对资源分配进行计算评估，使其进入安全状态。

## 应对高并发

**缓存、队列、拆分、池化**

写代码时考虑线程安全：开多线程、加锁、原子类、线程安全集合。

针对 MySQL：集群，主从架构、读写分离，分库分表

针对 Redis：集群，主从架构+哨兵

多台服务器：Nginx 负载均衡，Redis 统一存储 Session，使用消息队列接请求

消息队列：削峰

其他：CDN 缓存静态资源，使用中间件 ES
