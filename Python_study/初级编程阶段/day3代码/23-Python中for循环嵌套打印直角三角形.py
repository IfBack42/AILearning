'''
*
*  *
*  *  *
*  *  *  *
*  *  *  *  *
外层循环控制行数
内层循环控制列数
range(start, stop)
'''
for i in range(1,6):  # 1, 2, 3, 4, 5
    for j in range(1, i+1): # i=1, range(1,2)
        print('*', end='  ')
    print('')

