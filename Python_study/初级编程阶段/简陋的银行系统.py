"""
编写一个银行账户管理系统的类BankAccount，具有以下功能：

账户属性包括：账号(account_number)，账户类型(account_type)，余额(balance)和交易历史记录(transactions)，账户类型可以有多种
初始化方法__init__()用于设置账户属性。

存款方法deposit(amount)：接收存款金额(amount)，如果金额大于0，则将金额加入余额(balance)，
并将存款信息添加到交易历史记录(transactions)中，并打印存款成功信息。

取款方法withdraw(amount)：接收取款金额(amount)，如果金额大于0且小于等于余额(balance)，
则从余额中扣除金额，并将取款信息添加到交易历史记录(transactions)中，并打印取款成功信息。否则，打印余额不足或者取款金额无效的信息。

转账方法transfer(recipient_account, amount)：接收收款账户(recipient_account)和转账金额(amount)。
如果金额大于0且小于等于余额(balance)，则从当前账户余额中扣除相应金额，将金额存入收款账户，
并在两个账户的交易历史记录(transactions)中添加相应信息，并打印转账成功信息。否则，打印余额不足或者转账金额无效的信息。

查看交易历史记录方法get_transaction_history()：打印当前账户的交易历史记录。
str()方法用于返回账户的信息字符串表示。

请根据以上要求完成BankAccount类的编写，完成如下需求。

1，打印账户余额：

打印123456789账户的账户号码，类型，余额
打印987654321账户的账户号码，类型，余额
2，针对123456789账户进行500元的存入，和2000元的取出

3，账户987654321给123456789转账共3000 元。

4，打印123456789 的交易历史记录。

并最终输出结果如下：

账号：123456789  类型：储蓄账户  余额：10000
账号：987654321  类型：支票账户  余额：5000

成功存入 500 元。当前余额为：10500 元。
成功取出 2000 元。当前余额为：8500 元。

开始转账
成功存入 3000 元。当前余额为：11500 元。
本次转账，账户987654321 成功转账给账户123456789共3000 元。

账户 123456789 的交易历史记录：
存入 500 元。
取出 2000 元。
存入 3000 元。

遵循如下代码开始编写：

# 创建账户对象
account1 = BankAccount("123456789", "储蓄账户", 10000)
account2 = BankAccount("987654321", "支票账户", 5000)
"""
class BankAccount:
    def __init__(self,account_number,account_type,balance):
        self.__account_number = account_number
        self.__account_type = account_type
        self.__balance = balance
        self.__transaction = []
    #余额查询
    def balance_check(self):
        print(f"账户{self.__account_number}，账户类型{self.__account_type}，账户余额为：{self.__balance}")
    #交易记录查询
    def transaction_check(self):
        print(f"账户{self.__account_number}交易记录：")
        for i in self.__transaction:
            print(i)
    #存钱
    def deposit(self,amount):
        self.__balance += amount
        print(f"账户{self.__account_number}，账户类型{self.__account_type}，{amount}元存款成功，当前余额为{self.__balance}元")
        self.__transaction.append(f"存入{amount}元")
    #取钱
    def withdraw(self,amount):
        if self.__balance >= amount:
            self.__balance -= amount
            print(f"账户{self.__account_number}，账户类型{self.__account_type}，{amount}元取款成功，当前余额为{self.__balance}元")
            self.__transaction.append(f"取出{amount}元")
        else:
            print("钱不太够")
    #转账
    def transfer(self,recipient_account, amount):
        if self.__balance >= amount:
            self.__balance -= amount
            print(f"账户{self.__account_number}成功给账户{recipient_account.__account_number}转入{amount}元，当前余额为{self.__balance}")
            recipient_account.__balance += amount
            self.__transaction.append(f"账户{self.__account_number}给账户{recipient_account.__account_number}转入{amount}元")
            recipient_account.__transaction.append(f"账户{self.__account_number}给账户{recipient_account.__account_number}转入{amount}元")
account1 = BankAccount("123456789", "储蓄账户", 10000)
account2 = BankAccount("987654321", "支票账户", 5000)
account1.balance_check()
account2.balance_check()
account1.deposit(500)
account1.withdraw(2000)
account2.transfer(account1,3000)
account1.transaction_check()






