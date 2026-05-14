# ===================案例1 DML语句操作数据表 -> 增 ====================
/*
 DML语句：对数据表进行增删改操作

 添加数据方式：
 格式1：
    INSERT into 表名(列名1,列名2,列名3) values(值1,值2,值3);

 格式2：
    INSERT into 表名 values(值1,值2,值3);

 格式3：
    INSERT into 表名 values(值1,值2,值3); # 如果有主键约束则可以省略第一个值
 */

# 1.选择库
USE test;

# 2.展示所有表
SHOW tables;

# 3.查表
SELECT * from users;

# 4.添加数据
# 4.1格式1
INSERT users(id, name, password) VALUES (1,'xiaojie',114514);
INSERT users(name) VALUES ('战神');
INSERT
    users(id, name, password)
VALUES
    (3,'shentao',770626),
    (4,'yuchun',666666),
    (5,'zhenchang',888888);

# 4.2格式2
INSERT users VALUES(6,'滋滋',1919810);


# ===================案例2 约束入门 ====================
/*
 回顾：建表格式
    CREATE table **(
        字段1 数据类型 [约束],
        字段1 数据类型 [约束],
        字段1 数据类型 [约束]

 约束：
    概念：用来保证数据完整性和一致性
    分类：
        单表约束：
            primary key # 主键约束，非空、唯一，一张表只有一个主键
                        # 结合auto_increment使用，自增
            not null    # 非空约束，表示该列值不能为空
            unique      # 唯一约束，该列值不能重复
            default     # 默认约束，如果不传入值则默认值
            check       # 规则约束 低版本数据库无效
        多表约束：
            foreign key # 主外键
 */

# 1.创建学生表
CREATE table student(
    id int primary key auto_increment,  # 主键自增
    name varchar(20) not null ,         # 非空约束
    tel varchar(11) unique CHECK ( length(tel) = 11),            # 唯一约束
    gender varchar(1) default '男' unique    # 默认约束
);

DESC student;

SELECT * from student;

TRUNCATE table student;

INSERT into student values(null,'肖杰','1145141919','男');
INSERT into student values(null,'愚蠢','77777888888','男');
INSERT into student(name, tel, gender) values('神桃','999999999','男');

# ===================案例3 DML语句操作 改  ====================
# 格式： update 表名 set 字段1=值, 字段2=值 where 条件;
# 如果不加where条件则整张表都会被修改
# 例：修改 愚蠢为 滋滋，tle = 1234567

UPDATE student set name='滋滋', tel='12334567' where name='愚蠢';

# ===================案例4 DML语句操作 删  ====================
# 不加where条件，删除所有数据
DELETE from student;

# 加where条件， 删除具体行
DELETE from student where id=2;

# DELETE 和 TRUNCATE 区别：前者删除所有数据，id自增不重置；后者摧毁并重建表，id重置
# DELETE属于DML语句，可以结合事物使用。TRUNCATE属于DDL语句，不能结合事物使用

