# 创建数据库
# create database test_platform charset=utf8;
# 创建用户
# create user dev_user identified by '123456';
# 授权用户
#grant all on meiduo.* to 'itheima'@'%';
# grant all on test_platform.* to 'dev_user'@'%';
# 刷新权限
# flush privileges ;
# show columns from tb_user;
# show status ;
# SHOW ERRORS;
# SHOW WARNINGS;
select  distinct  *from tb_user;