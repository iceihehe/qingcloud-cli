# 青云SDK
> 实现青云简单的命令行接口，可以完成创建主机、获取主机、销毁主机操作

### 系统要求
> Linux系统，Python3.7环境

### 安装
> 下载源码到指定目录
> 执行下列命令
> ```shell script
> python setup.py install
> ```

### 自动补全
> 执行下列命令
> ```shell script 
> eval "$(_QING_COMPLETE=source qing)"
> ```

### 使用
#### 配置密钥
>```
> qing config accesskeyid secretaccesskey
>```
#### 创建
> ```shell script
> qing  run-instances instanceid loginpasswd zoneid --instance-type=c1m1  --login-passwd 123456
>```

#### 获取
>```shell script
> qing describe-instances zoneid --instance-id=instanceid
>```

#### 销毁
>```shell script
> qing terminate-instances zoneid --instance-id=instanceid
>```