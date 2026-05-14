"""
编写一个递归函数 sum_digits(n)，计算给定正整数 n 的各位数字之和。
要求：

输入：一个正整数 n（1 <= n <= 10^9）
输出：给定正整数 n 的各位数字之和
示例： 输入：12345 输出：15
"""
def sum_digits(n):
    if n < 10:
        return n
    return sum_digits(n // 10) + n % 10


print(sum_digits(12345))

def yuanshen(n):  #猴子最后一天还剩一个桃，把n看作桃坚持吃了天的第一天，但是n是坚持的天数，然后反向推
    if n == 1:    #n == 1看作最后一天而不是第一天
        return 1
    return (yuanshen(n - 1) + 1) * 2


print(yuanshen(10))

