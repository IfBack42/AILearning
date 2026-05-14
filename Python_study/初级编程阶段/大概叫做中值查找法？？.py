# 给定一个整数列表，找出列表中两个元素的和等于目标值的所有组合。
# 提示：
#
# 在这个解决方案中，我们首先对输入列表进行排序，以便使用双指针方法。
#
# 然后，我们使用两个指针left和right分别指向列表的开头和结尾。我们计算指针所指向的两个元素的和，并与目标值进行比较。
#
# 如果和等于目标值，我们将这两个元素作为一个组合添加到结果列表中，并将left指针向右移动一位，将right指针向左移动一位。
# 如果和小于目标值，说明当前的和偏小，我们将left指针向右移动一位。
# 如果和大于目标值，说明当前的和偏大，我们将right指针向左移动一位。
# 重复以上步骤，直到left和right指针相遇为止。
# 测试列表
nums = [2, 4, 6, 8, 10,1,3,5,7,9]
nums = sorted(nums)
print(nums)
left = 0
right = 4
# 定义最后的总的列表
list_big = []
aim = int(input("你要的目标值："))
# 使用循环来一步步判断
while True:
    list_small = []
    if nums[right] + nums[left] == aim:
        list_small = [left,right]
        list_big.append(list_small)
        left += 1
        right -= 1
    elif nums[right] + nums[left] < aim:
        left += 1
    elif nums[right] + nums[left] > aim:
        right -= 1
    if right <= left:
        break
print(list_big)
