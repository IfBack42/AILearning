'''
编写一个函数 find_duplicates(nums)，接受一个整数列表 nums 作为输入，并返回该列表中所有重复出现的元素。
要求函数返回的结果是一个集合（set），包含列表中所有重复的元素（仅出现一次即可）
'''
list_ = [1,1,2,3,4,2,5,6,4,7,8,5,6,8,7,9]
def find_duplicates(nums):
    # test_set = set()
    # final_set = set()
    # for i in nums:
    #     if i in test_set:
    #         final_set.add(i)
    #     test_set.add(i)
    test_list = []
    final_set = set()
    for i in nums:
        if i in test_list:
            final_set.add(i)
        test_list.append(i)
    print(final_set)
find_duplicates(list_)
