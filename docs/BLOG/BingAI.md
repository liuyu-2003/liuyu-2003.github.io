# 解决Copilot无法使用问题

**问题描述**：在Microsoft Edge中使用Copilot时：

1. 不断跳转相同的登陆网页，但是登陆不上
2. 显示今天次数用完了
3. 跳转到白屏页面

**问题原因**：账号无法开启New Bing

**问题解决**：

1. 在手机上下载美区的Bing，如果登陆账号后可以使用Copilot，代表该账号正常。（该教程不适用）
2. 如果不可以使用，另外注册一个账号，地区选择美国即可。

**注**：

1. 在Edge中打开bing.com页面，登陆可用账号后，Win11的Copilot也就可以正常使用了。
2. 如果PAC规则不适用，又不想开启全局代理，请添加规则

```
||copilot.microsoft.com
||microsoft.com
||sydney.bing.com
||edgeservices.bing.com
```





