# Sunlogin_RCE-GUI-
向日葵漏洞图形化利用工具

纯菜鸟第一次写图形化工具，各位大佬看看就好，勿喷。

代码写的比较垃圾，python写的打包也比较麻烦，后期优化更新之后会放开源码。



初版主要长这样，集成了获取配置信息（读取向日葵的配置文件）和执行命令功能。

<img src="img/1.jpg" alt="1" style="zoom:50%;" />

## 获取配置信息

该模块主要通过powershell、注册表、findstr命令来获取目标站点的配置文件信息；

该模块集成了实战过程中遇到过的各个向日葵配置文件路径。

<img src="img/2.jpg" alt="2" style="zoom:50%;" />

## 执行系统命令

该模块主要通过cmd和powershell来执行系统命令；

发现其他方法的话后续会进行添加。

<img src="img/3.jpg" alt="3" style="zoom:50%;" />



# ⚠️ 免责声明

​	此工具仅作为网络安全攻防研究交流，请使用者遵照网络安全法合理使用！ 如果使用者使用该工具出现非法攻击等违法行为，与本作者无关！
