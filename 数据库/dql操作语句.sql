# =============== 案例1 演示单表约束 ======================
/*
  约束：
    概述：
        在数据类型的基础上，继续对某列数据值做限定
        用来保证数据完整性和安全性
    分类：
        单表约束：
            主键约束： primary key 结合 auto_increment
            非空约束： not null 可以重复
            唯一约束： unique 可以为空
            默认约束： default
        多表约束：
            主外键约束： foreign key
 */

SHOW databases;
USE test;
SHOW tables;

# 1.创建数据表
CREATE table if not exists stu(
    id int primary key auto_increment,
    name varchar(20) not null,
    tel varchar(20) unique not null,
    gender varchar(2) not null default '男',
    address varchar(20) not null
);

SELECT * from stu;

DROP table stu;

INSERT into stu(name, tel, gender,address) VALUES ('肖杰','1145','男','伯今儿');
INSERT into stu(name, tel, gender,address) VALUES ('愚蠢','7777','男','兲禁');
INSERT into stu(name, tel, gender,address) VALUES ('神桃','2225','男','贺楠');
INSERT into stu(name, tel, gender,address) VALUES ('滋滋','0009','男','广嘻');

DESC  stu;

# =============== 案例2 演示单表查询 简单查询 ======================
/*
 单表查询完整格式：
 SELECT
    [distinct] 列名1 as 列名, 列名2 as 列名, ...
 from
    数据表名儿
 where
    组前筛选
 group by
    分组字段
 having
    组后筛选
 order by
    排序字段[asc|desc]
 limit
    起始索引,数据条数;
 */

# 1.创建商品表.
create table product(
    pid int primary key auto_increment, #商品id,主键
    pname varchar (20),                 #商品名
    price double,                       #商品单价
    category_id varchar (32)            #商品分类id
);

# 2.插入表数据
INSERT INTO product(pid,pname,price,category_id) VALUES(null, '联想',5000, 'c001');
INSERT INTO product(pid,pname,price,category_id) VALUEs(null, '海尔',3000, 'c001');
INSERT INTo product (pid,pname,price,category_id) VALUEs(null, '雷神',5000, 'c001');
INSERT INTO product (pid,pname,price, category_id) VALUES(null, '杰克琼斯',800, 'c002');
INSERT INTO product (pid,pname,price, category_id) VALUES(null,'真维斯',200, null);
INSERT INTO product(pid,pname, price,category_id) VALUES(6, '花花公子',440,'c002');
INSERT INTO product(pid, pname,price, category_id) VALUES(null,'劲',2000, 'c002');
INSERT INTO product (pid,pname,price,category_id) VALUES(null,'香儿',800, 'c003');
INSERT INTO product(pid,pname,price, category_id) VALUEs(null,'相本',200, null);
INSERT INTO product (pid,pname,price, category_id) VALUES(null, '面霸',5, 'c003');
INSERT INTO product(pid,pname,price, category_id) VALUES(null,'好想你枣',56, 'c004');
INSERT INTO product(pid,pname,price, category_id) VALUES(null,'香飘飘茶',1, 'c005');
INSERT INTO product (pid,pname,price, category_id) VALUES(null,'海之家',1,'c002');

TRUNCATE table product;

# 3.查看表数据
# 3.1查询所有数据
SELECT * from product;
SELECT pid,pname,price,category_id from product;
# 3.2查看 商品名 和 商品价格
SELECT pname,price from product;
# 扩展：起别名 列名 as 临时列名，其中as可以省略
SELECT pname 商品名儿,price 价格儿 from product p;
# 3.3 查看结果有表达式
SELECT pname,price + 10 from product;


# ================== 案例3:演示单表查询 条件查询 =================

# 场景1：比较查询
# 比较运算符：> ,< ,>= ,<= ,<> ,!=
# 格式: select 列名1，列名2..from 数表名 where 条件;

# 需求1:查询商品名称为“花花公子”的商品所有信息
SELECT * from product where pname='花花公子';

# 需求2:查询价格为800间品需求
SELECT * from product where price=800;

# 需求3:查询价格不是800的所有商品
SELECT * from product where price!=800;
SELECT * from product where price<>800;

# 需求4:在查询商品价格大于60元的所有商品信息
SELECT * from product where price>60;

# 需求5:查询商品价格小于等于800元的所有商品信息
SELECT * from product where price<=800;



# 场景2：范围查询： between 值1 and 值2 -> 范围内 ,in(值1，值2，值3...) -> 固定值间
# 逻辑运算符： and or not

# 需求1：查询商品价格在在200到1000间商品
SELECT * from product where price between 200 and 1000; # 包左包右
SELECT * from product where price>=200 and price<=800;

# 需求2：查询商品价格是200或800的所有商品
SELECT * from product where price in(200,800);
SELECT * from product where price=200 and price=800;

# 需求3：查询商品价格不是800的所有商品
SELECT * from product where price not in(800);
SELECT * from product where not price=800;
SELECT * from product where price!=800;


# 场景4：模糊查询，类似正则
# 格式： where 字段名 like '_%' ,其中_表示任意一个字符，%表示任意0到多个字符

# 需求1：查询所有‘香’开头的 商品
SELECT * from product where pname like '香%';

# 需求2：查询所有第二个字为‘想’的商品
SELECT * from product where pname like '_想%';


# 场景5：非空查询
# 格式：is null ，is not null ，不能用 =null 判断

# 需求1：查询没有分类的商品
SELECT * from product where category_id is null;

# 需求2：查询有分类的商品
SELECT * from product where category_id is not null;


# ================== 案例4:演示单表查询 排序查询 =================
# 格式：SELECT * from 表 order by 字段1 [asc|desc], 字段2 [asc|desc],...;
# ascending 升序   descending 降序 , 默认asc升序

# 需求1：根据价格升降序排序查询
SELECT * from product order by price;
SELECT * from product order by price asc;
SELECT * from product order by price desc;

# 需求2：根据价格降序排序查询，价格一样的情况根据分类降序降序
SELECT * from product order by price desc, category_id desc;


# ================== 案例5:演示单表查询 聚合查询 =================
/*
 聚合查询：
    count()     统计某列元素个数，只统计非空值
    sum()       求和某列元素
    max()       求最大值
    min()       求最小值
    avg()       求平均值
 小巧思：
    count(列名)，count(*)，count(1)区别：
    1.count(列名)只统计该列非空值，其他两个统计总数据条数
    2.效率上，count(主键列)>count(1)>count(*)>count(列名)
 */

# 需求1：查询商品总条数
SELECT count(*) total_cnt from product;
SELECT count(1) total_cnt from product;
SELECT count(pid) total_cnt from product;
SELECT count(category_id)  total_cnt from product;
# 需求2：查询价格大于200的商品总条数
SELECT count(price) total_cnt from product where price > 200;
# 需求3：查询分类为'c001'的商品总和
SELECT sum(price) sum from product where category_id = 'c001';
# 需求4：查询分类为'c002'的所有商品平均值
SELECT avg(price) avg_price  from product where category_id = 'c002';
# 需求5：查询商品最大价格和最小价格
SELECT max(price) max,min(price) min from product;
