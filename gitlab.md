#### 什么是gitlab
- gitlab是一个开源的分布式版本控制系统
- 开发语言： Ruby
- 功能： 管理项目源代码、版本控制、代码复用与查找
### github 与 gitlab
- github分布式在线版本托管仓库，个人版可直接在线免费试用，企业版本收费且需要服务器安装
- gitlab分布式在线代码仓库托管软件、分社区版与企业收费版，都需要服务器安装
### gitLab的优势和应用场景
- 开源免费，适合中小型公司将代码放置到该系统中
- 差异化的版本管理，离线同步以及强大分支管理功能
- 便捷的GUI操作界面以及强大账户权限管理功能
- 集成度很高，能集成绝大多数的开发工具
- 支持内置HA，保证在高并发下依旧实现高可用
### gitlab主要构成
- Nginx静态Web服务器
- Gitlab-workhores 轻量级的反向代理服务器
- Gitlab-shell 用于处理git命令和修改authorized keys列表
- Logrotate 日志文件管理工具
- Postgresql 数据库
- Redis缓存服务器
### gitLab的工作流程
- 创建并克隆仓项目
- 创建项目某Feature分支
- 编写代码并提交到该分支
- 推送该项目分支至远程服务器
- 进行代码检查并提交Master主分支合并申请
- 项目领导审查代码并确认合并申请

## gitlab安装配置管理
### 安装Gitlab前系统配置准备工作
#### 1.关闭firewalld防火墙
```shell script
systemctl stop firewalld
systemctl disable firewalld
```
#### 2.关闭SELINUX并重启系统
```shell script
vi /etc/sysconfig/selinux

SELINUX=disabled

reboot
```
#### 3.安装Omnibus Gitlab-ce package
```shell script
1.安装Gitlab组件
yum -y install curl policycoreutils openssh-server openssh-clients postfix
2.配置yum仓库
curl -sS https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.rpm.sh | sudo bash 

3.启动postfix邮件服务
systemctl start postfix  && systemctl enable postfix
4.安装gitlab-ce社区版
yum install -y gitlab-ce
```
#### 4.安装配置管理
```shell script
1.证书创建与配置加载
mkdir -p /etc/gitlab/ssl
openssl genrsa -out "/etc/gitlab/ssl/gitlab.example.com.key" 2048
openssl req -new -key "/etc/gitlab/ssl/gitlab.example.com.key" -out "/etc/gitlab/ssl/gitlab.example.com.csr"
  cn
  bj
  bj
  回车
  回车
  gitlab.example.com
  admin@example.com
  123456
  回车
openssl x509 -req -days 365 -in "/etc/gitlab/ssl/gitlab.example.com.csr" -signkey  "/etc/gitlab/ssl/gitlab.example.com.key" -out "/etc/gitlab/ssl/gitlab.example.com.crt" 
openssl dhparam -out /etc/gitlab/ssl/dhparams.pem  2048
chmod 600 *

2.Nginx SSL代理服务配置
vi /etc/gitlab/gitlab.rb

external_url 'https://gitlab.example.com'
nginx['redirect_http_to_https'] = true
nginx['ssl_certificate'] = "/etc/gitlab/ssl/gitlab.example.com.crt"
nginx['ssl_certificate_key'] = "/etc/gitlab/ssl/gitlab.example.com.key"
nginx['ssl_dhparam'] = /etc/gitlab/ssl/dhparams.pem




3.初始化Gitlab相关服务并完成安装
gitlab-ctl reconfigure

vi /var/opt/gitlab/nginx/conf/gitlab-http.conf

server_name ......
rewrite ^(.*)$ https://$host$1 permanent;

gitlab-ctl restart


亲测无用(还不如docker搭建的方便和快呢)



```


