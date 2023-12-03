# 解决Windows与Ubuntu双系统时，时间不统一问题

**问题发现**：在使用完毕Ubuntu切换回Windows后，发现右下角的时间显示与现实不符

**问题原因**：Windows 与 Linux 看待硬件时间的方式不同。Windows 把电脑的硬件时钟（RTC）看成是本地时间，即 RTC = Local Time，Windows 会直接显示硬件时间；而 Linux 则是把电脑的硬件时钟看成 UTC 时间，即 RTC = UTC，那么 Linux 显示的时间就是硬件时间加上时区。

- RTC：Real-Time Clock，即实时时钟，在计算机领域作为硬件时钟的简称。
- UTC：Universal Time Coordinated，即协调世界时。UTC 是以原子时秒长为基础，在时刻上尽量接近于 GMT 的一种时间计量系统。为确保 UTC 与 GMT 相差不会超过 0.9 秒，在有需要的情况下会在 UTC 内加上正或负闰秒。UTC 现在作为世界标准时间使用。
- GMT：Greenwich Mean Time，即格林尼治标准时间，也就是世界时。GMT 以地球自转为基础的时间计量系统，但由于地球自转不均匀，导致 GMT 不精确，现在已经不再作为世界标准时间使用。

简单来说：

Windows认为：BIOS时间就是当地时间，所以Windows会直接显示BIOS时间

Ubuntu认为：BIOS时间是UTC时间，所以Ubuntu会将BIOS时间加上8小时后再显示出来（在中国）



**问题解决**：使硬件时钟(RTC)以协调世界时(UTC)运行

1. 在键盘上按下`Win+R`打开**运行**程序
2. 输入`regedit`命令打开注册表编辑器
3. 定位到`计算机\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\TimeZoneInformation`目录下，新建一个`DWORD`类型，名称为`RealTimeIsUniversal`的键，并修改键值为1即可。

PS：这是最好的方法，另一种在Linux系统的终端下输入`timedatectl set-local-rtc 1 --adjust-system-clock`也可以实现时间同步，但是会跳出Warning警告，因为 RTC 时钟统一使用协调世界时（UTC）更恰当，如果在Linux下执行了该指令，会导致夏令时无法自动切换。而本文方法无论在Windows还是Linux下，系统都会根据当前的时区和夏令时规则自动调整显示的时间。**但是，请注意，这个设置会导致无法通过控制面板修改系统时间。**