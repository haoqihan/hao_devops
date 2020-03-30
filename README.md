#### nmap 模块
```shell 
python-nmap 模块 存活的设备IP列表(live_ip.list)

```
#### telnetlib 模块
```shell script
Linux 服务主机的IP列表(linux_ip.list)
非Linux 服务主机的IP列表(nolinux_ip.list)
```

```shell script
ssh -l test 192.168.1.1 -p 22

sshd.config 确认开启 PubkeyAuthentication、RSAuthentication

```
```shell script
# 获取主机名的命令
hostname
uname -a
cat /etc/sysconfig/network

# 获取系统版本
cat /etc/issue
cat /etc/redhat-release
uname 
lsb_release

# 获取mac地址
linux 系统
    cat /sys/class/net/eth*/address
    ifconfig eth0
    ip a
ESXI 
  esxcfg-vmknic -l
  
# 通用命令
cat /sys/class/net/[^vtlsb]*/address || esxcfg-vmknic -l | awk '{print $8}' | grep ':'


# 获取服务器硬件机型
dmidecode -s system-manufacturer
dmidecode -s system-product-name

# 获取序列号
dmidecode -s system-serial-number

```
```shell script
# ansible 基础和安装
Ansible 是python中的一套模块,系统中的一套自动化工具,可以用来作为系统管理,自动化命令 等任务

# 安装
pip3 install ansible
# ansible 的配置文件
/etc/ansbile
    ansible.cfg  执行需求的全局性.默认的配置文件
    hosts 默认的主机资产清单文件




```
ansible.cfg
```shell script
# 指定 ansible的配置文件
export ANSIBLE_CONFIG=/etc/ansible/ansible.cfg

ansible 配置文件 (优先级)
    ANSIBLE_CONFIG
    ./ansible.cfg
    ~/ansible.cfg
    /etc/ansible/ansible.cfg
# 常用配置项

1. inventory
   资源清单的位置 inventory = /root/ansible/hosts
2.library
    ansible的操作动作
3. forks
    设置默认情况下ansible最多能有多少个进程同时工作，默认是5个
    forks = 5
4. sudo_user
    设置默认执行命令的用户,可以在playbook中重新设置这个参数
    sudo_user = root
5.remote_port
    这个是指定连接被关联节点的管理端口,默认是22
    remote_port = 22
6.host_key_checking
    设置是否检查ssh主机秘钥,可以设置为True或False
    host_key_checking = False
7.timeout
    设置ssh连接的超时时间,单位秒
    timeout = 20
8.login_path
    ansible默认是不记录日志的,如果需要记录,可以设置
    log_path /var/log/ansible.log
9.private_key_file
    在使用ssh公钥进行登录的时候,使用的秘钥路径
    private_key_file = /path/to/file.pem

```
hosts 配置文件
```shell script
# 配置方式
(1) 第一种( 如果想用使用密码登录需要下载 sshpass )
[group_name]
192.168.1.1:22  ansible_ssh_user=root ansible_ssh_pass='111111'
ssh用户+ssh密码
(2) 第二种
[group_name]
192.168.1.1:22  ansible_ssh_user=root ansible_ssh_private_key_file=/etc/path
ssh用户+ssh秘钥
(3) 第三种
[group_name]
test1 ansible_ssh_host=192.168.1.1 ansible_ssh_port=22 ansible_ssh_user=root ansible_ssh_private_key_file=/etc/path
别名+ssh用户+ssh秘钥


# 简单查看方式
(1) 列出所有主机组的所有成员
  ansible all --list-hosts
(2) 列出指定主机组的成员
  ansible test --list-hosts

```

ansible的ad-hoc模式
```shell script
(1) 什么是ad-hoc 模式
  ad-hoc 就是"临时命令模式"
  ansible有两种模式 ad-hoc 和 playbook

(2) ad-hoc 模式使用的场景
  1.查看某个进程是否启动
  2.拷贝指定日志到本地
  

(3)ad-hoc 模式的命令使用
  ansible <host-pattern> [options]
  host-pattern:匹配主机名或者主机组名
  options: 包括执行的模块和执行命令参数
  ansible 192.168.1.* -a "ls /"
  ansible group1 -a "ls /"
  ansible 别名 -a 'ls /'
  
(4)ad-hoc 模式常用模块
```
|模块名|作用|用例|
|---|---|---|
|command | 默认模块| ansible webservers -a "/sbin/reboot" -f 10|
|shell|执行shell命令|ansible test -m shell -a "echo $HOSTNAME"|
|file transfer| 文件传输 | ansible test -m copy -a "src=/etc/hosts dest=/tmp/hosts"|
|managing packages| 管理软件包| ansible test -m yum -a "name=nginx state=present" present表示有不安装，没有才安装|
|user and groups| 用户和组| ansible test -m user -a "name=jeson password=123456"|
|Deploying| 部署模块| ansible test -m git -a "repo=https://github.com/xxx dest=/opt/xxx version=HEAD"|
|managing services| 服务管理| ansible test -m service -a "name=nginx state=started"|
|Background Operations| 后台运行| ansible test -B 3600 -a "/usr/bin/running_operation --do-stuff"|
|gathering facts| 搜集系统信息| ansible test -m setup|

### ansible playbook模式及语法
#### 什么是playbook及组成
```shell script
    play :定义的是主机的角色
    task: 定义的是具体执行的任务
    playbook:由一个或多个play组成,一个play可以包含多个task
```
#### playbook的优势
```shell script
    1.功能比adhoc更全
    2.控制好依赖
    3.展现更直观
    4.持久使用
```
#### playbook的配置语法
```shell script
1.基本使用
  1.playbook的基本使用
    ansible-playbook playbook.yml [options]
    options
      -u  # ssh 链接的用户名
      -k  # ssh登录的密码
      -s  # sudo到root用户
      -C  # 模拟执行，但不会真执行
      -e  # 传入的变量
      -i  # 指定ansible的hosts的文件路径
      --list-hosts # 打印有哪些主机会执行playbook
      --list-task  # 列出该playbook中会执行的task
      --private-key # 私钥路径
      --step   # 同一时间只执行一个task
      -v # 输出详细信息
2.执行结果返回
  红色:表示有task执行失败或者提醒的信息
  黄色:表示执行了且改变了远程主机状态
  绿色:表示执行成功
      
    
2.yaml语法和变量
  1.yaml语法
    大小写敏感
    使用缩进表示层级关系,(只能使用空格不能使用tab键)
    yaml文件以 --- 作为文件开始
  2.yaml支持的数据结构
    字典
      {name:xxx}
    列表
      - a
      - b
      - c
    纯量
      数字
      布尔
      字符串
  3.yaml变量的应用
    myname:json
    name:"{{ myname }}"

  4.playbook变量
    playbook 的yaml文件中定义变量赋值
    --extra-vars 执行参数赋值给变量
    在文件中定义变量(hosts中,[group2:vars] xxx=xxx)
    注册变量
      register 关键字可以存储指定命令的输出结果到一个自定义变量中
      - name: get times 
        command: date
        register: date_output
    
3.基本语句
  1.条件语句
    when 语句
      tasks:
        - name :"touch flag file"
          command: "touch /tmp/this_is_{{ansible_distribution}}_system"
          when: (ansible_distribution == "Centos" and ansible_distribution_major_version == "6") or
                (ansible_distribution == "Debian" and ansible_distribution_major_version == "7")
      
```
#### 循环语句
|循环类型|关键字|
|---|---|
|标准循环|with_items|
|嵌套循环| with_nested|
|遍历字典|with_dict|
|并行遍历列表|with_together|
|遍历列表和索引|with_indexed_items|
|遍历文件列表的内容|with_file|
|变量文件目录|with_fileglob|
|重试循环|until|
|查找第一个匹配文件|with_first_found|
|随机选择|with_random_choice|
|在序列中循环|with_sequence|

#### 循环语句+条件语句
```yaml
- hosts: xxx
  remote_user: root
  tasks:
    - debug: msg="{{ item.key }} is the winner"
      with_dict: {"json":{'english':60,'chinese':30},"tom":{'english':70,'chinese':40}}
      when: item.value.english >= 70
```

### 异常处理和相关操作
#### 异常处理
##### 忽略错误
    默认会检查命令和模块的返回状态，遇到错误就终端playbook的执行
    加入参数：ignore_errors:yes
##### 自定义错误
    failed_when: process_count > 3  抛出错误
    
##### 自定义change状态
    change_when: false
    

#### tags标签
##### 打标签
    对一个对象打标签
    对多个对象打标签
    打标签的对象包括：单个task任务、include对象、roles对象
    
##### 使用标签
```yaml
- hosts:xxx
  remote_user: root
  tasks:
    - name:create file
      shell: touch ./root
      tags:
        - tag1
        - tag2
    - name: create file2
      shell: touch ./root2
      tags:
        - tag3
```
-t: 执行指定的tag标签任务

--skip-tags: 执行--skip-tags 之外的标签任务


### roles角色
#### include的用法
include_tasks/include:动态的包含tasks任务列表执行
#### 为什么需要用到roles
是一种利用在playbook中的剧本配置模式，有着自己特定结构

```markdown
production        # 正式环境的inventory文件
staging           #测试环境用得inventory文件
group_vars/  # 机器组的变量文件
      group1        
      group2
host_vars/   #执行机器成员的变量
      hostname1     
      hostname2
================================================
site.yml                 # 主要的playbook剧本
webservers.yml    # webserver类型服务所用的剧本
dbservers.yml       # 数据库类型的服务所用的剧本

roles/
      webservers/        #webservers这个角色相关任务和自定义变量
           tasks/
               main.yml
           handlers/
               main.yml
           vars/            #
                main.yml
        dbservers/         #dbservers这个角色相关任务和定义变量
            ...
      common/         # 公共的
           tasks/        #   
                main.yml    # 
           handlers/     #
                main.yml    # handlers file.
           vars/         # 角色所用到的变量
                main.yml    # 
===============================================
      templates/    #
            ntp.conf.j2 # 模版文件
      files/        #   用于上传存放文件的目录
            bar.txt     #  
            foo.sh      # 
      meta/         # 角色的依赖
            main.yml    # 
```
#### nginx编译安装
```
## 主目录
|--- ansible.cfg
|--- files          存放上传文件
|--- production     线上的主机配置文件
|--- roles          roles角色执行
|--- staging        线下测试环境使用的主机配置文件
|--- templates      模板(配置，html)
 ——- webserver.yml  web服务相关主执行文件

# files目录
|--- index.html  测试使用的html文件
|--- nginx       系统init中，控制nginx启动脚本
 —— nginx.tar.gz  nginx安装包文件

# templates目录结构
|
 - nginxs.conf   nginx的自定义conf文件

# roles目录
|
|-- apache 
|-- command
|   |--- tasks
|           |-- main.yml
|    |--- vars
|           |---- main.yml
|--- meta
|--- nginx
|    |-- handlers   
|         |--- main.yml
|    | tasks
        |-- basic.yml
        |-- main.yml
        | nginx.yml
      |-- vars
            -- main.yml
-- tasks   


```




```shell script
. /etc/rc.d/init.d/functions
if [ -L $0 ];then
    initscript=`/bin/readlink -f $0`
else
    initscript=$0
fi
sysconfig=`/bin/basename $initscript`
if [ -f /etc/sysconfig/$initscript ];then
    . /etc/sysconfig/$$initscript
fi

nginx=${NGINX:-/opt/app/nginx/sbin/nginx}
prog=`/bin/basename $nginx`
conffile=${CONFFILE:-/ope/app/nginx/conf/nginx.conf}
lockfile=${LOCKFILE:-/var/lock/subsys/nginx}

```


```shell script
InventoryManager
    1.添加主机到指定主机组 add_host()
    2.查看主机组资源 get_groups_dict()
    3.获取指定的主机对象 get_host()
VariableManager
    1.查看主机变量方法 get_vars()
    2.设置主机变量方法: set_host_variable()
    3.添加扩展变量 extra_vars
      variable_manager.extra_vars = {}

ad-hoc


```

























