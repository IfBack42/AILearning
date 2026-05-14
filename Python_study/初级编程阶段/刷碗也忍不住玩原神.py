#我负责刷10个碗，刷到第5个忍不住去玩原神去了
i = 1
while i <= 10:
    print(f"我正在刷第{i}个碗")
    print("-" * 20)
    i += 1
    if i == 5:
        print("忍不住了我要玩会儿原神！！")
        print("-" * 20)
        i += 1
        continue
