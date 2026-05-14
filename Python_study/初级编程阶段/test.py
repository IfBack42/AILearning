# 在电商业务场景中，需要设计商品类、购物车类和用户类。具体描述如下：
#
# 商品类（Product）：每个商品对象应具有以下属性和方法：
# 属性：名称（name）、价格（price）、库存数量（stock）
# 方法：获取商品名称（get_name()）、获取商品价格（get_price()）、获取商品库存数量（get_stock()）、更新商品库存数量（update_stock(quantity)）

# 普通商品类（RegularProduct）：继承自商品类，每个普通商品对象应具有以下特有的方法：
# 方法：购买商品（buy_product(quantity)）：根据购买的数量减少商品库存量；如果库存不足，则输出"库存不足，无法购买该商品"；否则，减少库存数量。
# 方法：添加到购物车（add_to_cart(cart, quantity)）：将商品添加到指定购物车对象中，同时指定购买的数量。

# 折扣商品类（DiscountProduct）：继承自商品类，每个折扣商品对象应具有以下特有的属性和方法：
# 属性：折扣（discount）
# 方法：购买商品（buy_product(quantity)）：根据购买的数量减少商品库存量；如果库存不足，则输出"库存不足，无法购买该商品"；否则，减少库存数量。
# 方法：添加到购物车（add_to_cart(cart, quantity)）：将商品添加到指定购物车对象中，同时指定购买的数量。

# 购物车类（Cart）：每个购物车对象应具有以下属性和方法：
# 属性：商品项（items）,提示：考虑用字典进行存储
# 方法：添加商品（add_item(product, quantity)）：将指定数量的商品添加到购物车中；如果商品已存在于购物车，则增加该商品的数量；否则，添加新的商品项。
# 方法：删除商品（remove_item(product, quantity)）：从购物车中删除指定数量的商品；如果商品数量不足以删除，则直接删除该商品项；否则，减少商品数量。
# 方法：查看购物车内容（view_items()）：输出购物车中的商品项及其对应的数量。
# 方法：清空购物车（clear()）：将购物车中的商品项清空。

# 用户类（User）：每个用户对象应具有以下属性和方法：
# 属性：用户名（name）、购物车（cart）
# 方法：添加商品到购物车（add_to_cart(product, quantity)）：将指定数量的商品添加到用户的购物车中。
# 方法：查看购物车内容（view_cart()）：输出用户购物车中的商品项及其对应的数量。
# 方法：结算订单并支付（checkout()）：根据购物车中的商品项生成订单对象，并进行支付；支付成功后，清空购物车。

# 订单类（Order）：每个订单对象应具有以下属性和方法：
# 属性：购物车（cart）、总价（total_price）
# 方法：计算总价（calculate_total_price()）：根据购物车中的商品项计算订单的总价。
# 方法：支付（pay()）：执行支付逻辑，输出支付成功信息，并显示支付金额。

# 请使用面向对象的思想，设计并实现这些类，并编写主程序测试上述功能。请确保代码的正确性和健壮性，并合理处理各类之间的关系。
#
# 提示：在如下代码的基础上完善后续逻辑，需补充代码的部分都写了TODO。

class Product:
    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price

    def get_stock(self):
        return self.stock

    def update_stock(self, quantity):
        self.stock -= quantity


class RegularProduct(Product):
    def __init__(self, name, price, stock):
        super().__init__(name, price, stock)

    def buy_product(self, quantity):
        if self.stock < quantity:
            print("库存不足，无法购买该商品")
        else:
            self.stock -= quantity

    def add_to_cart(self, cart, quantity):
        cart.add_item(self, quantity)


class DiscountProduct(Product):
    def __init__(self, name, price, stock, discount):
        super().__init__(name, price, stock)
        self.discount = discount

    def buy_product(self, quantity):
        if self.stock < quantity:
            print("库存不足，无法购买该商品")
        else:
            self.stock -= quantity

    def add_to_cart(self, cart, quantity):
        cart.add_item(self, quantity)


class User:
    def __init__(self, name,cart):
        self.name = name
        self.cart = cart

    def add_to_cart(self, product, quantity):
        self.cart.add_item(product, quantity)

    def view_cart(self):
        self.cart.view_items()

    def checkout(self):
        # 方法：结算订单并支付（checkout()）：根据购物车中的商品项生成订单对象，并进行支付；支付成功后，清空购物车。
        order = Order(self.cart)
        order.pay()
        self.cart.clear()


class Cart:
    def __init__(self):
        self.items = {}

    def add_item(self, product, quantity):
        if product in self.items:
            self.items[product] += quantity
        else:
            self.items[product] = quantity

    def remove_item(self, product, quantity):
        if product in self.items:
            if quantity >= self.items[product]:
                del self.items[product]
            else:
                self.items[product] -= quantity

    def view_items(self):
        for product, quantity in self.items.items():
            print(f"{product.get_name()} - 数量：{quantity}")

    def clear(self):
        self.items.clear()


class Order:
    def __init__(self, cart):
        self.cart = cart
        self.total_price = self.calculate_total_price()

    def calculate_total_price(self):
        total_price = 0
        for product, quantity in self.cart.items.items():
            if isinstance(product, DiscountProduct):
                total_price += product.get_price() * product.discount * quantity
            else:
                total_price += product.get_price() * quantity
        return total_price

    def pay(self):
        # 实现支付逻辑
        print(f"支付成功！支付金额：{self.total_price}")


cart = Cart()
# 创建普通商品对象和折扣商品对象
regular_product = RegularProduct("iPhone 12", 6999, 100)
discount_product = DiscountProduct("Apple Watch", 1999, 50, 0.8)

# 创建用户对象
user = User("John",cart)

# 用户添加商品到购物车，并查看购物车
user.add_to_cart(regular_product, 2)
user.add_to_cart(discount_product, 3)
user.view_cart()

# 用户结算订单并支付
user.checkout()
# 打印结果：
#
# iPhone 12 - 数量：2
# Apple Watch - 数量：3
# 支付成功！支付金额：18795.6