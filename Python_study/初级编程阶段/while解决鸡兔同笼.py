#请用while循环解决如下问题，鸡兔同笼共94只脚，35个头，鸡兔个有多少只？
hen = 0
hen_fo = 0
rab = 35
rab_fo = 0
while hen_fo + rab_fo != 94:
    hen += 1
    rab -= 1
    hen_fo = hen * 2
    rab_fo = rab * 4
print(f"有{hen}只鸡，{rab}只兔")
