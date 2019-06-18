# zabbix-ipmi

IPMI LLD and check for zabbix  
Zabbix通过IPMI协议监控服务器硬件，使用python脚本自动发现风扇、电源、硬盘、温度等监控项。

## 使用说明

1. 安装freeipmi

+ CentOS/Redhat

```shell
sudo yum -y install freeipmi
```

+ Ubuntu

```shell
sudo apt-get install freeipmi-tools
```

+ 源码安装

freeipmi[官网]: https://www.gnu.org/software/freeipmi/download.html

2. 将python文件下载后放入外部脚本目录（/lib/zabbix//lib/zabbix/externalscripts/）,给脚本相应权限。

```shell
sudo chown zabbix:zabbix /lib/zabbix//lib/zabbix/externalscripts/ipmi*.py
sudo chmod a+x /lib/zabbix//lib/zabbix/externalscripts/ipmi*.py
```

3.注意给临时文件赋予zabbix的读写权限，脚本中为/var/tmp/

4. 导入监控脚本，添加主机。接口保持不变，设置宏，左侧填入{$SERVER}，右侧填入设备的IP地址（管理地址）。
