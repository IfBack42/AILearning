"""
假设我们正在创建一个银行账户管理系统，设计一个银行账户类（BankAccount），具有以下功能：

每个人都有：账号号码（account_number）和账户余额（balance），因为账户号码和账户余额都是隐身信息，所以只有账户持有人才有查看权限。
每个账户都可用于验证用户输入的PIN码是否正确validate_pin(self, pin)，因为对密码安全性保护较高，只有账户持有人才有输入密码，
尝试密码是否正确的权限。
每个账户都可以被存款deposit(amount)
每个账户都可以被取款，即从账户中取款指定金额，取款时需要输入PIN码进行验证withdraw(amount, pin)
余额充足，则可以取款
余额不足，则提示余额不足
密码错误，则提示Pin错误
在主程序中，创建一个银行账户对象，并调用公有方法进行存款和取款操作。

要求：

存款操作：直接将指定金额加到账户余额中
取款操作：先调用方法验证PIN码，若验证通过则将指定金额从账户余额中减去；若验证不通过则输出错误提示信息
参考如下方式创建账户对象
account = BankAccount("123456789", 1000)
"""

class BankAccount:
    def __init__(self,id,balance,pin):
        self.__id = id
        self.__balance = balance
        self.__pin = pin
        self.__is_acceptable = False
    def __validate_pin(self):
        if not self.__is_acceptable:
            users_pin = input("请输入密码：")
            if users_pin != self.__pin:
                print("错")
                return False
            else:
                self.__is_acceptable = True
        return self.__is_acceptable
    def deposit(self,amount):
        if self.__validate_pin():
            self.__balance += amount
            print(f"存款成功，当前余额为：{self.__balance}")
            self.__is_acceptable = False
    def withdraw(self,amount):
        if self.__validate_pin():
            if self.__balance >= amount:
                self.__balance -= amount
                print(f"取款成功，当前余额为：{self.__balance}")
            else:
                print("你钱够吗？")
            self.__is_acceptable = False
account = BankAccount("123456789", 1000,"123")
account.withdraw(200)
account.deposit(500)