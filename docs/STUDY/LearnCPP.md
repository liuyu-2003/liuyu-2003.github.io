# C++学习
1. 循环n次，且n以后不再用
```
int n;
cin >> n;
while (n -- )
{

}
```

2. scanf效率比cin高，但是cin简单好打，数值大于十万用scanf
3. 如果主函数里面的数组太大（存栈里），可以放在外面做全局变量（存堆里），此时数组里面的数全为0