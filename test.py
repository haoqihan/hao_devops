# import telnetlib
#
#
# tm = telnetlib.Telnet(host="192.168.1.1",port=22,timeout=3)
# tm.read_until('\n'.encode(),timeout=5)

import paramiko

"""
使用账号密码登录
"""
# 实例化ssh客户端对象
jssh = paramiko.SSHClient()
# 处理第一次连接的策略
jssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# 连接服务器
jssh.connect("106.13.54.147", 22, "root", "HHH111@@@")
_, stdout, _ = jssh.exec_command("ls /")
# print(stdin.read())
print(str(stdout.read()),"out")

"""
使用秘钥进行登录
"""
# jssh = paramiko.SSHClient()
# jssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# key = paramiko.RSAKey.from_private_key_file("/Users/haoqihan/.ssh/id_rsa")
# jssh.connect("106.13.54.147", 22, "root", pkey=key)
