# ===================案例1 DDL语句操作数据库 ====================

# 1.查看所有数据库
SHOW databases ;

# 2. 删除数据库
DROP database test;

# 3. 创建数据库
# 3.1 未设置防报错
CREATE database test;

# 3.2 设置防报错
CREATE database if not exists test;

# 3.3 设置码表
CREATE database test charset 'utf8';

# 4. 查询数据库详情信息
SHOW CREATE database if not exists test;

# 5. 修改数据库码表
ALTER database test charset 'gbk';

# 6. 选择数据库
USE test;

# 7. 查看当前使用的库
SELECT database();


# ===================案例2 DDL语句操作数据表 ====================
# 1.1 查看所有数据表
SHOW tables;

# 1.2 查看数据表的详情
DESC users;

# 2. 创建数据表
/*
 格式：
    CREATE table [if not exists] 表名(
        字段1 数据类型 [约束],
        字段2 数据类型 [约束],
        字段3 数据类型 [约束]
    );
 */
CREATE table if not exists users(
    id int,
    name varchar(20),
    password varchar(20)
);

# 3. 修改表名儿（一般不用）
ALTER table users rename xiaojie;
RENAME table users to xiaojie;

# 4. 删表
DROP table users;